#!/usr/bin/env python3
"""
Base64 编解码工具 - Catppuccin Mocha 配色
"""

import base64
import sys
import argparse
from pathlib import Path

# Catppuccin Mocha 配色 ANSI
COLORS = {
    "bg": "\033[48;2;30;30;46m",
    "fg": "\033[38;2;205;214;244m",
    "blue": "\033[38;2;137;180;250m",
    "green": "\033[38;2;166;227;161m",
    "red": "\033[38;2;243;139;168m",
    "yellow": "\033[38;2;249;226;175m",
    "mauve": "\033[38;2;203;166;247m",
    "teal": "\033[38;2;148;226;213m",
    "peach": "\033[38;2;250;179;135m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}

def print_header(title):
    """打印标题"""
    print()
    print(f"{COLORS['blue']}{COLORS['bold']}{'='*60}{COLORS['reset']}")
    print(f"{COLORS['mauve']}{COLORS['bold']}{title:^60}{COLORS['reset']}")
    print(f"{COLORS['blue']}{'='*60}{COLORS['reset']}")
    print()

def print_result(title, content, color="green"):
    """打印结果"""
    print(f"{COLORS[color]}{COLORS['bold']}{title}:{COLORS['reset']}")
    print(f"{COLORS['teal']}{'-'*40}{COLORS['reset']}")
    print(f"{COLORS['fg']}{content}{COLORS['reset']}")
    print(f"{COLORS['teal']}{'-'*40}{COLORS['reset']}")
    print()

def encode_text(text):
    """文本转 Base64"""
    if isinstance(text, str):
        text_bytes = text.encode('utf-8')
    else:
        text_bytes = text
    return base64.b64encode(text_bytes).decode('utf-8')

def decode_text(base64_str):
    """Base64 转文本"""
    try:
        decoded_bytes = base64.b64decode(base64_str)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"{COLORS['red']}解码失败: {e}{COLORS['reset']}"

def encode_file(file_path):
    """文件转 Base64"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        return f"{COLORS['red']}读取文件失败: {e}{COLORS['reset']}"

def decode_to_file(base64_str, output_path):
    """Base64 转文件"""
    try:
        data = base64.b64decode(base64_str)
        with open(output_path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"{COLORS['red']}写入文件失败: {e}{COLORS['reset']}")
        return False

def interactive_mode():
    """交互模式"""
    print_header("🐱 Base64 编解码工具 - Catppuccin Mocha")
    
    while True:
        print(f"{COLORS['yellow']}请选择操作:{COLORS['reset']}")
        print(f"  {COLORS['blue']}1{COLORS['reset']}. 文本 → Base64")
        print(f"  {COLORS['blue']}2{COLORS['reset']}. Base64 → 文本")
        print(f"  {COLORS['blue']}3{COLORS['reset']}. 文件 → Base64")
        print(f"  {COLORS['blue']}4{COLORS['reset']}. Base64 → 文件")
        print(f"  {COLORS['blue']}5{COLORS['reset']}. 清屏")
        print(f"  {COLORS['blue']}6{COLORS['reset']}. 退出")
        print()
        
        choice = input(f"{COLORS['peach']}选择 (1-6): {COLORS['reset']}").strip()
        
        if choice == '1':
            text = input(f"{COLORS['green']}输入文本: {COLORS['reset']}")
            if text:
                result = encode_text(text)
                print_result("Base64 结果", result, "green")
        
        elif choice == '2':
            b64 = input(f"{COLORS['green']}输入 Base64: {COLORS['reset']}")
            if b64:
                result = decode_text(b64)
                print_result("解码结果", result, "mauve")
        
        elif choice == '3':
            path = input(f"{COLORS['green']}输入文件路径: {COLORS['reset']}")
            if path and Path(path).exists():
                result = encode_file(path)
                print_result("文件 Base64", result[:200] + ("..." if len(result) > 200 else ""), "green")
                print(f"{COLORS['yellow']}完整结果已保存到剪贴板? 需要时复制即可{COLORS['reset']}")
            else:
                print(f"{COLORS['red']}文件不存在{COLORS['reset']}")
        
        elif choice == '4':
            b64 = input(f"{COLORS['green']}输入 Base64: {COLORS['reset']}")
            if b64:
                output = input(f"{COLORS['green']}输出文件路径: {COLORS['reset']}")
                if output:
                    if decode_to_file(b64, output):
                        print(f"{COLORS['green']}✅ 文件已保存: {output}{COLORS['reset']}")
        
        elif choice == '5':
            print("\033[2J\033[H")
            print_header("🐱 Base64 编解码工具 - Catppuccin Mocha")
        
        elif choice == '6':
            print(f"{COLORS['green']}👋 再见！{COLORS['reset']}")
            break
        
        else:
            print(f"{COLORS['red']}无效选择{COLORS['reset']}")
        
        print()

def main():
    parser = argparse.ArgumentParser(description="Base64 编解码工具 - Catppuccin Mocha")
    parser.add_argument("-e", "--encode", help="编码文本为 Base64")
    parser.add_argument("-d", "--decode", help="解码 Base64 为文本")
    parser.add_argument("-ef", "--encode-file", help="编码文件为 Base64")
    parser.add_argument("-df", "--decode-file", help="解码 Base64 到文件", nargs=2, metavar=('BASE64', 'OUTPUT'))
    parser.add_argument("-i", "--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_mode()
    elif args.encode:
        result = encode_text(args.encode)
        print(result)
    elif args.decode:
        result = decode_text(args.decode)
        print(result)
    elif args.encode_file:
        result = encode_file(args.encode_file)
        print(result)
    elif args.decode_file:
        b64_str, output = args.decode_file
        if decode_to_file(b64_str, output):
            print(f"✅ 文件已保存: {output}")
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
