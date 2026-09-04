#!/usr/bin/env python3
"""日常维护：清理 npm/pip 缓存 + 更新系统包"""

import os
import shlex
import shutil
import subprocess
import sys

CLEAN_CMDS = [
    ("npm", "npm", "npm cache clean --force"),
    ("pip", "pip", "pip cache purge"),
]

UPDATE_CMD = "sudo pacman -Syyu"


def clean_cargo_cache():
    if not shutil.which("cargo"):
        print("[跳过] 未找到 cargo\n", flush=True)
        return 0
    cargo_dir = os.path.expanduser("~/.cargo/registry")
    if not os.path.isdir(cargo_dir):
        print("[跳过] cargo 缓存目录不存在\n", flush=True)
        return 0
    print(">> 清理 cargo 缓存", flush=True)
    for d in ["cache", "src"]:
        p = os.path.join(cargo_dir, d)
        if os.path.isdir(p):
            for item in os.listdir(p):
                shutil.rmtree(os.path.join(p, item), ignore_errors=True)
    print("   完成\n", flush=True)
    return 0


def run_tool(tool, cmd):
    if not shutil.which(tool):
        print(f"[跳过] 未找到 {tool}\n", flush=True)
        return 0
    print(f">> {cmd}", flush=True)
    proc = subprocess.run(shlex.split(cmd), stdin=subprocess.DEVNULL)
    print(f"   退出码: {proc.returncode}\n", flush=True)
    return proc.returncode


def run_interactive(cmd):
    print(f">> {cmd}\n", flush=True)
    return subprocess.run(shlex.split(cmd)).returncode


def main():
    failed = []
    for label, tool, cmd in CLEAN_CMDS:
        if run_tool(tool, cmd) != 0:
            failed.append(label)

    if clean_cargo_cache() != 0:
        failed.append("cargo")

    if sys.stdin.isatty():
        if run_interactive(UPDATE_CMD) != 0:
            failed.append("系统更新")
    else:
        print(f"[跳过] 非交互环境，无法更新。请手动执行: {UPDATE_CMD}")

    if failed:
        print(f"[失败] {', '.join(failed)}")
        return 1
    print("[完成] 全部成功")
    return 0


if __name__ == "__main__":
    sys.exit(main())