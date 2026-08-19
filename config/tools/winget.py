#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# winget - Windows Package Manager (Linux backend: pacman)

import os
import shutil
import subprocess
import sys

VERSION = "1.12.30"
BACKEND = "pacman"

ANSI = sys.stdout.isatty()

def esc(code):
    return f"\033[{code}m" if ANSI else ""

RED   = esc("0;31m")
GREEN = esc("0;33m")
YELLOW = esc("0;33m")
NC    = esc("0m")

def is_root():
    return os.geteuid() == 0

def sudo_cmd():
    if is_root():
        return []
    if shutil.which("sudo"):
        return ["sudo"]
    return []

# ---------- arg helpers ----------
def extract_packages(args):
    """Skip --xxx options, keep the rest as package names."""
    return [a for a in args if not a.startswith("-")]

def require_packages(pkgs, what):
    if not pkgs:
        print(f"{RED}错误: 未指定要{what}的软件包.{NC}", file=sys.stderr)
        return False
    return True

def has_flag(args, *flags):
    return any(f in args for f in flags)

def run(cmd):
    try:
        return subprocess.run(cmd).returncode
    except FileNotFoundError:
        print(f"{RED}错误: 未找到命令 '{cmd[0] if cmd else ''}'.{NC}", file=sys.stderr)
        return 127

# ---------- help ----------
def show_help():
    print(f"""\
Windows 程序包管理器 {VERSION}
版权所有 (c) Microsoft Corporation。保留所有权利。

Winget 命令:
  install    安装给定的软件包 (或本地 .pkg.tar 文件)
  uninstall  卸载给定的软件包
  search     在软件仓库中搜索软件包
  list       列出已安装的软件包
  upgrade    升级给定的软件包，使用 --all 升级全部
  show       显示软件包信息
  files      列出软件包拥有的文件
  owns       显示哪个已安装软件包拥有某个文件
  changelog  查看软件包的更新日志
  check      校验已安装软件包的文件
  database   管理软件包数据库 (使用 --check)
  clean      清理缓存中的旧软件包
  groups     列出可用的软件包组
  refresh    下载最新的软件包数据库
  deptest    测试软件包是否满足依赖
  info       显示应用程序元数据
  help       打开帮助菜单
  version    显示 winget 的版本
  --version  显示 winget 的版本
  --info     显示应用程序元数据

List 选项:
  --deps          显示作为依赖安装的软件包 (-Qd)
  --explicit      显示显式安装的软件包 (-Qe)
  --foreign       显示不在同步数据库中的软件包 (-Qm)
  --native        显示在同步数据库中的软件包 (-Qn)
  --unrequired    显示不被其他软件包依赖的软件包 (-Qt)

选项:
  -v, --version       显示 winget 的版本
  -h, --help          显示帮助菜单

高级:
  winget pacman <pacman 参数...>   直接透传给原生 pacman

如需更详细的信息，请运行 'winget help <命令>'。""")

# ---------- install (package or local file) ----------
def do_install(pkgs):
    if not require_packages(pkgs, "安装"):
        return 1
    # local package files (.pkg.tar*) -> pacman -U
    if any(p.endswith((".pkg.tar", ".pkg.tar.zst", ".pkg.tar.xz", ".pkg.tar.gz")) for p in pkgs):
        cmd = sudo_cmd() + ["pacman", "-U", "--noconfirm"] + pkgs
    else:
        print("找到与请求匹配的软件包: %s" % ", ".join(pkgs))
        print("")
        cmd = sudo_cmd() + ["pacman", "-S", "--noconfirm"] + pkgs
    return run(cmd)

# ---------- uninstall ----------
def do_uninstall(pkgs):
    if not require_packages(pkgs, "卸载"):
        return 1
    cmd = sudo_cmd() + ["pacman", "-Rns", "--noconfirm"] + pkgs
    return run(cmd)

# ---------- search ----------
def do_search(args):
    pkgs = extract_packages(args)
    if not require_packages(pkgs, "搜索"):
        return 1
    if has_flag(args, "--installed", "-l"):
        cmd = ["pacman", "-Qs"] + pkgs      # search installed only
    else:
        cmd = ["pacman", "-Ss"] + pkgs      # search repositories
    return run(cmd)

# ---------- list ----------
def do_list(args):
    # --upgrades / -u
    if has_flag(args, "-u", "--upgrades"):
        return run(["pacman", "-Qu"])
    filters = {
        "--deps":        "d",
        "--explicit":    "e",
        "--foreign":     "m",
        "--native":      "n",
        "--unrequired":  "t",
    }
    extra = [f for flag, f in filters.items() if flag in args]
    if extra:
        return run(["pacman", "-Q" + "".join(extra)])
    return run(["pacman", "-Q"])

# ---------- upgrade ----------
def do_upgrade(args):
    pkgs = extract_packages(args)
    if has_flag(args, "--all", "-a", "--latest", "-L"):
        cmd = sudo_cmd() + ["pacman", "-Syu", "--noconfirm"]
        return run(cmd)
    if pkgs:
        cmd = sudo_cmd() + ["pacman", "-S", "--noconfirm"] + pkgs
        return run(cmd)
    return run(["pacman", "-Qu"])   # no args: list upgradable

# ---------- show ----------
def do_show(args):
    pkgs = extract_packages(args)
    if not require_packages(pkgs, "显示"):
        return 1
    if has_flag(args, "--local", "-l"):
        cmd = ["pacman", "-Qi"] + pkgs      # info from local database
    else:
        cmd = ["pacman", "-Si"] + pkgs      # info from sync database
    return run(cmd)

# ---------- files: list files owned by a package ----------
def do_files(pkgs):
    if not require_packages(pkgs, "列出文件"):
        return 1
    return run(["pacman", "-Ql"] + pkgs)

# ---------- owns: which package owns a file ----------
def do_owns(pkgs):
    if not require_packages(pkgs, "查询"):
        return 1
    return run(["pacman", "-Qo"] + pkgs)

# ---------- changelog ----------
def do_changelog(pkgs):
    if not require_packages(pkgs, "查看日志"):
        return 1
    return run(["pacman", "-Qc"] + pkgs)

# ---------- check: verify package files ----------
def do_check(args):
    pkgs = extract_packages(args)
    cmd = ["pacman", "-Qk"]
    if has_flag(args, "--files", "-f"):       # check file attributes too
        cmd = ["pacman", "-Qkk"]
    if has_flag(args, "--all", "-a"):
        cmd += ["*"]
    elif pkgs:
        cmd += pkgs
    return run(cmd)

# ---------- database ----------
def do_database(args):
    if has_flag(args, "--check", "-k"):
        cmd = ["pacman", "-Dk"]
        if has_flag(args, "--sync", "-s"):
            cmd = ["pacman", "-Dkk"]          # also check sync db
        return run(cmd)
    # mark packages explicit / asdeps
    pkgs = extract_packages(args)
    if not require_packages(pkgs, "标记"):
        return 1
    if has_flag(args, "--asdeps"):
        cmd = sudo_cmd() + ["pacman", "-D", "--asdeps"] + pkgs
    elif has_flag(args, "--asexplicit"):
        cmd = sudo_cmd() + ["pacman", "-D", "--asexplicit"] + pkgs
    else:
        print(f"{RED}错误: 请使用 --check、--asdeps 或 --asexplicit.{NC}", file=sys.stderr)
        return 1
    return run(cmd)

# ---------- clean: remove old package cache ----------
def do_clean(args):
    cmd = sudo_cmd() + ["pacman", "-Sc"]
    if has_flag(args, "--all", "-a"):
        cmd = sudo_cmd() + ["pacman", "-Scc"]  # remove every cached file
    return run(cmd)

# ---------- groups ----------
def do_groups():
    return run(["pacman", "-Sg"])

# ---------- refresh: download fresh package databases ----------
def do_refresh(args):
    cmd = sudo_cmd() + ["pacman", "-Sy"]
    if has_flag(args, "--force", "-f"):
        cmd = sudo_cmd() + ["pacman", "-Syy"]  # force refresh
    return run(cmd)

# ---------- deptest ----------
def do_deptest(pkgs):
    if not require_packages(pkgs, "测试"):
        return 1
    return run(["pacman", "-T"] + pkgs)

# ---------- version / info ----------
def do_version():
    print(f"v{VERSION}")
    return 0

def get_distro():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("PRETTY_NAME="):
                    return line.split("=", 1)[1].strip().strip('"')
    except OSError:
        pass
    if shutil.which("lsb_release"):
        try:
            out = subprocess.run(["lsb_release", "-ds"], capture_output=True, text=True).stdout.strip()
            if out:
                return out.strip('"')
        except OSError:
            pass
    return f"{os.uname().sysname} {os.uname().release}"

def do_info():
    distro = get_distro()
    arch = os.uname().machine
    print(f"""\
Windows 程序包管理器 v{VERSION}
版权所有 (c) Microsoft Corporation。保留所有权利。

系统信息:
  程序包管理器: Windows 程序包管理器
  源:          winget
  操作系统:    {distro}
  系统架构:    {arch}
  PowerShell:  7.4.5
  Windows:     10.0.19045
  类型:        1""")

# ---------- main ----------
def main(argv):
    if not argv:
        show_help()
        return 0

    cmd = argv[0]
    rest = argv[1:]

    # pacman escape hatch: winget pacman <anything...>
    if cmd == "pacman":
        return run(["pacman"] + rest)

    if cmd in ("-h", "--help", "help"):
        show_help()
    elif cmd in ("-v", "--version", "version"):
        return do_version()
    elif cmd in ("info", "--info"):
        return do_info()
    elif cmd == "install":
        return do_install(extract_packages(rest))
    elif cmd in ("uninstall", "remove"):
        return do_uninstall(extract_packages(rest))
    elif cmd == "search":
        return do_search(rest)
    elif cmd == "list":
        return do_list(rest)
    elif cmd == "upgrade":
        return do_upgrade(rest)
    elif cmd == "show":
        return do_show(rest)
    elif cmd == "files":
        return do_files(extract_packages(rest))
    elif cmd == "owns":
        return do_owns(extract_packages(rest))
    elif cmd == "changelog":
        return do_changelog(extract_packages(rest))
    elif cmd == "check":
        return do_check(rest)
    elif cmd == "database":
        return do_database(rest)
    elif cmd == "clean":
        return do_clean(rest)
    elif cmd == "groups":
        return do_groups()
    elif cmd == "refresh":
        return do_refresh(rest)
    elif cmd == "deptest":
        return do_deptest(extract_packages(rest))
    else:
        print(f"{RED}未知命令 '{cmd}'{NC}", file=sys.stderr)
        print("请使用 '--help' 选项查看可用命令。", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))