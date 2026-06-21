#!/bin/bash
#
# install-maple-mono.sh - 为 Arch Linux 安装 Maple Mono NF CN 字体
# 
# 用法: ./install-maple-mono.sh
# 说白了就是下载个字体、扔对地方、刷新缓存，没了。
#
# 注意: 只适用于 Arch Linux，别的发行版不保证能用，
#       不过你要是在 termux-proot 里跑 Arch 容器，那也归它管。
# 
# 作者: FLT18355
# 日期: 2025-06-21

set -euo pipefail   # 遇错就停，变量没定义就报错，管道异常也报错

# ===== 颜色定义，让输出好看点 =====
# 不用也行，但有了更清楚
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${GREEN}[*]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[X]${NC} $1"; exit 1; }
ask()   { echo -e "${BLUE}[?]${NC} $1"; }

# ===== 检查是不是 Arch Linux =====
# 先看看 /etc/os-release 里写的啥，不是 Arch 就警告一下
if [ -f /etc/os-release ]; then
    . /etc/os-release
    if [[ "$ID" != "arch" ]]; then
        warn "当前系统是 $ID，不是 Arch Linux，但如果你在 proot 里跑 Arch 容器，那就无视这条。"
        ask "继续？(y/N)"
        read -r confirm
        [[ "$confirm" != "y" && "$confirm" != "Y" ]] && exit 0
    fi
else
    warn "找不到 /etc/os-release，跳过系统检查。"
fi

# ===== 检查必要的命令 =====
# curl 或 wget 至少得有一个，不然没法下载
if ! command -v curl &>/dev/null && ! command -v wget &>/dev/null; then
    error "curl 和 wget 都没装，选一个装上再跑。 pacman -S curl"
fi

# fc-cache 和 fc-list 来自 fontconfig，一般 Arch 都有，没有就装
if ! command -v fc-cache &>/dev/null; then
    warn "fc-cache 找不到，试试 pacman -S fontconfig"
fi

# ===== 去哪个仓库下载 =====
# Maple Mono 的 GitHub 仓库，版本号写死 v7.9
REPO="subframe7536/maple-font"
VERSION="V7.9"
FONT_NAME="MapleMono-NF-CN.zip"
FONT_URL="https://github.com/${REPO}/releases/download/${VERSION}/${FONT_NAME}"

# 本地放字体文件的地方
# $HOME/.local/share/fonts 是 Arch 默认的用户字体目录，不用 sudo
FONT_DIR="$HOME/.local/share/fonts"
FONT_PATH="$FONT_DIR/${FONT_NAME}"

# 如果目录不存在，建一个
mkdir -p "$FONT_DIR"

# ===== 检查字体是不是已经装过了 =====
# 如果 fc-list 能搜到，说明系统里已经有了，问你要不要覆盖
if command -v fc-list &>/dev/null && fc-list | grep -qi "MapleMono"; then
    warn "系统里已经有一个 Maple Mono NF CN 了。"
    ask "要覆盖重装吗？(y/N)"
    read -r confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        info "取消安装。"
        exit 0
    fi
fi

# ===== 下载并解压字体 =====
info "开始下载 ${FONT_NAME} ..."
info "来源: ${FONT_URL}"

# 创建临时目录用来解压
TMP_DIR=$(mktemp -d)
trap "rm -rf $TMP_DIR" EXIT

# 下载到临时目录
if command -v curl &>/dev/null; then
    curl -L --fail --progress-bar -o "$TMP_DIR/${FONT_NAME}" "$FONT_URL" || error "下载失败"
elif command -v wget &>/dev/null; then
    wget -q --show-progress -O "$TMP_DIR/${FONT_NAME}" "$FONT_URL" || error "下载失败"
fi

# 检查下载的文件大小
FILE_SIZE=$(stat -c%s "$TMP_DIR/${FONT_NAME}" 2>/dev/null || stat -f%z "$TMP_DIR/${FONT_NAME}" 2>/dev/null)
if [ "$FILE_SIZE" -lt 1048576 ]; then
    warn "下载的文件只有 ${FILE_SIZE} 字节，可能是个 404 页面。"
    ask "要删掉重试吗？(y/N)"
    read -r confirm
    if [[ "$confirm" == "y" || "$confirm" == "Y" ]]; then
        rm -rf "$TMP_DIR"
        info "已清理，重新运行脚本重试吧。"
        exit 0
    fi
fi

info "下载完成，开始解压..."

# 解压 zip 包
if ! command -v unzip &>/dev/null; then
    error "unzip 没装，装一下: pacman -S unzip"
fi

unzip -q "$TMP_DIR/${FONT_NAME}" -d "$TMP_DIR/extracted/" || error "解压失败"

# 找出所有 .ttf 文件并移到字体目录
TTF_COUNT=0
while IFS= read -r -d '' file; do
    mv "$file" "$FONT_DIR/"
    TTF_COUNT=$((TTF_COUNT + 1))
    info "安装字体: $(basename "$file")"
done < <(find "$TMP_DIR/extracted/" -type f -name "*.ttf" -print0)

if [ $TTF_COUNT -eq 0 ]; then
    error "没找到任何 .ttf 文件，解压出来的东西不对。"
fi

info "共安装了 $TTF_COUNT 个字体文件。"

# 清理临时目录（trap 会自动执行）

# ===== 刷新字体缓存 =====
# fc-cache 让系统知道有新字体来了
if command -v fc-cache &>/dev/null; then
    info "刷新字体缓存 (fc-cache -fv) ..."
    fc-cache -fv 2>/dev/null | head -5
else
    warn "fontconfig 没装，字体装了但系统可能不认识。"
    warn "装一下: pacman -S fontconfig"
fi

# ===== 验证一下 =====
if command -v fc-list &>/dev/null; then
    if fc-list | grep -qi "MapleMono"; then
        info "✅ 安装成功！字体已就位。"
        fc-list | grep -i "MapleMono" | head -1
    else
        warn "fc-list 搜不到 MapleMono，可能需要重启终端或重新登录。"
    fi
else
    warn "fc-list 没有，装 fontconfig 后才能验证。"
fi

# ===== 顺手告诉你怎么用 =====
echo ""
echo "--- 怎么用 ---"
echo "• Termux: 编辑 ~/.termux/termux.properties，加一行 font = ${FONT_PATH}"
echo "• VSCode: 设置 editor.fontFamily = 'Maple Mono NF CN, monospace'"
echo "• Neovim : set guifont=Maple\\ Mono\\ NF\\ CN:h12"
echo "• Alacritty: font.normal.family = 'Maple Mono NF CN'"
echo ""
echo "好了，完事了。"