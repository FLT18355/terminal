from PIL import Image

# 定义颜色 (十六进制转RGB)
color_hex = "#1e1e2e"
color_rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

# 创建一张 1920x1080 的纯色图片
width, height = 1920, 1080
img = Image.new("RGB", (width, height), color_rgb)

# 保存为 PNG
img.save("catppuccin_mocha_bg.png")
print(f"图片已保存为 catppuccin_mocha_bg.png，颜色为 {color_hex}")
