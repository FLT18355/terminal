#!/usr/bin/env python3
"""
7zip 压缩/解压工具 - Catppuccin Mocha 配色版
支持：压缩、解压、分卷、加密、列表查看、测试、批量处理
"""

import subprocess
import sys
import os
import json
import time
import shutil
from pathlib import Path
from datetime import datetime

# ========== Catppuccin Mocha 配色 ==========
COLORS = {
    "bg": "\033[48;2;30;30;46m",
    "fg": "\033[38;2;205;214;244m",
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    
    "rosewater": "\033[38;2;245;224;220m",
    "flamingo": "\033[38;2;242;205;205m",
    "pink": "\033[38;2;245;194;231m",
    "mauve": "\033[38;2;203;166;247m",
    "red": "\033[38;2;243;139;168m",
    "maroon": "\033[38;2;235;160;172m",
    "peach": "\033[38;2;250;179;135m",
    "yellow": "\033[38;2;249;226;175m",
    "green": "\033[38;2;166;227;161m",
    "teal": "\033[38;2;148;226;213m",
    "blue": "\033[38;2;137;180;250m",
    "sky": "\033[38;2;137;220;235m",
    "lavender": "\033[38;2;180;190;254m",
}

def c(text, color="fg", bold=False):
    """彩色输出"""
    style = COLORS.get(color, COLORS["fg"])
    if bold:
        style += COLORS["bold"]
    return f"{style}{text}{COLORS['reset']}"

def print_header(title):
    """打印标题"""
    print()
    print(c("═" * 60, "blue", bold=True))
    print(c(f"  {title}", "mauve", bold=True))
    print(c("═" * 60, "blue", bold=True))
    print()

def print_success(msg):
    print(c("✓ ", "green") + c(msg, "fg"))

def print_error(msg):
    print(c("✗ ", "red") + c(msg, "fg"))

def print_info(msg):
    print(c("ℹ ", "blue") + c(msg, "fg"))

def print_warning(msg):
    print(c("⚠ ", "yellow") + c(msg, "fg"))

# ========== 配置文件 ==========
CONFIG_FILE = Path.home() / ".7z_config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"last_output": "", "default_level": 9, "default_format": "7z"}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def find_7z():
    """查找 7z 可执行文件"""
    for cmd in ['7zz', '7z']:
        if shutil.which(cmd):
            return cmd
    return None

def get_size_str(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f} 秒"
    elif seconds < 3600:
        return f"{seconds/60:.1f} 分钟"
    else:
        return f"{seconds/3600:.1f} 小时"

def list_archive(archive, password=None):
    """列出压缩包内容"""
    seven_zip = find_7z()
    if not seven_zip:
        print_error("未找到 7z")
        return False
    
    archive = expand_path(archive)
    
    if not os.path.exists(archive):
        print_error(f"文件不存在: {archive}")
        return False
    
    print_header(f"📋 压缩包内容: {Path(archive).name}")
    
    cmd = [seven_zip, 'l', archive]
    if password:
        cmd.extend(['-p' + password])
    
    try:
        subprocess.run(cmd)
        return True
    except Exception as e:
        print_error(str(e))
        return False

def expand_path(path):
    """展开 ~ 为用户家目录"""
    if path is None:
        return None
    if isinstance(path, str) and path.startswith('~'):
        return str(Path.home()) + path[1:]
    return path

def test_archive(archive, password=None):
    seven_zip = find_7z()
    if not seven_zip:
        print_error("未找到 7z，请安装：pkg install p7zip 或 pkg install 7zip")
        return False
    
    cmd = [seven_zip, 't', archive]
    if password:
        cmd.extend(['-p' + password])
    
    print_header(f"🔍 测试压缩包: {Path(archive).name}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print_success("压缩包完整，无损坏")
            return True
        else:
            print_error("压缩包已损坏")
            print(result.stderr)
            return False
    except Exception as e:
        print_error(str(e))
        return False

def compress(source, output=None, password=None, level=9, 
             fmt='7z', split=None, encrypt_header=False, 
             include_hidden=False, exclude=None, compression_method='lzma2'):
    seven_zip = find_7z()
    if not seven_zip:
        print_error("未找到 7z，请安装：pkg install p7zip 或 pkg install 7zip")
        return False
    
    source_path = Path(source)
    if not source_path.exists():
        print_error(f"文件不存在: {source}")
        return False
    
    if not output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"{source_path.name}_{timestamp}.{fmt}"
    
    cmd = [seven_zip, 'a', f'-t{fmt}', f'-mx={level}', f'-mmt=on', output]
    
    if compression_method:
        cmd.append(f'-mm={compression_method}')
    
    if encrypt_header and fmt == '7z' and password:
        cmd.append('-mhe=on')
    
    if password:
        cmd.append(f'-p{password}')
    
    if split:
        cmd.append(f'-v{split}')
    
    if exclude:
        for pattern in exclude:
            cmd.append(f'-xr!{pattern}')
    
    if include_hidden:
        cmd.append('-xr!.*')
    
    cmd.append(str(source_path))
    
    print_header("📦 压缩操作")
    print(f"  {c('源文件:', 'teal')} {source_path}")
    print(f"  {c('输出:', 'teal')} {output}")
    print(f"  {c('格式:', 'teal')} {fmt.upper()}")
    print(f"  {c('等级:', 'teal')} {level}")
    print(f"  {c('算法:', 'teal')} {compression_method}")
    if password:
        print(f"  {c('密码:', 'teal')} {c('*' * len(password), 'yellow')}")
    if split:
        print(f"  {c('分卷:', 'teal')} {split}")
    if encrypt_header:
        print(f"  {c('文件名加密:', 'teal')} {c('开启', 'green')}")
    print()
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print_success(f"压缩成功！({format_time(elapsed)})")
            
            if os.path.exists(output):
                size = os.path.getsize(output)
                print(f"  {c('大小:', 'teal')} {c(get_size_str(size), 'green')}")
            
            if source_path.is_file():
                original_size = source_path.stat().st_size
                if original_size > 0:
                    ratio = (1 - size / original_size) * 100
                    print(f"  {c('压缩率:', 'teal')} {c(f'{ratio:.1f}%', 'mauve')}")
            
            return True
        else:
            print_error(f"压缩失败: {result.stderr}")
            return False
    except Exception as e:
        print_error(str(e))
        return False

def decompress(archive, output_dir=None, password=None, overwrite=False):
    seven_zip = find_7z()
    if not seven_zip:
        print_error("未找到 7z")
        return False
    
    if not os.path.exists(archive):
        print_error(f"文件不存在: {archive}")
        return False
    
    if not output_dir:
        output_dir = os.path.splitext(archive)[0]
    
    cmd = [seven_zip, 'x', archive, f'-o{output_dir}', '-y' if overwrite else '-aoa']
    
    if password:
        cmd.append(f'-p{password}')
    
    print_header("📂 解压操作")
    print(f"  {c('源文件:', 'teal')} {archive}")
    print(f"  {c('输出:', 'teal')} {output_dir}")
    if password:
        print(f"  {c('密码:', 'teal')} {c('*' * len(password), 'yellow')}")
    print()
    
    start_time = time.time()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        elapsed = time.time() - start_time
        
        if result.returncode == 0:
            print_success(f"解压成功！({format_time(elapsed)})")
            return True
        else:
            print_error(f"解压失败: {result.stderr}")
            return False
    except Exception as e:
        print_error(str(e))
        return False

def batch_compress(sources, output_dir=None, **kwargs):
    if not output_dir:
        output_dir = os.getcwd()
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print_header(f"📦 批量压缩 ({len(sources)} 个文件)")
    
    success_count = 0
    for i, source in enumerate(sources, 1):
        print(f"\n  [{i}/{len(sources)}] {Path(source).name}")
        output = Path(output_dir) / f"{Path(source).name}.7z"
        if compress(source, str(output), **kwargs):
            success_count += 1
    
    print()
    if success_count == len(sources):
        print_success(f"批量压缩完成: {success_count}/{len(sources)} 成功")
    else:
        print_warning(f"批量压缩完成: {success_count}/{len(sources)} 成功，{len(sources)-success_count} 失败")
    
    return success_count == len(sources)

def interactive_mode():
    seven_zip = find_7z()
    if not seven_zip:
        print_error("请先安装 7z: pkg install p7zip")
        return
    
    config = load_config()
    
    while True:
        print_header("7zip 压缩/解压工具")
        print()
        print(f"  {c('1', 'blue')}  压缩文件/目录")
        print(f"  {c('2', 'blue')}  批量压缩")
        print(f"  {c('3', 'blue')}  分卷压缩")
        print()
        print(f"  {c('4', 'green')}  解压文件")
        print(f"  {c('5', 'green')}  批量解压")
        print()
        print(f"  {c('6', 'yellow')}  查看压缩包内容")
        print(f"  {c('7', 'yellow')}  测试压缩包完整性")
        print()
        print(f"  {c('8', 'mauve')}  设置")
        print(f"  {c('9', 'red')}  退出")
        print()
        
        choice = input(f"{c('请选择', 'teal')} (1-9): ").strip()
        
        if choice == '1':
            source = input(f"{c('源文件/目录', 'teal')}: ").strip()
            if not source:
                continue
            output = input(f"{c('输出文件名', 'teal')} ({c('留空自动', 'dim')}): ").strip() or None
            password = input(f"{c('密码', 'teal')} ({c('留空无密码', 'dim')}): ").strip() or None
            level = input(f"{c('压缩等级', 'teal')} 0-9 ({c(config['default_level'], 'green')}): ").strip()
            level = int(level) if level else config['default_level']
            fmt = input(f"{c('格式', 'teal')} 7z/zip/tar ({c('7z', 'green')}): ").strip() or '7z'
            compress(source, output, password, level, fmt)
            
        elif choice == '2':
            sources = input(f"{c('文件列表', 'teal')} ({c('用空格分隔', 'dim')}): ").strip().split()
            if not sources:
                continue
            output_dir = input(f"{c('输出目录', 'teal')} ({c('留空当前目录', 'dim')}): ").strip() or None
            password = input(f"{c('密码', 'teal')} ({c('留空无密码', 'dim')}): ").strip() or None
            level = input(f"{c('压缩等级', 'teal')} 0-9 ({c(config['default_level'], 'green')}): ").strip()
            level = int(level) if level else config['default_level']
            batch_compress(sources, output_dir, password=password, level=level, fmt='7z')
            
        elif choice == '3':
            source = input(f"{c('源文件/目录', 'teal')}: ").strip()
            if not source:
                continue
            split = input(f"{c('分卷大小', 'teal')} ({c('如 100M, 1G', 'dim')}): ").strip()
            if not split:
                continue
            output = input(f"{c('输出文件名前缀', 'teal')} ({c('留空自动', 'dim')}): ").strip() or None
            password = input(f"{c('密码', 'teal')} ({c('留空无密码', 'dim')}): ").strip() or None
            compress(source, output, password, split=split)
            
        elif choice == '4':
            archive = input(f"{c('压缩文件', 'teal')}: ").strip()
            if not archive:
                continue
            output_dir = input(f"{c('输出目录', 'teal')} ({c('留空自动', 'dim')}): ").strip() or None
            password = input(f"{c('密码', 'teal')} ({c('留空无密码', 'dim')}): ").strip() or None
            decompress(archive, output_dir, password)
            
        elif choice == '5':
            archives = input(f"{c('文件列表', 'teal')} ({c('用空格分隔', 'dim')}): ").strip().split()
            if not archives:
                continue
            output_dir = input(f"{c('输出目录', 'teal')} ({c('留空当前目录', 'dim')}): ").strip() or None
            for archive in archives:
                decompress(archive, output_dir)
                
        elif choice == '6':
            archive = input(f"{c('压缩文件', 'teal')}: ").strip()
            if not archive:
                continue
            password = input(f"{c('密码', 'teal')} ({c('留空无密码', 'dim')}): ").strip() or None
            list_archive(archive, password)
            
        elif choice == '7':
            archive = input(f"{c('压缩文件', 'teal')}: ").strip()
            if not archive:
                continue
            password = input(f"{c('密码', 'teal')} ({c('留空无密码', 'dim')}): ").strip() or None
            test_archive(archive, password)
            
        elif choice == '8':
            print_header("⚙️ 设置")
            level = input(f"  默认压缩等级 ({c(config['default_level'], 'green')}): ").strip()
            if level:
                config['default_level'] = int(level)
            fmt = input(f"  默认格式 ({c(config.get('default_format', '7z'), 'green')}): ").strip()
            if fmt:
                config['default_format'] = fmt
            save_config(config)
            print_success("设置已保存")
            
        elif choice == '9':
            print()
            print_success("再见！👋")
            break
        
        input(f"\n{c('按 Enter 继续...', 'dim')}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='7zip 压缩/解压工具 - Catppuccin 配色版')
    parser.add_argument('-c', '--compress', help='压缩文件或目录')
    parser.add_argument('-x', '--extract', help='解压文件')
    parser.add_argument('-o', '--output', help='输出文件名')
    parser.add_argument('-p', '--password', help='密码')
    parser.add_argument('-l', '--level', type=int, default=9, help='压缩等级 0-9')
    parser.add_argument('-f', '--format', default='7z', help='格式: 7z, zip, tar, gz, xz, bz2')
    parser.add_argument('-s', '--split', help='分卷大小 (如 100M, 1G)')
    parser.add_argument('-e', '--encrypt-header', action='store_true', help='加密文件名')
    parser.add_argument('-L', '--list', help='列出压缩包内容')
    parser.add_argument('-t', '--test', help='测试压缩包完整性')
    parser.add_argument('-b', '--batch', nargs='+', help='批量压缩多个文件')
    parser.add_argument('--exclude', nargs='+', help='排除模式')
    parser.add_argument('--method', default='lzma2', help='压缩算法')
    
    args = parser.parse_args()
    
    if args.list:
        list_archive(args.list, args.password)
    elif args.test:
        test_archive(args.test, args.password)
    elif args.batch:
        batch_compress(args.batch, args.output, password=args.password, level=args.level)
    elif args.compress:
        compress(args.compress, args.output, args.password, args.level, 
                 args.format, args.split, args.encrypt_header, 
                 False, args.exclude, args.method)
    elif args.extract:
        decompress(args.extract, args.output, args.password)
    else:
        interactive_mode()

if __name__ == '__main__':
    main()