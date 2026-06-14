#!/usr/bin/env python3

from PIL import Image

# Catppuccin Mocha base 色
COLOR = "#1e1e2e"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_solid_image(width=1920, height=1080, output="solid.png"):
    """创建纯色图片"""
    rgb = hex_to_rgb(COLOR)
    img = Image.new('RGB', (width, height), rgb)
    img.save(output)
    print(f"✅ 已生成: {output}")
    print(f"   尺寸: {width}x{height}")
    print(f"   颜色: {COLOR}")

if __name__ == "__main__":
    # 默认 1920x1080
    create_solid_image()
    
    # 也可以自定义尺寸
    # create_solid_image(1080, 1920, "solid_phone.png")