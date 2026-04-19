#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Catppuccin Mocha 配色表 - 终端显示工具
用法: python3 catppuccin_palette.py
"""

# Catppuccin Mocha 配色表 (HEX 和 RGB)
COLORS = {
    # 背景色系
    "base":    {"hex": "#1e1e2e", "rgb": (30, 30, 46)},
    "mantle":  {"hex": "#181825", "rgb": (24, 24, 37)},
    "crust":   {"hex": "#11111b", "rgb": (17, 17, 27)},
    # 文字色系
    "text":    {"hex": "#cdd6f4", "rgb": (205, 214, 244)},
    "subtext0":{"hex": "#a6adc8", "rgb": (166, 173, 200)},
    "subtext1":{"hex": "#bac2de", "rgb": (186, 194, 222)},
    # 覆盖层/边框
    "overlay0":{"hex": "#6c7086", "rgb": (108, 112, 134)},
    "overlay1":{"hex": "#7f849c", "rgb": (127, 132, 156)},
    "overlay2":{"hex": "#9399b2", "rgb": (147, 153, 178)},
    # 表面色
    "surface0":{"hex": "#313244", "rgb": (49, 50, 68)},
    "surface1":{"hex": "#45475a", "rgb": (69, 71, 90)},
    "surface2":{"hex": "#585b70", "rgb": (88, 91, 112)},
    # 强调色
    "rosewater":{"hex": "#f5e0dc", "rgb": (245, 224, 220)},
    "flamingo": {"hex": "#f2cdcd", "rgb": (242, 205, 205)},
    "pink":     {"hex": "#f5c2e7", "rgb": (245, 194, 231)},
    "mauve":    {"hex": "#cba6f7", "rgb": (203, 166, 247)},
    "red":      {"hex": "#f38ba8", "rgb": (243, 139, 168)},
    "maroon":   {"hex": "#eba0ac", "rgb": (235, 160, 172)},
    "peach":    {"hex": "#fab387", "rgb": (250, 179, 135)},
    "yellow":   {"hex": "#f9e2af", "rgb": (249, 226, 175)},
    "green":    {"hex": "#a6e3a1", "rgb": (166, 227, 161)},
    "teal":     {"hex": "#94e2d5", "rgb": (148, 226, 213)},
    "sky":      {"hex": "#89dceb", "rgb": (137, 220, 235)},
    "blue":     {"hex": "#89b4fa", "rgb": (137, 180, 250)},
    "lavender": {"hex": "#b4befe", "rgb": (180, 190, 254)},
}

def rgb_to_ansi(r, g, b):
    """将 RGB 转换为 ANSI 256 色近似码"""
    # 简化版：返回 24 位真彩色转义序列
    return f"\033[38;2;{r};{g};{b}m"

def bg_rgb_to_ansi(r, g, b):
    """将 RGB 转换为背景色 ANSI 转义序列"""
    return f"\033[48;2;{r};{g};{b}m"

def print_color_block(color_name, hex_code, rgb):
    """打印单个颜色块（前景色示例）"""
    ansi_fg = rgb_to_ansi(*rgb)
    print(f"{ansi_fg}{color_name:12} {hex_code:8} {rgb}  ██████████\033[0m")

def print_bg_block(color_name, hex_code, rgb):
    """打印单个背景色块"""
    ansi_bg = bg_rgb_to_ansi(*rgb)
    # 根据背景亮度自动选择前景文字颜色
    brightness = (rgb[0] * 299 + rgb[1] * 587 + rgb[2] * 114) / 1000
    fg_color = "\033[38;2;205;214;244m" if brightness < 130 else "\033[38;2;30;30;46m"
    print(f"{fg_color}{ansi_bg}{color_name:12} {hex_code:8} {rgb}  ██████████\033[0m")

def print_header():
    """打印标题头"""
    print("\n" + "=" * 60)
    print("🐱  Catppuccin Mocha 配色表")
    print("=" * 60)

def print_section(title):
    """打印分类标题"""
    print(f"\n✨ {title}")
    print("-" * 50)

def main():
    print_header()
    
    # 背景色系
    print_section("背景色系 (Background)")
    bg_colors = ["base", "mantle", "crust"]
    for name in bg_colors:
        c = COLORS[name]
        print_bg_block(name, c["hex"], c["rgb"])
    
    # 表面色系
    print_section("表面色系 (Surface)")
    surface_colors = ["surface0", "surface1", "surface2"]
    for name in surface_colors:
        c = COLORS[name]
        print_bg_block(name, c["hex"], c["rgb"])
    
    # 文字色系
    print_section("文字色系 (Text)")
    text_colors = ["text", "subtext0", "subtext1"]
    for name in text_colors:
        c = COLORS[name]
        print_color_block(name, c["hex"], c["rgb"])
    
    # 覆盖层/边框
    print_section("覆盖层/边框 (Overlay)")
    overlay_colors = ["overlay0", "overlay1", "overlay2"]
    for name in overlay_colors:
        c = COLORS[name]
        print_bg_block(name, c["hex"], c["rgb"])
    
    # 强调色系
    print_section("强调色系 (Accent)")
    accent_colors = [
        "rosewater", "flamingo", "pink", "mauve",
        "red", "maroon", "peach", "yellow",
        "green", "teal", "sky", "blue", "lavender"
    ]
    for name in accent_colors:
        c = COLORS[name]
        print_color_block(name, c["hex"], c["rgb"])
    
    print("\n" + "=" * 60)
    print("💡 提示：你的终端需要支持真彩色 (True Color) 才能正确显示")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()