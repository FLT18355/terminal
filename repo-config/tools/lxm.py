#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地音乐播放器 (基于 mpv)
=========================
功能:
  - 音乐播放 / 暂停 / 上一首 / 下一首 / 停止
  - 音乐目录   : 自动递归扫描指定目录下的音频文件 (可通过 config 子命令配置)
  - 音乐循环   : REPEAT_OFF / REPEAT_ALL / REPEAT_ONE 三种模式
  - lrc 加载   : 自动加载与音频同名的 .lrc 歌词, 并实时滚动显示
  - 随机播放   : 洗牌模式 (shuffle)
  - 列表播放   : 播放列表浏览与跳转
  - 使用 mpv   : 通过 mpv 的 JSON IPC 接口进行控制

依赖: 系统已安装 mpv (在 PATH 中)。
用法:
  python3 mpv_player.py [音乐目录]              # 启动播放器
  python3 mpv_player.py config --music-directory /xxx/xx   # 配置音乐目录
配置文件保存在 ~/.config/lxmusic/config.toml
"""

import os
import sys
import json
import time
import random
import math
import socket
import unicodedata
import tempfile
import subprocess
import curses
import argparse
import tomllib

# ---------------- 配置文件 ----------------
CONFIG_DIR = os.path.expanduser("~/.config/lxmusic")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.toml")


def load_config():
    """读取配置文件, 返回 dict; 不存在或损坏时返回 {}."""
    try:
        with open(CONFIG_FILE, "rb") as f:
            return tomllib.load(f)
    except (OSError, tomllib.TOMLDecodeError):
        return {}


def save_config(cfg):
    """将配置写入 ~/.config/lxmusic/config.toml (与现有配置合并)."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    merged = load_config()
    merged.update(cfg)
    lines = [
        "# 本地音乐播放器配置文件",
        "# 修改音乐目录: python3 mpv_player.py config --music-directory /xxx/xx",
        "",
    ]
    for k, v in merged.items():
        if isinstance(v, bool):
            lines.append('{} = {}'.format(k, "true" if v else "false"))
        elif isinstance(v, (list, tuple)):
            items = ', '.join('"{}"'.format(x) for x in v)
            lines.append('{} = [{}]'.format(k, items))
        elif isinstance(v, (int, float)):
            lines.append('{} = {}'.format(k, v))
        else:
            lines.append('{} = "{}"'.format(k, v))
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

# ---------------- 音频扩展名 ----------------
AUDIO_EXTS = {
    ".mp3", ".flac", ".m4a", ".ogg", ".wav", ".aac",
    ".opus", ".wma", ".ape", ".alac", ".oga", ".webm", ".aiff",
}

# ---------------- 循环模式 ----------------
REPEAT_OFF, REPEAT_ALL, REPEAT_ONE = "OFF", "ALL", "ONE"
REPEAT_CYCLE = [REPEAT_OFF, REPEAT_ALL, REPEAT_ONE]


def _dispw(text):
    """计算文本在终端中的显示宽度 (CJK 宽字符记 2 列)."""
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
               for ch in text)


def _pad_width(text, width):
    """用空格把文本补到指定显示宽度 (不截断)."""
    cur = _dispw(text)
    if cur >= width:
        return text
    return text + " " * (width - cur)


def _clip_width(text, maxw):
    """按终端显示宽度 (考虑 CJK 宽字符) 截断文本, 保证不会引发 curses ERR."""
    if maxw <= 0:
        return ""
    width = 0
    out = []
    for ch in text:
        cw = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        if width + cw > maxw:
            break
        out.append(ch)
        width += cw
    return "".join(out)


def scan_directory(root):
    """递归扫描目录, 返回所有音频文件排序列表."""
    files = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext in AUDIO_EXTS:
                files.append(os.path.join(dirpath, name))
    files.sort()
    return files


def find_lrc(path):
    """查找与音频同名的 .lrc 歌词文件, 找不到返回 None."""
    root, _ = os.path.splitext(path)
    for cand in (root + ".lrc", root + ".LRC"):
        if os.path.isfile(cand):
            return cand
    return None


def parse_lrc(path):
    """
    解析 LRC 歌词文件.
    返回 [(time_seconds, line), ...], 按时间排序.
    """
    tags = []          # 头部元信息 (ti/ar/al/by/offset 等)
    timestamps = []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                # 头部标签 例如 [ti:歌名]
                if line.startswith("[") and ":" in line and line.endswith("]"):
                    inner = line[1:-1]
                    if ":" in inner and len(inner.split(":")) == 2:
                        key, val = inner.split(":", 1)
                        key = key.strip().lower()
                        if key not in ("ti", "ar", "al", "by", "re", "ve", "offset", "length"):
                            pass
                        if key == "offset":
                            timestamps.append(["offset", val])
                            continue
                        tags.append((key, val))
                        continue
                # 普通歌词行: 可能含多个时间戳 [mm:ss.xx][mm:ss.xx]文本
                matches = []
                rest = line
                while rest.startswith("["):
                    end = rest.find("]")
                    if end == -1:
                        break
                    match = rest[1:end]
                    rest = rest[end + 1:]
                    if _parse_time(match) is not None:
                        matches.append(_parse_time(match))
                text = rest.strip()
                for t in matches:
                    timestamps.append((t, text))
    except OSError:
        return [], []

    timestamps.sort(key=lambda x: x[0] if isinstance(x[0], float) else -1)

    # 应用 offset (毫秒, 正数提前)
    offset = 0
    parsed = []
    for ts, text in timestamps:
        if isinstance(ts, str):   # "offset"
            try:
                offset = int(text)
            except ValueError:
                offset = 0
            continue
        if isinstance(ts, float):
            parsed.append((ts - offset / 1000.0, text))
    return parsed, tags


def _parse_time(s):
    """解析 'mm:ss.xx' 返回秒数, 失败返回 None."""
    try:
        if ":" in s:
            m, rest = s.split(":", 1)
            sec = float(rest) if "." in rest else int(rest)
            return int(m) * 60 + float(sec)
        return float(s)
    except (ValueError, TypeError):
        return None


# =========================================================
#  mpv JSON IPC 客户端
# =========================================================
class MpvClient:
    """通过 JSON IPC socket 与 mpv 进程通信."""

    def __init__(self, socket_path):
        self.sock = None
        self.socket_path = socket_path
        self._req = 0

    def connect(self, retries: int = 30, delay: float = 0.1):
        """等待 mpv socket 就绪并建立连接."""
        for _ in range(retries):
            try:
                self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.sock.connect(self.socket_path)
                self.sock.setblocking(False)
                return
            except OSError:
                try:
                    self.sock.close()
                except OSError:
                    pass
                time.sleep(delay)
        raise RuntimeError("无法连接 mpv IPC socket")

    def _command(self, name, *args):
        """发送命令并等待响应. 自动懒连接/断线重连."""
        self._req += 1
        reqid = self._req
        payload = json.dumps({"command": [name, *args], "request_id": reqid})
        # 确保 socket 已连接 (首次调用或断线时自动重连)
        for attempt in range(2):
            if self.sock is None:
                try:
                    self.connect(retries=10, delay=0.1)
                except RuntimeError:
                    return None
            try:
                self.sock.sendall((payload + "\n").encode())
                break
            except OSError:
                # socket 失效, 关闭后重连一次
                try:
                    self.sock.close()
                except OSError:
                    pass
                self.sock = None
                if attempt == 1:
                    return None
        # 读取响应 (阻塞读取到匹配 request_id)
        if self.sock is None:
            return None
        deadline = time.time() + 3.0
        buf = b""
        self.sock.setblocking(True)
        self.sock.settimeout(0.1)
        try:
            while time.time() < deadline:
                try:
                    data = self.sock.recv(4096)
                except (socket.timeout, BlockingIOError):
                    if b"\n" in buf:
                        for line in buf.split(b"\n"):
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            if obj.get("request_id") == reqid:
                                self.sock.setblocking(False)
                                return obj
                    buf = b""
                    continue
                if not data:
                    break
                buf += data
                while b"\n" in buf:
                    line, buf = buf.split(b"\n", 1)
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if obj.get("request_id") == reqid:
                        self.sock.setblocking(False)
                        return obj
        finally:
            self.sock.setblocking(False)
        return None

    def loadfile(self, path, **opts):
        """清空当前曲目并加载新文件."""
        args = [path, "replace"]
        extra = []
        for k, v in opts.items():
            if v is not None:
                extra.append("--" + k + "=" + str(v))
        return self._command("loadfile", *([args[0], args[1]] + extra))

    def append(self, path):
        return self._command("loadfile", path, "append")

    def pause(self, val):
        return self._command("set_property", "pause", True if val else False)

    def status(self):
        return self._command("get_property", "pause")

    def get_property(self, prop):
        return self._command("get_property", prop)

    def set_property(self, prop, value):
        return self._command("set_property", prop, value)

    def seek(self, seconds, absolute=False):
        if absolute:
            return self._command("seek", seconds, "absolute")
        return self._command("seek", seconds, "relative")

    def get_events(self):
        """读取缓冲区内所有未处理事件 (不阻塞)."""
        events = []
        if not self.sock:
            return events
        try:
            self.sock.setblocking(False)
        except OSError:
            # Socket 描述符已失效 (mpv 退出或连接断开)
            try:
                self.sock.close()
            except OSError:
                pass
            self.sock = None
            return events
        try:
            data = self.sock.recv(65536)
        except (BlockingIOError, socket.timeout, OSError):
            return events
        if not data:
            return events
        for line in data.split(b"\n"):
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "event" in obj:
                events.append(obj)
        return events


# =========================================================
#  播放器逻辑
# =========================================================
class Player:
    def __init__(self, playlist, socket_path, music_dir):
        self.playlist = playlist          # 完整曲目列表
        self.is_shuffle = playlist is not None and False
        self.repeat = REPEAT_OFF
        self.idx = 0
        self.queue = list(range(len(playlist))) if playlist else []
        self.music_dir = music_dir
        self.mpv = MpvClient(socket_path)
        self.playing = False
        self.paused = False
        self.current_path = None
        self.lyrics = []                  # [(time, line)]
        self.lyric_tags = []
        self.show_lyrics = True
        self.volume = 100
        self.speed = 1.0                  # 倍速播放
        # ---- 收藏夹 ----
        self.favorites = []               # 收藏的歌曲绝对路径列表
        self.fav_mode = False             # 是否只显示收藏
        # ---- 切歌淡入淡出 ----
        self.fade_state = None            # None / "in" / "out"
        self.fade_vol = 0.0               # 淡入淡出过程中的当前音量
        # ---- 断点续播 ----
        self.pending_seek = None          # 启动后待跳转的秒数

    def next_index(self, step=1):
        if not self.queue:
            return None
        if len(self.queue) == 1:
            return self.queue[0]
        pos = self.queue.index(self.idx) if self.idx in self.queue else 0
        return self.queue[(pos + step) % len(self.queue)]

    def previous_index(self):
        return self.next_index(-1)


# =========================================================
#  TUI (curses)
# =========================================================
class TUI:
    def __init__(self, stdscr, player: Player):
        self.stdscr = stdscr
        self.p = player
        self.scroll = 0
        self.sel = 0
        self.lyric_scroll = 0
        self.msg = ""
        self.msg_until = 0.0
        self.last_tick = 0.0
        self.time_pos = 0.0
        self.duration = 0.0
        self.title_tag = ""
        self.artist_tag = ""
        self.search_mode = False      # 是否在搜索输入模式
        self.search_query = ""        # 当前搜索关键词
        self.search_active = False    # 是否处于搜索结果浏览模式
        self.utf8_accum = b""         # UTF-8 字节累积缓冲（用于中文输入）
        self.show_help = False        # 帮助界面开关
        self.full_lyrics = False      # 全屏歌词模式

    # ---------- UI helpers ----------
    def _flash(self, text, seconds=1.2):
        self.msg = text
        self.msg_until = time.time() + seconds

    def _wrap(self, text, width):
        words = text.split()
        lines, cur = [], ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > width:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w) if cur else w
        # 最后的 cur 也要存入, 否则短行会被丢弃
        if cur:
            lines.append(cur)
        return lines or [""]

    # ---------- drawing ----------
    def _safe(self, y, x, text, attr=0):
        """安全的写屏: 宽度按显示列数截断并兜底捕获 curses.error."""
        std = self.stdscr
        try:
            _h, w = std.getmaxyx()
        except Exception:
            return
        # 按显示宽度截断, 避免末行/宽字符触发 ERR
        text = _clip_width(text, w - x)
        try:
            std.addnstr(y, x, text, w - x, attr)
        except curses.error:
            # 逐字降级, 遇到坏字符直接忽略该字符
            for ch in text:
                try:
                    std.addstr(y, x, ch, attr)
                    x += 1
                except curses.error:
                    break
    
    # ---------- 美化绘制辅助 ----------
    def _boxed(self, y, text, attr=0, left="│", right="│"):
        """带左右边框的内容行."""
        try:
            _h, w = self.stdscr.getmaxyx()
        except Exception:
            return
        inner = w - 2
        txt = _clip_width(text, inner)
        txt = _pad_width(txt, inner)
        self._safe(y, 0, left + txt + right, attr)

    def _sep(self, y, text="", attr=0):
        """分隔线: ├─ 标题 ─┤."""
        try:
            _h, w = self.stdscr.getmaxyx()
        except Exception:
            return
        inner = w - 2
        if text:
            mid = inner - _dispw(text)
            if mid < 2:
                mid = 2
            line = "├" + "─" * (mid // 2) + text + "─" * (mid - mid // 2) + "┤"
        else:
            line = "├" + "─" * inner + "┤"
        self._safe(y, 0, line, attr)

    def _equalizer(self):
        """伪频谱动画 (播放时跳动)."""
        p = self.p
        if not p.playing or p.paused:
            return "▁ ▁ ▁ ▁"
        t = self.time_pos
        chars = "▁▂▃▄▅"
        out = []
        for i in range(4):
            v = math.sin(t * 2.6 + i * 1.9) * math.cos(t * 1.3 + i * 0.7)
            h = int(abs(v) * 4.9) % 5
            out.append(chars[h])
        return " ".join(out)

    def draw(self):
        std, p = self.stdscr, self.p
        try:
            h, w = std.getmaxyx()
        except Exception:
            return
        if self.show_help:
            self._draw_help_screen(h, w)
            std.refresh()
            return
        if self.full_lyrics:
            self._draw_full_lyrics(h, w)
            std.refresh()
            return
        if h < 14 or w < 46:
            try:
                std.addstr(0, 0, "窗口太小啦喵~ 请放大终端 (至少 46x14)")
            except curses.error:
                pass
            std.refresh()
            return

        std.erase()
        inner = w - 2

        # ── 顶部边框 + 标题 ──
        mode = "🔀 随机" if p.is_shuffle else ("🔍 搜索" if self.search_active else "🎵 列表")
        rep = {"OFF": "不循环", "ALL": "列表循环", "ONE": "单曲循环"}[p.repeat]
        eq = self._equalizer()
        head_l = " 本地音乐播放器  {} ".format(eq)
        head_r = " {} ┊ {} ┊ 音量{} ".format(mode, rep, p.volume)
        mid = inner - _dispw(head_l) - _dispw(head_r)
        if mid < 2:
            mid = 2
        self._safe(0, 0, "┌" + head_l + "─" * mid + head_r + "┐",
                   curses.color_pair(2) | curses.A_BOLD)

        # ── 正在播放信息 ──
        now = p.playlist[p.idx] if p.playlist else ""
        base = os.path.basename(now) if now else "—"
        status = "▶ 播放中" if p.playing and not p.paused else (
            "⏸ 已暂停" if p.paused else "⏹ 待机")
        title = self.title_tag or os.path.splitext(base)[0]
        artist = self.artist_tag or (os.path.dirname(now).split(os.sep)[-1] if now else "")
        if self.search_active:
            info = " 🔍 搜索: {} ({} 首) ".format(
                self.search_query, len(p.queue) if p.queue else 0)
        else:
            info = " {} {} ".format(status, title)
            if artist:
                info += " ┊ " + artist
            if p.speed != 1.0:
                info += "  ×{:.2f}".format(p.speed)
        self._boxed(1, info, curses.color_pair(3))

        # ── 进度条 ──
        tpos, dur = self.time_pos, self.duration
        pct = min(max(tpos / dur, 0.0), 1.0) if dur > 0 else 0.0
        barw = max(inner - 20, 6)
        filled = int(barw * pct)
        prog = "█" * filled + "░" * (barw - filled)
        timestr = "{} / {}".format(self._fmt(tpos), self._fmt(dur))
        pctstr = "{:3d}%".format(int(pct * 100))
        self._safe(2, 0, "│", 0)
        self._safe(2, 1, " " + prog, curses.color_pair(4) | curses.A_BOLD)
        self._safe(2, barw + 2, " " + timestr + " " + pctstr, curses.color_pair(5))
        self._safe(2, w - 1, "│", 0)

        # ── 歌词区 ──
        y = 3
        self._sep(y, " 歌词 ", curses.color_pair(2))
        y += 1
        L = max((h - 8) // 2, 3)
        if self.p.show_lyrics and p.lyrics:
            self._draw_lyrics(y, w, L)
        else:
            if self.p.show_lyrics:
                self._boxed(y, " (无歌词文件喵~ 同名 .lrc)", 0)
            for r in range(1, L):
                self._boxed(y + r, "")
        y += L

        # ── 播放列表 ──
        P = (h - 8) - L
        if P < 1:
            P = 1
        if self.search_active:
            pl_title = " 搜索结果 {} 首 ".format(len(p.queue) if p.queue else 0)
        elif p.fav_mode:
            pl_title = " ♥ 收藏 {} 首 (F退出) ".format(len(p.queue) if p.queue else 0)
        elif self.search_mode:
            pl_title = " 播放列表 {} 首 · 输入中 ".format(len(p.playlist))
        else:
            pl_title = " 播放列表 {} 首 ".format(len(p.playlist))
        self._sep(y, pl_title, curses.color_pair(2))
        y += 1
        if not self.search_mode:
            self._draw_playlist(y, w, P)
        else:
            for r in range(P):
                self._boxed(y + r, "")
        y += P

        # ── 底部 (仅搜索输入栏 / 提示消息; 帮助已移到 h 全屏界面) ──
        if self.search_mode:
            self._boxed(h - 2, "/ 搜索: {}_".format(self.search_query),
                        curses.color_pair(5) | curses.A_BOLD)
        elif self.msg and time.time() < self.msg_until:
            self._boxed(h - 2, self.msg, curses.color_pair(5))
        else:
            self._boxed(h - 2, "")

        # ── 底部边框 ──
        self._safe(h - 1, 0, "└" + "─" * inner + "┘", curses.color_pair(4))

        std.refresh()

    def _draw_lyrics(self, y0, w, height):
        p = self.p
        lines = p.lyrics
        # 找到当前行
        cur = -1
        for i, (t, _txt) in enumerate(lines):
            if t <= self.time_pos:
                cur = i
        if cur < 0:
            cur = 0
        # 居中滚动
        center = cur - height // 2
        if center < 0:
            center = 0
        for r in range(height):
            i = center + r
            if i < len(lines):
                _t, txt = lines[i]
                txt = self._wrap(txt, w - 6)
                txt = txt[0] if txt else ""
                attr = curses.color_pair(2) if i == cur else 0
                if i == cur:
                    attr |= curses.A_BOLD
                self._boxed(y0 + r, ("♪ " if i == cur else "   ") + txt, attr)
            else:
                self._boxed(y0 + r, "")

    def _draw_playlist(self, y0, w, height):
        p = self.p
        if self.search_active or p.fav_mode:
            if not p.queue:
                self._boxed(y0, "  没有匹配结果喵~", 0)
                for r in range(1, height):
                    self._boxed(y0 + r, "")
                return
            n = len(p.queue)
            list_items = p.queue
        else:
            n = len(p.playlist)
            list_items = list(range(n))
            if n == 0:
                self._boxed(y0, "  目录里没有音频文件喵~", 0)
                for r in range(1, height):
                    self._boxed(y0 + r, "")
                return
        # 计算使选中项居中的视图起始行
        mid = height // 2
        start = self.sel - mid
        if start < 0:
            start = 0
        if start + height > n:
            start = max(n - height, 0)
        drawn = 0
        for r in range(min(height, n)):
            idx_in_list = start + r
            if idx_in_list >= len(list_items):
                break
            orig_idx = list_items[idx_in_list]
            name = os.path.basename(p.playlist[orig_idx])
            marker = "▶" if orig_idx == p.idx else " "
            marker += "♪" if p.lyrics and p.playlist[orig_idx] == p.current_path else " "
            fav = "♥" if p.playlist[orig_idx] in p.favorites else " "
            display_num = idx_in_list + 1 if (self.search_active or p.fav_mode) else orig_idx + 1
            line = "{} {} {}".format(marker, display_num, name)
            if fav == "♥":
                line += " ♥"
            line = _clip_width(line, w - 2)
            if self.search_active or p.fav_mode:
                is_selected = (idx_in_list == self.sel)
            else:
                is_selected = (orig_idx == self.sel)
            if is_selected:
                attr = curses.A_REVERSE
                if orig_idx == p.idx:
                    attr |= curses.color_pair(3)
            elif orig_idx == p.idx:
                attr = curses.color_pair(3)
            else:
                attr = 0
            self._boxed(y0 + r, line, attr)
            drawn += 1
        for r in range(drawn, height):
            self._boxed(y0 + r, "")

    def _draw_help_screen(self, h, w):
        """全屏帮助界面."""
        std = self.stdscr
        std.erase()
        inner = w - 2
        self._safe(0, 0, "┌" + _pad_width(" 帮助 · 本地音乐播放器 ", inner) + "┐",
                   curses.color_pair(2) | curses.A_BOLD)
        rows = [
            ("播放控制", [
                " 空格 / Enter   播放｜暂停｜播放选中",
                " n / p           下一首 / 上一首",
                " ← / →          快退 / 快进 5 秒",
                " [ / ]          快退 / 快进 10 秒",
            ]),
            ("倍速 & 音量", [
                " r / a           减速 / 加速 (0.25x ~ 4.0x)",
                " + / -           音量增 / 减",
            ]),
            ("列表 & 播放", [
                " ↑↓ / jk        选择曲目",
                " s               随机播放开关",
                " m               循环模式 (不循环/列表/单曲)",
                " l / L           歌词显示开关 / 全屏歌词 (KTV)",
                " f / F           收藏当前歌曲 / 只看收藏",
                " d               重新扫描目录",
            ]),
            ("搜索 & 其他", [
                " /               搜索 (支持中文, Enter执行, Esc退出)",
                " h               帮助界面 (再按任意键关闭)",
                " q / Esc         退出播放器 / 关闭搜索",
            ]),
            ("贴心功能", [
                " 断点续播       退出时记住歌曲与位置, 重开自动续播",
                " 切歌淡入淡出   上一首渐弱、下一首渐强, 自动生效",
            ]),
        ]
        y = 1
        for title, items in rows:
            if y >= h - 2:
                break
            self._boxed(y, " " + title, curses.color_pair(2) | curses.A_BOLD)
            y += 1
            for it in items:
                if y >= h - 2:
                    break
                self._boxed(y, it)
                y += 1
        self._boxed(h - 2, " 按任意键返回喵~ ", curses.color_pair(5))
        self._safe(h - 1, 0, "└" + "─" * inner + "┘", curses.color_pair(4))

    def _draw_full_lyrics(self, h, w):
        """全屏歌词模式 (KTV 风格): 当前句居中放大, 前后句暗色, 顶部歌名底部进度."""
        std = self.stdscr
        p = self.p
        std.erase()
        inner = w - 2
        now = p.playlist[p.idx] if p.playlist else ""
        base = os.path.basename(now) if now else "—"
        title = self.title_tag or os.path.splitext(base)[0]
        # 顶部: 歌名 + 状态
        status = "▶" if p.playing and not p.paused else ("❚❚" if p.paused else "⏹")
        head = " {}  {}  {}".format(status, title, os.path.basename(self.p.music_dir) if hasattr(self.p, 'music_dir') else "")
        self._safe(0, 0, "┌" + _pad_width(head, inner) + "┐",
                   curses.color_pair(2) | curses.A_BOLD)
        # 进度
        tpos, dur = self.time_pos, self.duration
        pct = min(max(tpos / dur, 0.0), 1.0) if dur > 0 else 0.0
        barw = inner - 18
        if barw < 6:
            barw = 6
        filled = int(barw * pct)
        prog = "█" * filled + "░" * (barw - filled)
        timestr = "{} / {}".format(self._fmt(tpos), self._fmt(dur))
        self._safe(1, 0, "│ " + prog + "  " + timestr + " │",
                   curses.color_pair(4))
        # 歌词主体: 当前行居中
        lines = p.lyrics
        cur = -1
        if lines:
            for i, (t, _txt) in enumerate(lines):
                if t <= self.time_pos:
                    cur = i
            if cur < 0:
                cur = 0
        mid = h // 2
        if lines:
            # 当前句 (居中大字, 加粗亮色)
            _t, txt = lines[cur][0], lines[cur][1]
            self._safe(mid - 1, 0, "  " + txt, curses.color_pair(3) | curses.A_BOLD)
            # 前后句 (小字暗色)
            for off in (1, 2, 3):
                if cur - off >= 0:
                    self._safe(mid - 1 - off, 0, "   " + lines[cur - off][1], curses.color_pair(4))
                if cur + off < len(lines):
                    self._safe(mid - 1 + off, 0, "   " + lines[cur + off][1], curses.color_pair(4))
        else:
            self._safe(mid, 0, "  (无歌词文件喵~ 同名 .lrc)", curses.color_pair(5))
        # 底部提示
        self._safe(h - 2, 0, "┌" + _pad_width(" 按 L / Esc 退出全屏歌词 ", inner) + "┐",
                   curses.color_pair(5))
        self._safe(h - 1, 0, "└" + "─" * inner + "┘", curses.color_pair(4))

    def _fmt(self, sec):
        sec = max(0, int(sec))
        return "{:02d}:{:02d}".format(sec // 60, sec % 60)

    # ---------- input ----------
    def handle(self, key):
        p = self.p
        try:
            c = chr(key)
        except ValueError:
            c = ""
        # ---------- 帮助界面: 按任意键关闭 ----------
        if self.show_help:
            self.show_help = False
            return True
        # ---------- 全屏歌词模式: 简单控制 ----------
        if self.full_lyrics:
            if key == ord("L") or key == 27 or c == "q":
                self.full_lyrics = False
            elif key == ord(" "):
                self.toggle_pause()
            elif c == "n":
                self.next_track()
            elif c == "p":
                self.prev_track()
            return True
        # ---------- 搜索输入模式 ----------
        if self.search_mode:
            if key == 13 or key == 10:  # Enter 执行搜索
                self.search_active = True
                self.search_mode = False
                query = self.search_query.lower()
                if query:
                    results = [i for i, path in enumerate(p.playlist)
                               if query in os.path.basename(path).lower()]
                    if results:
                        p.queue = results
                        p.idx = 0
                        self.sel = 0
                        self.msg = "搜索到 {} 首喵~ 关键词: {}".format(len(results), self.search_query)
                    else:
                        p.queue = []
                        self.msg = "没有找到 '{}' 喵~".format(self.search_query)
                else:
                    p.queue = list(range(len(p.playlist)))
                    self.search_active = False
                    self.msg = "已清空搜索喵~"
                self.msg_until = time.time() + 2.0
                return True
            elif key == 27:  # Esc 退出搜索输入
                self.search_mode = False
                self.search_active = False
                self.search_query = ""
                p.queue = list(range(len(p.playlist)))
                self.sel = 0
                self.msg = "已取消搜索喵~"
                self.msg_until = time.time() + 1.2
                return True
            elif key == 8 or key == 127 or key == 263:  # Backspace / DEL
                self.search_query = self.search_query[:-1] if self.search_query else ""
                self.utf8_accum = b""  # 重置 UTF-8 缓冲
                return True
            else:
                # UTF-8 字节累积: 中文多字节输入由终端逐字节传入
                # 对非控制字符累积字节，解码成功后写入搜索词
                if 0 < key < 256:
                    self.utf8_accum += bytes([key])
                    try:
                        ch = self.utf8_accum.decode('utf-8')
                        if ch.isprintable() or ch.isspace():
                            self.search_query += ch
                        self.utf8_accum = b""
                    except UnicodeDecodeError:
                        pass  # 字节不完整，继续等待
                    return True
                elif key > 255:
                    # 宽字符直接传入（部分终端行为）
                    try:
                        ch = chr(key)
                        if ch.isprintable() or ch.isspace():
                            self.search_query += ch
                    except ValueError:
                        pass
                    return True
                else:
                    return True

        # ---------- 搜索结果浏览模式 ----------
        if self.search_active:
            if key == ord("/"):
                self.search_mode = True
                self.search_query = ""
                self.utf8_accum = b""
                return True
            elif key == 27:  # Esc 退出搜索结果浏览，恢复全部列表
                self.search_active = False
                self.search_query = ""
                self.utf8_accum = b""
                p.queue = list(range(len(p.playlist)))
                self.sel = 0
                self.msg = "已退出搜索喵~"
                self.msg_until = time.time() + 1.2
                return True
            # 在搜索结果中浏览
            n = len(p.queue) if p.queue else 1
            if key in (curses.KEY_UP, ord("k")):
                self.sel = max(0, self.sel - 1)
            elif key in (curses.KEY_DOWN, ord("j")):
                self.sel = min(max(0, n - 1), self.sel + 1)
            elif key in (curses.KEY_ENTER, 10, 13):
                if p.queue:
                    self.play_index(p.queue[self.sel])
            return True

        if key in (curses.KEY_UP, ord("k")):
            self.sel = max(0, self.sel - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            self.sel = min(len(p.playlist) - 1, self.sel + 1)
        elif key in (curses.KEY_RIGHT,):
            self.seek(5)
        elif key in (curses.KEY_LEFT,):
            self.seek(-5)
        elif key == ord(" ") or key in (curses.KEY_ENTER, 10, 13):
            if key == ord(" "):
                self.toggle_pause()
            elif p.fav_mode and p.queue:
                # 收藏模式: sel 是收藏列表位置, 映射到真实播放列表索引
                self.play_index(p.queue[self.sel % len(p.queue)])
            else:
                self.play_index(self.sel)
        elif c == "s":
            self.toggle_shuffle()
        elif c == "m":
            self.cycle_repeat()
        elif c == "l":
            p.show_lyrics = not p.show_lyrics
            self._flash("歌词显示: " + ("开" if p.show_lyrics else "关"))
        elif c == "L":
            self.full_lyrics = not self.full_lyrics
            self._flash("全屏歌词模式: " + ("开" if self.full_lyrics else "关"))
        elif c == "f":
            self.toggle_favorite()
        elif c == "F":
            self.toggle_fav_mode()
        elif c == "h":
            self.show_help = not self.show_help
        elif c in ("+", "="):
            self.set_volume(p.volume + 5)
        elif c in ("-", "_"):
            self.set_volume(p.volume - 5)
        elif c == "[":
            self.seek(-10)
        elif c == "]":
            self.seek(10)
        elif c == "r":
            self.set_speed(p.speed - 0.25)
        elif c == "a":
            self.set_speed(p.speed + 0.25)
        elif c == "n":
            self.next_track()
        elif c == "p":
            self.prev_track()
        elif c == "d":
            self.refresh_dir()
        elif c == "/":
            self.search_mode = True
            self.search_query = ""
            self.search_active = False
            self.utf8_accum = b""
            self.msg = "搜索: 输入关键词后按回车"
            self.msg_until = time.time() + 3.0
        elif c == "q" or c == "Q" or key == 27:
            if self.search_mode:
                self.search_mode = False
                if self.search_active:
                    self.search_active = False
                    self.search_query = ""
                    self.sel = 0
                    self.msg = "已退出搜索喵~"
                    self.msg_until = time.time() + 1.5
                else:
                    return False
            else:
                return False
        elif c == ".":
            self.maybe_advance()
        return True

    # ---------- actions ----------
    def toggle_pause(self):
        p = self.p
        if not p.playing and p.queue:
            self.play_index(self.idx if self.idx else 0)
            return
        if p.playing:
            p.paused = not p.paused
            p.mpv.pause(p.paused)
            self._flash("已暂停喵~" if p.paused else "继续播放~")

    def play_index(self, i):
        p = self.p
        if not p.playlist:
            self._flash("没有可播放的曲目喵~")
            return
        p.idx = i % len(p.playlist)
        path = p.playlist[p.idx]
        p.current_path = path
        self._load_lyrics(path)
        opts = ["--loop-file=inf"] if p.repeat == REPEAT_ONE else []
        p.mpv.loadfile(path, **{})  # simply load
        p.mpv.set_property("speed", p.speed)  # 同步倍速
        p.playing = True
        p.paused = False
        self.time_pos, self.duration = 0, 0
        # 选中项同步: 收藏/搜索模式下 sel 应是队列内位置, 否则是真实索引
        if (p.fav_mode or self.search_active) and p.queue and p.idx in p.queue:
            self.sel = p.queue.index(p.idx)
        else:
            self.sel = p.idx
        self.scroll = max(0, p.idx)
        # 淡入淡出: 新歌从低音量渐升到设定音量
        p.fade_vol = 1.0
        p.fade_state = "in"
        p.mpv.set_property("volume", 1.0)
        self._flash("♪ 正在播放: " + os.path.basename(path), 1.5)

    def _load_lyrics(self, path):
        p = self.p
        lrc = find_lrc(path)
        if lrc:
            p.lyrics, p.lyric_tags = parse_lrc(lrc)
            self.title_tag = ""
            self.artist_tag = ""
            for k, v in p.lyric_tags:
                if k == "ti" and not self.title_tag:
                    self.title_tag = v
                elif k == "ar" and not self.artist_tag:
                    self.artist_tag = v
        else:
            p.lyrics, p.lyric_tags = [], []
            self.title_tag, self.artist_tag = "", ""

    def next_track(self):
        return self._advance(1)

    def prev_track(self):
        return self._advance(-1)

    def _advance(self, step):
        p = self.p
        if not p.queue:
            return
        cur = p.idx
        pos = p.queue.index(cur) if cur in p.queue else 0
        np = pos + step
        if p.repeat == REPEAT_OFF:
            if np < 0 or np >= len(p.queue):
                self._flash("已经是最后一首啦喵~")
                return
        np %= len(p.queue)
        self.play_index(p.queue[np])

    def maybe_advance(self):
        """当 mpv 报告播放结束 (end-file) 时调用."""
        p = self.p
        if p.repeat == REPEAT_ONE:
            # 重新加载当前曲目实现单曲循环
            self.play_index(p.idx)
            return
        self._advance(1)

    def toggle_shuffle(self):
        p = self.p
        p.is_shuffle = not p.is_shuffle
        if p.is_shuffle:
            rest = [i for i in range(len(p.playlist)) if i != p.idx]
            random.shuffle(rest)
            p.queue = [p.idx] + rest
            self._flash("🔀 随机播放已开启")
        else:
            p.queue = list(range(len(p.playlist)))
            self._flash("🎵 顺序播放已开启")

    def cycle_repeat(self):
        p = self.p
        i = REPEAT_CYCLE.index(p.repeat)
        p.repeat = REPEAT_CYCLE[(i + 1) % len(REPEAT_CYCLE)]
        self._flash("循环模式: " + {"OFF": "不循环", "ALL": "列表循环", "ONE": "单曲循环"}[p.repeat])

    def set_volume(self, vol):
        p = self.p
        p.volume = max(0, min(150, vol))
        p.mpv.set_property("volume", p.volume)

    def set_speed(self, spd):
        p = self.p
        p.speed = max(0.25, min(4.0, round(spd, 2)))
        p.mpv.set_property("speed", p.speed)
        self._flash("倍速: {:.2f}x".format(p.speed))

    def toggle_favorite(self):
        """收藏 / 取消收藏当前选中的歌曲."""
        p = self.p
        if not p.playlist:
            return
        # 收藏/搜索模式: sel 是列表内的位置, 需映射到真实播放列表索引
        if p.fav_mode and p.queue:
            target = p.playlist[p.queue[self.sel % len(p.queue)]]
        else:
            target = p.playlist[self.sel]
        if target in p.favorites:
            p.favorites.remove(target)
            self._flash("已取消收藏: " + os.path.basename(target))
        else:
            p.favorites.append(target)
            self._flash("♥ 已收藏: " + os.path.basename(target))
        save_config({"favorites": list(p.favorites)})

    def toggle_fav_mode(self):
        """只看收藏模式开关 (队列 = 收藏列表)."""
        p = self.p
        if p.fav_mode:
            p.fav_mode = False
            p.queue = list(range(len(p.playlist)))
            self._flash("已退出收藏模式")
        else:
            if not p.favorites:
                self._flash("还没有收藏喵~ 按 f 收藏歌曲")
                return
            fav_idx = [i for i, x in enumerate(p.playlist) if x in p.favorites]
            if not fav_idx:
                self._flash("收藏的歌曲不在当前目录喵~")
                return
            p.fav_mode = True
            p.queue = fav_idx
            self.sel = 0
            self._flash("♥ 收藏模式: {} 首".format(len(fav_idx)))

    def save_state(self):
        """退出前保存断点续播状态 (歌曲 + 位置)."""
        p = self.p
        if p.current_path and p.playing:
            save_config({"last_path": p.current_path,
                         "last_pos": round(self.time_pos, 1)})
        elif p.current_path:
            save_config({"last_path": p.current_path,
                         "last_pos": 0})

    def seek(self, sec):
        p = self.p
        if p.playing:
            p.mpv.seek(sec)
            self._flash("快进 {} 秒喵~".format(sec) if sec > 0 else "快退 {} 秒喵~".format(-sec))

    def refresh_dir(self):
        p = self.p
        import glob
        new = scan_directory(p.music_dir)
        keep = set(os.path.realpath(x) for x in new)
        old_real = os.path.realpath(p.playlist[p.idx]) if p.playlist else None
        p.playlist = new
        if old_real is not None:
            try:
                p.idx = [os.path.realpath(x) for x in new].index(old_real)
            except ValueError:
                p.idx = 0
        if p.is_shuffle:
            self.toggle_shuffle(); self.toggle_shuffle()
        else:
            p.queue = list(range(len(new)))
        self._flash("扫描完成喵~ 共 {} 首".format(len(new)))

    # ---------- event polling ----------
    def poll_mpv_events(self):
        p = self.p
        try:
            for ev in p.mpv.get_events():
                name = ev.get("event")
                if name == "end-file":
                    reason = ev.get("reason")
                    if reason in ("eof", "stop"):
                        self.maybe_advance()
                elif name == "idle":
                    pass
            # 刷新时间与属性
            if p.playing:
                r = p.mpv.get_property("time-pos")
                if r and isinstance(r.get("data"), (int, float)):
                    self.time_pos = float(r["data"])
                r = p.mpv.get_property("duration")
                if r and isinstance(r.get("data"), (int, float)):
                    self.duration = float(r["data"])
                # 断点续播: 启动后待跳转位置, 等文件加载好再跳
                if p.pending_seek is not None and self.time_pos > 0.2:
                    p.mpv.seek(p.pending_seek, absolute=True)
                    self.time_pos = p.pending_seek
                    self._flash("已续播到 {} 喵~".format(self._fmt(p.pending_seek)))
                    p.pending_seek = None
                # 淡入淡出
                self._update_fade(p)
        except Exception:
            pass  # mpv socket 断开时静默忽略，避免主循环崩溃

    def _update_fade(self, p):
        """每帧处理淡入淡出: 淡入渐升, 歌曲快结束时淡出."""
        FADE_STEP = p.volume / 8.0   # 约 8 帧 (=1.6s) 完成淡入
        # 淡入: 音量渐升到目标
        if p.fade_state == "in" and not p.paused:
            p.fade_vol += FADE_STEP
            if p.fade_vol >= p.volume:
                p.fade_vol = p.volume
                p.fade_state = None
            p.mpv.set_property("volume", p.fade_vol)
            return
        # 淡出: 歌曲接近结尾 (排除单曲循环, 避免音量卡在 0)
        if (p.fade_state is None and not p.paused and p.repeat != REPEAT_ONE
                and self.duration > 2.0
                and self.time_pos > self.duration - 2.0):
            p.fade_state = "out"
            p.fade_vol = p.volume
        if p.fade_state == "out":
            p.fade_vol -= FADE_STEP
            if p.fade_vol <= 0:
                p.fade_vol = 0
            p.mpv.set_property("volume", p.fade_vol)


# =========================================================
#  主循环
# =========================================================
def main_loop(stdscr, playlist, socket_path, music_dir):
    curses.curs_set(0)
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    # Catppuccin Latte 配色方案 — 将标准 curses 颜色重新映射为 Latte 色值
    # 使用 curses.init_color 重定义索引颜色 (RGB 范围 0-1000)
    # Latte: Sky #04a5e5 | Green #40a02b | Yellow #df8e1d | Pink #ea76cb | Base #eff1f5
    try:
        # 重新映射标准颜色索引接近 Latte 色值
        curses.init_color(curses.COLOR_GREEN,  251, 627, 169)  # Green #40a02b
        curses.init_color(curses.COLOR_YELLOW, 875, 557, 114)  # Yellow #df8e1d
        curses.init_color(curses.COLOR_MAGENTA, 918, 462, 796) # Pink #ea76cb
        curses.init_color(curses.COLOR_CYAN,    15, 643, 898)  # Sky #04a5e5
        curses.init_color(curses.COLOR_WHITE,  936, 945, 960)  # Base #eff1f5 (浅背景)
    except curses.error:
        pass  # 终端不支持自定义颜色时静默回退
    curses.init_color(8, 0, 0, 0)  # 保留黑色作为备用
    curses.init_pair(1, 7, -1)     # 默认：Base 白 (#eff1f5) 背景 + 默认前景
    curses.init_pair(2, 6, -1)     # Sky (#04a5e5) 高亮
    curses.init_pair(3, 2, -1)     # Green (#40a02b) 当前播放
    curses.init_pair(4, 3, -1)     # Yellow (#df8e1d) 进度/提示
    curses.init_pair(5, 5, -1)     # Pink (#ea76cb) 消息

    player = Player(playlist, socket_path, music_dir)
    player.queue = list(range(len(playlist)))
    # 主循环里的播放器也建立 mpv 连接
    try:
        player.mpv.connect()
    except RuntimeError as e:
        pass

    tui = TUI(stdscr, player)

    # ---- 恢复断点续播: 上次播放的歌曲 + 位置 ----
    cfg = load_config()
    player.favorites = list(cfg.get("favorites", []))
    last_path = cfg.get("last_path")
    last_pos = cfg.get("last_pos", 0)
    if last_path:
        try:
            resume_idx = playlist.index(last_path)
            player.idx = resume_idx
            player.current_path = last_path
            tui.sel = resume_idx
            tui.play_index(resume_idx)
            if last_pos:
                player.pending_seek = float(last_pos)
        except ValueError:
            pass  # 上次的歌不在当前目录, 忽略

    stdscr.nodelay(True)
    try:
        stdscr.timeout(200)  # 200ms 刷新循环
    except Exception:
        pass

    stdscr.clear()
    while True:
        # 绘制
        tui.draw()

        # 处理 mpv 事件
        tui.poll_mpv_events()

        # 读取按键
        try:
            key = stdscr.getch()
        except Exception:
            key = -1

        if key != -1:
            if not tui.handle(key):
                break
            if player.paused is False and player.playing:
                pass

    # 退出前保存断点
    try:
        tui.save_state()
    except Exception:
        pass
    # 退出时清理
    try:
        player.mpv.set_property("shutdown", "all")
    except Exception:
        pass


def handle_config(argv):
    """config 子命令: 配置/查看音乐目录."""
    p = argparse.ArgumentParser(prog="mpv_player.py config",
                                description="配置音乐目录")
    p.add_argument("--music-directory", metavar="DIR",
                   help="设置音乐目录并保存到配置文件")
    args = p.parse_args(argv)
    if args.music_directory:
        music_dir = os.path.abspath(os.path.expanduser(args.music_directory))
        if not os.path.isdir(music_dir):
            print("目录不存在喵: {}".format(music_dir))
            sys.exit(1)
        save_config({"music_directory": music_dir})
        print("已保存配置喵~")
        print("  配置文件: {}".format(CONFIG_FILE))
        print("  音乐目录: {}".format(music_dir))
    else:
        cfg = load_config()
        if cfg.get("music_directory"):
            print("当前音乐目录: {}".format(cfg["music_directory"]))
            print("  配置文件: {}".format(CONFIG_FILE))
        else:
            print("尚未配置音乐目录喵~")
            print("用法: python3 mpv_player.py config --music-directory /xxx/xx")


def main():
    # 手动识别 config 子命令 (避免 argparse 子命令与音乐目录位置参数冲突)
    argv = sys.argv[1:]
    if argv and argv[0] == "config":
        handle_config(argv[1:])
        return

    parser = argparse.ArgumentParser(description="本地音乐播放器 (基于 mpv)")
    parser.add_argument("dir", nargs="?", default=None,
                        help="音乐目录 (默认读取 ~/.config/lxmusic/config.toml, 再回退 ~/Music)")
    args = parser.parse_args(argv)

    # ---------- 确定音乐目录 (优先级: 命令行 > 配置文件 > ~/Music) ----------
    cfg = load_config()
    music_dir = args.dir or cfg.get("music_directory") or os.path.expanduser("~/Music")
    music_dir = os.path.abspath(os.path.expanduser(music_dir))
    if not os.path.isdir(music_dir):
        print("目录不存在喵: {}".format(music_dir))
        print("可用 python3 mpv_player.py config --music-directory /xxx/xx 配置")
        sys.exit(1)

    playlist = scan_directory(music_dir)
    if not playlist:
        print("在 {} 中没找到音频文件喵~".format(music_dir))
        sys.exit(1)

    print("扫描到 {} 首曲目喵~".format(len(playlist)))

    # 启动 mpv
    socket_path = os.path.join(tempfile.gettempdir(),
                               "lanxi_mpv_{}.sock".format(os.getpid()))
    if os.path.exists(socket_path):
        try:
            os.remove(socket_path)
        except OSError:
            pass

    cmd = ["mpv", "--idle=yes", "--no-video", "--input-ipc-server=" + socket_path,
           "--terminal=no", "--quiet", "--no-config",
           "--volume=100"]
    try:
        mpv_proc = subprocess.Popen(cmd)
    except FileNotFoundError:
        print("未找到 mpv, 请先安装喵~")
        sys.exit(1)

    # 等待 socket
    try:
        # 启动 mpv 后由其自身建立 socket, 这里先等待创建
        deadline = time.time() + 3.0
        while not os.path.exists(socket_path) and time.time() < deadline:
            time.sleep(0.05)
        curses.wrapper(main_loop, playlist, socket_path, music_dir)
    finally:
        mpv_proc.terminate()
        try:
            mpv_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            mpv_proc.kill()
        if os.path.exists(socket_path):
            try:
                os.remove(socket_path)
            except OSError:
                pass


if __name__ == "__main__":
    main()