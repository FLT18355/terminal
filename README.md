# FLT18355 - Terminal Config

**仓库版本 / Repo Version:** `1.2.1`

---

## 📖 简介 / Introduction

我的个人 **dotfiles** 仓库，所有配置统一使用 Catppuccin Mocha 主题，涵盖 Arch Linux (NyarchOS)、Debian 和 Termux (Android) 三大平台。

My personal **dotfiles** repo, all themed with Catppuccin Mocha, covering Arch Linux (NyarchOS), Debian, and Termux (Android).

> ⚠️ 配置文件仅供参考，建议按需取用 / Configs are for reference only, cherry-pick what you need

```bash
git clone https://github.com/FLT18355/terminal.git
```

---

## 🗂️ 目录结构 / Directory Structure

```
terminal/
├── config/                    # 平台配置
│   ├── arch/                  # Arch Linux (NyarchOS)
│   │   ├── system/            # 系统级 (pacman mirror, os-release)
│   │   ├── home/              # 用户目录 dotfiles
│   │   ├── logos/             # 系统 Logo 图片
│   │   └── wallpaper/
│   ├── debian/                # Debian 配置
│   │   ├── etc/               # apt sources.list
│   │   ├── home/              # 用户 dotfiles (fish, btop, nvim…)
│   │   └── usr/               # 系统级主题
│   ├── notes/                 # 笔记 (Python 函数等)
│   ├── help/                  # LazyVim 安装指南
│   ├── scripts/               # 工具脚本
│   │   ├── mc/                # Minecraft CLI 工具
│   │   └── terminal/          # 终端小工具 (base64, 日历, 下载器…)
│   └── web/                   # Catppuccin JS 用户样式
├── nvim/                      # NeoVim 配置 (基于 LazyVim)
├── termux/                    # Termux (Android 终端)
├── assets/                    # 截图
├── images/                    # 壁纸 & ANSI 艺术
├── .bashrc                    # 根 bashrc (启动 x-cmd)
└── README.md
```

---

## 🚀 安装指南 / Setup

> 关于目录里面的setup.sh
> 目前只是个半成品，千万不要用 /
> Regarding the setup.sh file in the directory:
> It's currently only half-finished – do not use it under any circumstances.

### 方式一：直接使用 / Direct Use

```bash
git clone https://github.com/FLT18355/terminal.git ~/terminal
```

然后按需将配置链接到对应目录 / Then symlink configs as needed:

```bash
# NeoVim
ln -sf ~/terminal/nvim ~/.config/nvim

# Termux (on Android)
ln -sf ~/terminal/termux/.zshrc ~/.zshrc
ln -sf ~/terminal/termux/.tmux.conf ~/.tmux.conf
ln -sf ~/terminal/termux/termux.properties ~/.termux/termux.properties
```

### 方式二：Arch Linux (NyarchOS)

```bash
# 配置 arch 源
sudo cp ~/terminal/config/arch/system/etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist

# Fish shell
ln -sf ~/terminal/config/arch/home/.config/fish ~/.config/fish

# 其他工具
ln -sf ~/terminal/config/arch/home/.config/alacritty ~/.config/alacritty
ln -sf ~/terminal/config/arch/home/.config/polybar ~/.config/polybar
ln -sf ~/terminal/config/arch/home/.config/rofi ~/.config/rofi
ln -sf ~/terminal/config/arch/home/.config/yazi ~/.config/yazi
ln -sf ~/terminal/config/arch/home/.config/starship.toml ~/.config/starship.toml
ln -sf ~/terminal/config/arch/home/.config/kitty ~/.config/kitty
```

### 方式三：Debian

```bash
# APT 源 (testing 分支)
sudo cp ~/terminal/config/debian/etc/apt/sources.list /etc/apt/sources.list

# Fish shell
ln -sf ~/terminal/config/debian/home/.config/fish ~/.config/fish

# 其他工具
ln -sf ~/terminal/config/debian/home/.config/btop ~/.config/btop
ln -sf ~/terminal/config/debian/home/.config/nvim ~/.config/nvim
```

### 方式四：Termux (Android)

```bash
# Zsh + Oh My Zsh
ln -sf ~/terminal/termux/.zshrc ~/.zshrc

# Tmux
ln -sf ~/terminal/termux/.tmux.conf ~/.tmux.conf

# Termux 属性
cp ~/terminal/termux/termux.properties ~/.termux/termux.properties

# 颜色方案
cp ~/terminal/termux/colors.properties ~/.termux/colors.properties

# Alacritty
ln -sf ~/terminal/termux/.config/alacritty ~/.config/alacritty

# Fastfetch
ln -sf ~/terminal/termux/.config/fastfetch ~/.config/fastfetch

# Cava (音频可视化)
ln -sf ~/terminal/termux/.config/cava ~/.config/cava

# Yazi (文件管理器)
ln -sf ~/terminal/termux/.config/yazi ~/.config/yazi
```

---

## ✨ 主要特性 / Features

### 🅽 Neovim (LazyVim)

基于 **LazyVim** 启动模板构建。

| 插件 / Plugin | 用途 / Purpose |
|--------------|----------------|
| catppuccin | 色彩主题 |
| blink-cmp | 自动补全 |
| snacks.nvim | 启动页 + 增强功能 |
| render-markdown.nvim | Markdown 渲染 |
| highlight-colors.nvim | 颜色代码高亮 |
| mason.nvim | LSP/DAP/Linter 管理 |
| lualine | 状态栏 |

**快捷键 / Keymaps:**

| 按键 | 功能 |
|------|------|
| `<F2>` | 格式化 Python (ruff) |
| `<F9>` | 切换粘贴模式 |
| `<leader>w` | 保存文件 |
| `<leader>q` | 关闭窗口 |

### 🐟 Fish Shell

三大平台统一使用 Fish，带以下插件 / Unified Fish setup across all platforms:

- **fzf.fish** — 模糊搜索 (历史、文件、进程、Git)
- **autopair** — 自动括号补全
- **sponge** — 历史记录去重 / 过滤
- **puffer-fish** — `!!` `!$` 等 Bang 展开
- **abbr-tips** — 缩写提示
- **catppuccin-tide** — 主题化提示符

### 🎨 Catppuccin Mocha 主题覆盖 / Theme Coverage

| 类别 | 工具 |
|------|------|
| 编辑器 | NeoVim, LazyGit |
| Shell | Fish, Zsh, Bash |
| 终端 | Alacritty, Kitty, Konsole, XFCE4 Terminal |
| 文件管理 | Yazi, Ranger, nnn, Superfile |
| 系统监控 | Btop, Fastfetch, Neofetch, htop |
| 启动器 | Rofi |
| 面板 | Polybar |
| 音乐 | Cava (可视化), ncmpcpp, Audacious, Strawberry, go-musicfox |
| 窗口管理 | Openbox, i3, Niri, KDE Plasma, LXQt, XFCE4 |
| 合成器 | Picom |
| 其他 | Glow (Markdown), Eza (ls 替代), Starship |

### 🛠️ 工具脚本 / Utility Scripts

| 脚本 | 语言 | 用途 |
|------|------|------|
| `scripts/mc/MC_CLI.py` | Python | Minecraft CLI 工具 |
| `scripts/mc/music.py` | Python | Minecraft 相关音乐 |
| `scripts/terminal/base64_tool.py` | Python | Base64 编解码 |
| `scripts/terminal/7z.py` | Python | 7z 压缩工具 |
| `scripts/terminal/中国日历.py` | Python | 中国日历查询 |
| `scripts/terminal/yd下载器.py` | Python | 视频下载器 |
| `scripts/terminal/player.js` | Node.js | 终端音乐播放器 |
| `scripts/terminal/cbg.py` | Python | (自定义工具) |

---

## 📸 截图 / Screenshots

![](https://github.com/FLT18355/terminal/blob/main/assets/1.png?raw=true)
![](https://github.com/FLT18355/terminal/blob/main/assets/2.png?raw=true)
![](https://github.com/FLT18355/terminal/blob/main/assets/3.png?raw=true)

---

## 🔗 相关链接 / Links

- [Catppuccin](https://catppuccin.com) — 主题灵感 / Theme inspiration
- [LazyVim](https://www.lazyvim.org) — NeoVim 配置框架
- [Termux](https://termux.dev) — Android 终端模拟器

## 📱 正在使用的应用 / Apps in Use

| 应用 | 用途 |
|------|------|
| Obsidian | 笔记 / Notes |
| Konsole | KDE 终端 |
| Kitty | GPU 加速终端 |
| ZeroTermux | Android Termux 增强版 |
| QQ | 通讯 / Messaging |
| mpv | 视频播放 / Media player |

---

## 🙏 致谢 / Credits

- [Catppuccin](https://github.com/catppuccin) — 惊艳的色彩方案
- [LazyVim](https://github.com/LazyVim/LazyVim) — NeoVim 配置框架
- [oh-my-zsh](https://ohmyz.sh) — Zsh 框架
- 所有开源工具的维护者们 / All open-source tool maintainers
