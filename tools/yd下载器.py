#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

"""
🎬 全能下载工具箱 v26.4 (Rich 美化版)
功能：yt-dlp(视频) + wget(文件) + curl(网络)
修复：视频大小显示优化
"""

import os
import sys
import subprocess
import json
import time
import re
from datetime import datetime
from pathlib import Path

# Rich 美化库
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.prompt import Prompt, Confirm
    from rich import print as rprint
    from rich.layout import Layout
    from rich.text import Text
    from rich.columns import Columns
    from rich.syntax import Syntax
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    # 简单回退
    def rprint(*args, **kwargs): print(*args)
    class DummyConsole:
        def print(self, *args, **kwargs): print(*args)
        def clear(self): os.system('clear')
    console = DummyConsole()

class DownloadToolbox:
    def __init__(self):
        self.download_path = os.path.expanduser("~/storage/downloads")
        self.history_file = os.path.expanduser("~/.download_history.json")
        self.history = self.load_history()
        
        os.makedirs(self.download_path, exist_ok=True)
    
    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history[-100:], f, indent=2)
        except:
            pass
    
    def print_header(self, title):
        """打印标题"""
        if HAS_RICH:
            console.clear()
            console.rule(f"[bold cyan]{title}[/bold cyan]", style="bright_blue")
            print()
        else:
            os.system('clear')
            print("="*60)
            print(title.center(60))
            print("="*60)
            print()
    
    def add_to_history(self, url, tool, filename='', status='成功'):
        self.history.append({
            'url': url[:50],
            'tool': tool,
            'filename': filename,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'path': self.download_path,
            'status': status
        })
        self.save_history()
    
    # ========== 工具检查 ==========
    def check_ytdlp(self):
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '--version'],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def check_wget(self):
        try:
            subprocess.run(['wget', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def check_curl(self):
        try:
            subprocess.run(['curl', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def check_ffmpeg(self):
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    # ========== 修复：精确解析文件大小 ==========
    def parse_filesize(self, line):
        """从一行输出中精确解析文件大小"""
        # 常见的 yt-dlp 大小格式示例：
        # ~ 2.34 MiB
        # 1.5 MiB
        # 456.7 KiB
        # ~ 500.0 KiB
        # ≈ 1.2 MB (但通常是 MiB)
        
        # 尝试匹配 MiB
        mib_match = re.search(r'(\d+(?:\.\d+)?)\s*MiB', line)
        if mib_match:
            size = float(mib_match.group(1))
            if size < 1:
                return f"{size*1024:.1f} KiB"
            return f"{size:.1f} MiB"
        
        # 尝试匹配 KiB
        kib_match = re.search(r'(\d+(?:\.\d+)?)\s*KiB', line)
        if kib_match:
            size = float(kib_match.group(1))
            if size >= 1024:
                return f"{size/1024:.1f} MiB"
            return f"{size:.1f} KiB"
        
        # 尝试匹配 GiB
        gib_match = re.search(r'(\d+(?:\.\d+)?)\s*GiB', line)
        if gib_match:
            return f"{gib_match.group(1)} GiB"
        
        # 尝试匹配 ≈ 符号
        approx_match = re.search(r'[≈~]\s*(\d+(?:\.\d+)?)\s*([KM]i?B?)', line)
        if approx_match:
            size = float(approx_match.group(1))
            unit = approx_match.group(2)
            if 'MiB' in unit or 'MB' in unit:
                return f"{size:.1f} MiB"
            elif 'KiB' in unit or 'KB' in unit:
                if size >= 1024:
                    return f"{size/1024:.1f} MiB"
                return f"{size:.1f} KiB"
        
        # 尝试匹配任何数字 + 单位
        size_match = re.search(r'(\d+(?:\.\d+)?)\s*([KMGT]i?B?)', line)
        if size_match:
            size = float(size_match.group(1))
            unit = size_match.group(2)
            if 'GiB' in unit:
                return f"{size:.2f} GiB"
            elif 'MiB' in unit:
                if size < 1:
                    return f"{size*1024:.1f} KiB"
                return f"{size:.1f} MiB"
            elif 'KiB' in unit:
                if size >= 1024:
                    return f"{size/1024:.1f} MiB"
                return f"{size:.1f} KiB"
        
        return "未知"
    
    # ========== yt-dlp 视频下载 ==========
    def ytdlp_menu(self):
        """yt-dlp 视频下载"""
        if not self.check_ytdlp():
            console.print(Panel(
                "[red]❌ yt-dlp 未安装[/red]\n\n[yellow]运行: pip install yt-dlp[/yellow]",
                title="错误",
                border_style="red"
            ))
            input("\n按回车返回...")
            return
        
        # 检查 ffmpeg
        has_ffmpeg = self.check_ffmpeg()
        if not has_ffmpeg:
            console.print(Panel(
                "[yellow]⚠️ ffmpeg 未安装，视频可能没有声音[/yellow]\n\n[yellow]运行: pkg install ffmpeg[/yellow]",
                title="警告",
                border_style="yellow"
            ))
            if not Confirm.ask("是否继续？"):
                return
        
        while True:
            self.print_header("🎬 yt-dlp 视频下载")
            
            # 显示状态
            status_table = Table(show_header=False, box=None)
            status_table.add_column("项目", style="cyan")
            status_table.add_column("状态", style="white")
            status_table.add_row("📂 下载目录", self.download_path)
            status_table.add_row("🎵 音频支持", "✅ MP3" if has_ffmpeg else "⚠️ 需要ffmpeg")
            status_table.add_row("🎬 视频合并", "✅ 支持" if has_ffmpeg else "❌ 不支持")
            console.print(Panel(status_table, border_style="blue"))
            print()
            
            # 菜单
            menu = Table(show_header=False, box=None, padding=(0, 2))
            menu.add_column("选项", style="bold yellow")
            menu.add_column("功能", style="bold white")
            menu.add_column("说明", style="dim white")
            
            items = [
                ("[1]", "🎯 清晰度下载", "选择画质 (修复无声)"),
                ("[2]", "🔍 查看格式", "列出所有可用格式"),
                ("[3]", "🎵 音频下载", "MP3最佳音质"),
                ("[4]", "📑 播放列表", "批量下载"),
                ("[5]", "🍪 Cookie下载", "登录后下载"),
                ("[0]", "🔙 返回", "回主菜单"),
            ]
            
            for opt, name, desc in items:
                menu.add_row(opt, name, f"• {desc}")
            
            console.print(menu)
            print()
            
            choice = Prompt.ask("请选择", choices=["0","1","2","3","4","5"])
            
            if choice == "0":
                break
            elif choice == "2":
                url = Prompt.ask("[cyan]输入 URL[/cyan]")
                if url:
                    self.ytdlp_show_formats(url)
            elif choice == "3":
                url = Prompt.ask("[cyan]输入 URL[/cyan]")
                if url:
                    self.ytdlp_download_audio(url)
            elif choice == "4":
                url = Prompt.ask("[cyan]输入播放列表 URL[/cyan]")
                if url:
                    self.ytdlp_playlist(url)
            elif choice == "5":
                url = Prompt.ask("[cyan]输入 URL[/cyan]")
                if url:
                    self.ytdlp_cookie_download(url)
            elif choice == "1":
                url = Prompt.ask("[cyan]输入 URL[/cyan]")
                if url:
                    self.ytdlp_quality_select(url)
    
    def ytdlp_show_formats(self, url):
        """显示所有格式 (精确大小显示)"""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            progress.add_task("[cyan]获取视频信息...", total=None)
            
            result = subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '-F', url],
                capture_output=True,
                text=True
            )
        
        if result.returncode != 0:
            console.print("[red]❌ 获取失败[/red]")
            return
        
        # 创建表格
        table = Table(title="📋 可用格式", show_header=True)
        table.add_column("ID", style="yellow", width=8)
        table.add_column("扩展名", style="cyan", width=6)
        table.add_column("分辨率", style="white", width=14)
        table.add_column("大小", style="green", width=12)
        table.add_column("描述", style="dim white", width=40)
        
        lines = result.stdout.split('\n')
        in_format_section = False
        format_count = 0
        
        for line in lines:
            if 'ID  ' in line and 'EXT' in line and 'RESOLUTION' in line:
                in_format_section = True
                continue
            
            if in_format_section and line.strip() and not line.startswith('---'):
                parts = line.split()
                if len(parts) >= 7:
                    fmt_id = parts[0]
                    ext = parts[1]
                    resolution = parts[2]
                    
                    # 使用精确解析获取大小
                    display_size = self.parse_filesize(line)
                    
                    # 获取描述信息
                    desc = ' '.join(parts[6:]) if len(parts) > 6 else ''
                    
                    # 高亮最佳格式
                    if 'best' in desc.lower():
                        fmt_id = f"[green]{fmt_id}[/green]"
                    
                    table.add_row(fmt_id, ext, resolution, display_size, desc[:40])
                    format_count += 1
                    
                    if format_count >= 50:
                        break
        
        console.print(table)
        
        input("\n按回车继续...")
    
    def parse_formats(self, output):
        """解析格式信息"""
        formats = []
        lines = output.split('\n')
        in_format_section = False
        
        for line in lines:
            if 'ID  ' in line and 'EXT' in line and 'RESOLUTION' in line:
                in_format_section = True
                continue
            
            if in_format_section and line.strip() and not line.startswith('---'):
                parts = line.split()
                if len(parts) >= 7:
                    fmt_id = parts[0]
                    ext = parts[1]
                    resolution = parts[2]
                    
                    # 使用精确解析获取大小
                    filesize = self.parse_filesize(line)
                    
                    # 跳过纯音频
                    desc = ' '.join(parts[6:])
                    if 'audio only' in desc.lower():
                        continue
                    
                    # 提取分辨率数字
                    res_match = re.search(r'(\d+)x(\d+)', resolution)
                    if res_match:
                        height = int(res_match.group(2))
                        
                        if height >= 2160:
                            quality = '4K'
                        elif height >= 1440:
                            quality = '2K'
                        elif height >= 1080:
                            quality = '1080p'
                        elif height >= 720:
                            quality = '720p'
                        elif height >= 480:
                            quality = '480p'
                        else:
                            quality = f'{height}p'
                        
                        formats.append({
                            'id': fmt_id,
                            'quality': quality,
                            'resolution': resolution,
                            'ext': ext,
                            'size': filesize,
                            'raw_size': line  # 保留原始行用于调试
                        })
        
        return formats
    
    def ytdlp_quality_select(self, url):
        """清晰度选择下载 (修复大小显示)"""
        # 先获取格式
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            progress.add_task("[cyan]获取视频信息...", total=None)
            
            result = subprocess.run(
                [sys.executable, '-m', 'yt_dlp', '-F', url],
                capture_output=True,
                text=True
            )
        
        if result.returncode != 0:
            console.print("[red]❌ 获取格式失败[/red]")
            return
        
        # 解析格式
        formats = self.parse_formats(result.stdout)
        if not formats:
            console.print("[yellow]没有找到视频格式[/yellow]")
            return
        
        # 按清晰度分组
        quality_groups = {}
        for f in formats:
            if f['quality'] not in quality_groups:
                quality_groups[f['quality']] = []
            quality_groups[f['quality']].append(f)
        
        # 排序清晰度
        quality_order = {'4K':4, '2K':3, '1080p':2, '720p':1, '480p':0}
        sorted_qualities = sorted(quality_groups.keys(), 
                                 key=lambda x: quality_order.get(x, -1), 
                                 reverse=True)
        
        # 显示清晰度选项
        console.print("\n[bold cyan]🎯 选择清晰度:[/bold cyan]")
        for i, q in enumerate(sorted_qualities, 1):
            count = len(quality_groups[q])
            # 估算该清晰度的典型大小
            sizes = []
            for f in quality_groups[q][:3]:
                if 'MiB' in f['size']:
                    size_match = re.search(r'(\d+\.?\d*)', f['size'])
                    if size_match:
                        sizes.append(float(size_match.group(1)))
            
            if sizes:
                avg_size = sum(sizes) / len(sizes)
                size_hint = f"~{avg_size:.1f}MiB"
            else:
                size_hint = ""
            
            console.print(f"  {i}. {q} [dim]({count}种格式{ ' ' + size_hint if size_hint else ''})[/dim]")
        
        q_choice = Prompt.ask("选择", choices=[str(i) for i in range(1, len(sorted_qualities)+1)])
        selected_q = sorted_qualities[int(q_choice)-1]
        
        # 显示该清晰度的格式
        video_fmts = quality_groups[selected_q]
        console.print(f"\n[bold cyan]{selected_q} 可用格式:[/bold cyan]")
        
        # 按大小排序（尝试提取数字）
        def extract_size_num(size_str):
            match = re.search(r'(\d+\.?\d*)', size_str)
            if match:
                return float(match.group(1))
            return 0
        
        video_fmts.sort(key=lambda x: extract_size_num(x['size']), reverse=True)
        
        for i, f in enumerate(video_fmts, 1):
            console.print(f"  {i}. [yellow][{f['id']}][/yellow] {f['resolution']} {f['ext']} [green]{f['size']}[/green]")
        
        fmt_choice = Prompt.ask("选择格式编号", default="1")
        selected_fmt = video_fmts[int(fmt_choice)-1]['id']
        
        # 检查 ffmpeg
        has_ffmpeg = self.check_ffmpeg()
        
        console.print(f"\n[yellow]⏳ 正在下载...[/yellow]")
        
        if has_ffmpeg:
            # 有 ffmpeg：下载视频+最佳音频并合并
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-f', f'{selected_fmt}+bestaudio/best',
                '--merge-output-format', 'mkv',
                '-o', f'{self.download_path}/%(title)s_merged.%(ext)s',
                url
            ]
        else:
            # 无 ffmpeg：只下载视频流（可能无声）
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-f', selected_fmt,
                '-o', f'{self.download_path}/%(title)s.%(ext)s',
                url
            ]
        
        # 直接运行，不显示进度条
        subprocess.run(cmd)
        
        console.print("[green]✅ 下载完成！[/green]")
        self.add_to_history(url, 'yt-dlp')
        input("\n按回车继续...")
    
    def ytdlp_download_audio(self, url):
        """下载音频"""
        fmt = Prompt.ask("音频格式", choices=["mp3", "m4a", "opus"], default="mp3")
        
        console.print(f"\n[yellow]⏳ 下载音频中...[/yellow]")
        
        cmd = [
            sys.executable, '-m', 'yt_dlp',
            '-x', '--audio-format', fmt,
            '--audio-quality', '0',
            '-o', f'{self.download_path}/%(title)s.%(ext)s',
            url
        ]
        subprocess.run(cmd)
        
        console.print("[green]✅ 音频下载完成！[/green]")
        self.add_to_history(url, 'yt-dlp_audio')
        input("\n按回车继续...")
    
    def ytdlp_playlist(self, url):
        """下载播放列表"""
        console.print("选择类型:", style="yellow")
        console.print("  1. 🎵 音频")
        console.print("  2. 🎬 视频")
        
        choice = Prompt.ask("选择", choices=["1", "2"])
        
        console.print(f"\n[yellow]⏳ 下载播放列表中...[/yellow]")
        
        if choice == "1":
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-x', '--audio-format', 'mp3',
                '--yes-playlist',
                '-o', f'{self.download_path}/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s',
                url
            ]
        else:
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-f', 'best',
                '--yes-playlist',
                '-o', f'{self.download_path}/%(playlist_title)s/%(playlist_index)s-%(title)s.%(ext)s',
                url
            ]
        
        subprocess.run(cmd)
        
        console.print("[green]✅ 播放列表下载完成！[/green]")
        self.add_to_history(url, 'yt-dlp_playlist')
        input("\n按回车继续...")
    
    def ytdlp_cookie_download(self, url):
        """使用 Cookie 下载"""
        browser = Prompt.ask("浏览器", choices=["chrome", "firefox"], default="chrome")
        
        console.print(f"\n[yellow]⏳ 使用Cookie下载中...[/yellow]")
        
        cmd = [
            sys.executable, '-m', 'yt_dlp',
            '--cookies-from-browser', browser,
            '-o', f'{self.download_path}/%(title)s.%(ext)s',
            url
        ]
        subprocess.run(cmd)
        
        console.print("[green]✅ 下载完成！[/green]")
        self.add_to_history(url, 'yt-dlp_cookie')
        input("\n按回车继续...")
    
    # ========== wget 文件下载 ==========
    def wget_menu(self):
        """wget 文件下载"""
        if not self.check_wget():
            console.print(Panel(
                "[red]❌ wget 未安装[/red]\n\n[yellow]运行: pkg install wget[/yellow]",
                title="错误",
                border_style="red"
            ))
            input("\n按回车返回...")
            return
        
        while True:
            self.print_header("📥 wget 文件下载")
            
            menu = Table(show_header=False, box=None, padding=(0, 2))
            menu.add_column("选项", style="bold yellow")
            menu.add_column("功能", style="bold white")
            menu.add_column("说明", style="dim white")
            
            items = [
                ("[1]", "🌐 普通下载", "直接下载文件"),
                ("[2]", "🔄 断点续传", "继续未完成的下载"),
                ("[3]", "📊 限速下载", "控制下载速度"),
                ("[4]", "📁 批量下载", "从文件读取URL列表"),
                ("[5]", "📝 镜像网站", "递归下载整站"),
                ("[0]", "🔙 返回", "回主菜单"),
            ]
            
            for opt, name, desc in items:
                menu.add_row(opt, name, f"• {desc}")
            
            console.print(menu)
            print()
            
            choice = Prompt.ask("请选择", choices=["0","1","2","3","4","5"])
            
            if choice == "0":
                break
            
            url = Prompt.ask("[cyan]输入 URL[/cyan]")
            if not url:
                continue
            
            filename = url.split('/')[-1] or 'index.html'
            
            console.print(f"\n[yellow]⏳ 下载中...[/yellow]")
            
            if choice == "1":
                cmd = ['wget', '-P', self.download_path, url]
            elif choice == "2":
                cmd = ['wget', '-c', '-P', self.download_path, url]
            elif choice == "3":
                speed = Prompt.ask("限速 (K/s)")
                cmd = ['wget', '--limit-rate', f'{speed}k', '-P', self.download_path, url]
            elif choice == "4":
                file_path = Prompt.ask("URL列表文件路径")
                if os.path.exists(file_path):
                    cmd = ['wget', '-i', file_path, '-P', self.download_path]
                else:
                    console.print("[red]❌ 文件不存在[/red]")
                    continue
            elif choice == "5":
                depth = Prompt.ask("下载深度", default="3")
                cmd = ['wget', '-r', '-l', depth, '-P', self.download_path, url]
            else:
                continue
            
            subprocess.run(cmd)
            
            console.print("[green]✅ 下载完成！[/green]")
            self.add_to_history(url, 'wget', filename)
            input("\n按回车继续...")
    
    # ========== curl 网络工具 ==========
    def curl_menu(self):
        """curl 网络工具"""
        if not self.check_curl():
            console.print(Panel(
                "[red]❌ curl 未安装[/red]\n\n[yellow]运行: pkg install curl[/yellow]",
                title="错误",
                border_style="red"
            ))
            input("\n按回车返回...")
            return
        
        while True:
            self.print_header("🌐 curl 网络工具")
            
            menu = Table(show_header=False, box=None, padding=(0, 2))
            menu.add_column("选项", style="bold yellow")
            menu.add_column("功能", style="bold white")
            menu.add_column("说明", style="dim white")
            
            items = [
                ("[1]", "📥 下载文件", "普通下载"),
                ("[2]", "🔍 查看响应头", "查看HTTP头信息"),
                ("[3]", "🌍 外网IP", "查看公网IP地址"),
                ("[4]", "📝 POST请求", "发送POST数据"),
                ("[5]", "🔄 断点续传", "继续下载"),
                ("[6]", "🔐 Cookie请求", "带Cookie访问"),
                ("[0]", "🔙 返回", "回主菜单"),
            ]
            
            for opt, name, desc in items:
                menu.add_row(opt, name, f"• {desc}")
            
            console.print(menu)
            print()
            
            choice = Prompt.ask("请选择", choices=["0","1","2","3","4","5","6"])
            
            if choice == "0":
                break
            
            if choice == "3":
                console.print("\n[green]🌍 你的外网IP:[/green]")
                subprocess.run(['curl', '-s', 'ifconfig.me'])
                print()
                input("\n按回车继续...")
                continue
            
            url = Prompt.ask("[cyan]输入 URL[/cyan]")
            if not url:
                continue
            
            filename = url.split('/')[-1] or 'index.html'
            output = f'{self.download_path}/{filename}'
            
            console.print(f"\n[yellow]⏳ 执行中...[/yellow]")
            
            if choice == "1":
                cmd = ['curl', '-L', '-o', output, url]
            elif choice == "2":
                cmd = ['curl', '-I', url]
                subprocess.run(cmd)
                input("\n按回车继续...")
                continue
            elif choice == "4":
                data = Prompt.ask("POST数据")
                cmd = ['curl', '-X', 'POST', '-d', data, '-L', '-o', output, url]
            elif choice == "5":
                cmd = ['curl', '-L', '-C', '-', '-o', output, url]
            elif choice == "6":
                cookie = Prompt.ask("Cookie")
                cmd = ['curl', '-H', f'Cookie: {cookie}', '-L', '-o', output, url]
            else:
                continue
            
            subprocess.run(cmd)
            
            console.print("[green]✅ 完成！[/green]")
            self.add_to_history(url, 'curl', filename)
            input("\n按回车继续...")
    
    # ========== 历史记录 ==========
    def show_history(self):
        """显示历史记录"""
        self.print_header("📜 下载历史")
        
        if not self.history:
            console.print("[dim]暂无历史记录[/dim]")
        else:
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("#", style="yellow", width=4)
            table.add_column("时间", style="dim", width=16)
            table.add_column("工具", style="green", width=10)
            table.add_column("链接", style="white", width=40)
            
            for i, item in enumerate(self.history[-20:], 1):
                table.add_row(
                    str(i),
                    item['time'],
                    item['tool'],
                    item['url'][:40]
                )
            
            console.print(table)
        
        print()
        input("按回车继续...")
    
    # ========== 更改下载目录 ==========
    def change_path(self):
        """更改下载目录"""
        self.print_header("📂 更改下载目录")
        
        console.print(f"[cyan]当前目录:[/cyan] [white]{self.download_path}[/white]")
        print()
        
        console.print("[yellow]常用目录:[/yellow]")
        console.print("  1. ~/storage/downloads")
        console.print("  2. /sdcard/Download")
        console.print("  3. ~/Music")
        console.print("  4. ~/Videos")
        console.print("  5. 自定义")
        print()
        
        choice = Prompt.ask("选择", choices=["1","2","3","4","5"])
        
        if choice == "1":
            self.download_path = os.path.expanduser("~/storage/downloads")
        elif choice == "2":
            self.download_path = "/sdcard/Download"
        elif choice == "3":
            self.download_path = os.path.expanduser("~/Music")
        elif choice == "4":
            self.download_path = os.path.expanduser("~/Videos")
        elif choice == "5":
            path = Prompt.ask("输入路径")
            if path:
                self.download_path = os.path.expanduser(path)
        
        os.makedirs(self.download_path, exist_ok=True)
        console.print(f"[green]✅ 已更改为: {self.download_path}[/green]")
        input("\n按回车继续...")
    
    # ========== 主菜单 ==========
    def show_menu(self):
        """显示主菜单"""
        if HAS_RICH:
            console.clear()
            
            # 标题
            title = Text()
            title.append("🎬 ", style="bold cyan")
            title.append("全能下载工具箱", style="bold yellow")
            title.append(" v26.4", style="dim white")
            console.print(Panel(title, border_style="bright_blue"))
            print()
            
            # 状态
            status_table = Table(show_header=False, box=None)
            status_table.add_column("项目", style="cyan")
            status_table.add_column("状态", style="white")
            status_table.add_row("📂 下载目录", self.download_path)
            status_table.add_row("📊 历史记录", f"{len(self.history)} 条")
            
            # 工具检查
            yt_status = "[green]✓[/green]" if self.check_ytdlp() else "[red]✗[/red]"
            wget_status = "[green]✓[/green]" if self.check_wget() else "[red]✗[/red]"
            curl_status = "[green]✓[/green]" if self.check_curl() else "[red]✗[/red]"
            ffmpeg_status = "[green]✓[/green]" if self.check_ffmpeg() else "[yellow]⚠️[/yellow]"
            
            status_table.add_row("🎬 yt-dlp", yt_status)
            status_table.add_row("📥 wget", wget_status)
            status_table.add_row("🌐 curl", curl_status)
            status_table.add_row("🎵 ffmpeg", ffmpeg_status)
            
            console.print(Columns([status_table]))
            print()
            
            # 菜单
            menu = Table(show_header=False, box=None, padding=(0, 2))
            menu.add_column("选项", style="bold yellow", width=8)
            menu.add_column("功能", style="bold white", width=20)
            menu.add_column("说明", style="dim white")
            
            items = [
                ("[1]", "🎬 yt-dlp", "视频下载 (修复无声)"),
                ("[2]", "📥 wget", "文件下载"),
                ("[3]", "🌐 curl", "网络工具"),
                ("[4]", "📜 历史", "下载记录"),
                ("[5]", "📂 目录", "更改下载目录"),
                ("[0]", "❌ 退出", "再见"),
            ]
            
            for opt, name, desc in items:
                menu.add_row(opt, name, f"• {desc}")
            
            console.print(menu)
            print()
            
            return Prompt.ask("请选择", choices=["0","1","2","3","4","5"])
        else:
            # 无 Rich 的简单版本
            os.system('clear')
            print("="*60)
            print("全能下载工具箱 v26.4".center(60))
            print("="*60)
            print()
            print(f"下载目录: {self.download_path}")
            print(f"历史记录: {len(self.history)} 条")
            print()
            print("  [1] yt-dlp 视频下载")
            print("  [2] wget 文件下载")
            print("  [3] curl 网络工具")
            print("  [4] 下载历史")
            print("  [5] 更改下载目录")
            print("  [0] 退出")
            print()
            return input("请选择 [0-5]: ").strip()
    
    def run(self):
        """主程序"""
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                self.ytdlp_menu()
            elif choice == "2":
                self.wget_menu()
            elif choice == "3":
                self.curl_menu()
            elif choice == "4":
                self.show_history()
            elif choice == "5":
                self.change_path()
            elif choice == "0":
                if HAS_RICH:
                    console.clear()
                    console.print(Panel(
                        "[bold yellow]👋 再见！[/bold yellow]",
                        border_style="red"
                    ))
                else:
                    print("\n👋 再见！")
                break

if __name__ == "__main__":
    toolbox = DownloadToolbox()
    toolbox.run()