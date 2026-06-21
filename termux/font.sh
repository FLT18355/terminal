#!/bin/bash

# Maple Mono NF CN 字体安装脚本
# 适用于 Linux (包括 Termux proot 环境)

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检测系统架构
detect_arch() {
    ARCH=$(uname -m)
    case $ARCH in
        x86_64)
            echo "x86_64"
            ;;
        aarch64|arm64)
            echo "arm64"
            ;;
        armv7l|armhf)
            echo "armv7"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

# 获取最新的字体版本（从 GitHub 的 releases 或直接使用固定版本）
get_latest_version() {
    # 使用固定的稳定版本，避免 GitHub API 限制
    # 如果需要自动获取最新版本，可以用下面的 curl 命令
    # curl -s https://api.github.com/repos/ryanoasis/nerd-fonts/releases/latest | grep -Po '"tag_name": "\K[^"]*'
    echo "v3.2.1"  # 固定版本，你也可以换成最新的
}

# 创建字体目录
setup_font_dir() {
    FONT_DIR="$HOME/.local/share/fonts"
    if [ ! -d "$FONT_DIR" ]; then
        mkdir -p "$FONT_DIR"
        print_info "创建字体目录: $FONT_DIR"
    fi
}

# 下载字体
download_font() {
    local ARCH=$(detect_arch)
    local VERSION=$(get_latest_version)
    local FONT_NAME="MapleMono-NF-CN"
    local FONT_FILE="${FONT_NAME}.ttf"
    local FONT_URL="https://github.com/subframe7536/Maple-font/releases/download/${VERSION}/${FONT_NAME}.ttf"

    # 如果指定了架构特定的 URL，可以在这里修改
    # 目前 Maple Mono 的 Release 中，ttf 文件是架构无关的
    print_info "检测到架构: $ARCH"
    print_info "下载版本: $VERSION"
    print_info "字体文件: $FONT_FILE"
    print_info "下载 URL: $FONT_URL"

    # 下载字体
    cd "$FONT_DIR"
    if command -v curl &> /dev/null; then
        curl -L -o "$FONT_FILE" "$FONT_URL"
    elif command -v wget &> /dev/null; then
        wget -O "$FONT_FILE" "$FONT_URL"
    else
        print_error "未找到 curl 或 wget，请安装其中之一"
        exit 1
    fi

    if [ $? -eq 0 ]; then
        print_info "字体下载成功: $FONT_FILE"
    else
        print_error "字体下载失败，请检查网络连接或手动下载"
        exit 1
    fi
}

# 刷新字体缓存
refresh_font_cache() {
    print_info "刷新字体缓存..."
    if command -v fc-cache &> /dev/null; then
        fc-cache -fv
        print_info "字体缓存刷新完成"
    else
        print_warn "未找到 fc-cache 命令，请手动刷新字体缓存"
        print_warn "在 Termux 中，需要安装 fontconfig 包: pkg install fontconfig"
    fi
}

# 验证字体是否安装成功
verify_font() {
    print_info "验证字体是否安装成功..."
    if command -v fc-list &> /dev/null; then
        if fc-list | grep -i "MapleMono" &> /dev/null; then
            print_info "✅ Maple Mono NF CN 字体已成功安装！"
            print_info "字体路径: $(fc-list | grep -i 'MapleMono' | head -1)"
        else
            print_warn "⚠️ 未在字体列表中找到 Maple Mono，但文件已下载到 $FONT_DIR"
            print_warn "可以尝试重启终端或重新登录"
        fi
    else
        print_warn "未找到 fc-list 命令，无法验证字体安装"
    fi
}

# 显示使用说明
show_usage() {
    print_info "Maple Mono NF CN 字体安装完成！"
    echo ""
    echo "使用方法:"
    echo "1. 在终端中设置字体:"
    echo "   在 Termux 中，编辑 ~/.termux/termux.properties，添加:"
    echo "   font = $HOME/.local/share/fonts/MapleMono-NF-CN.ttf"
    echo ""
    echo "2. 在 VSCode 中设置:"
    echo "   'editor.fontFamily': 'Maple Mono NF CN, monospace'"
    echo ""
    echo "3. 在 Neovim 中设置:"
    echo "   set guifont=Maple\\ Mono\\ NF\\ CN:h12"
}

# 主函数
main() {
    print_info "开始安装 Maple Mono NF CN 字体..."
    echo ""

    setup_font_dir
    download_font
    refresh_font_cache
    verify_font
    echo ""
    show_usage
}

# 执行主函数
main