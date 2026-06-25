#!/bin/bash
# 使用脚本须知:你的系统需要拥有sudo, 否者下面指令无法运行
# 你的用户需要拥有sudo权限
# ===== 检测 sudo 是否可用 =====
if ! command -v sudo &> /dev/null; then
    echo "错误: 系统未安装 sudo。"
    echo "请切换为 root 用户后直接运行:pacman -S sudo"
    echo "  su -"
    echo "  然后重新执行该脚本。"
    exit 1
fi

# ===== 检测当前用户是否有 sudo 权限 =====
if ! sudo -v 2>/dev/null; then
    echo "错误: 当前用户没有 sudo 权限。"
    echo "请切换为 root 用户或添加当前用户到 sudoers 后重试。"
    exit 1
fi

echo "欢迎使用安装脚本, 该脚本可以快速为你安装系统的必要软件, 在这之前请确认一下你的用户是否拥有sudo权限"
# ===== 询问是否继续 =====
read -p "是否继续？(y/N): " choice
case "$choice" in
    y|Y|yes|Yes|YES)
        echo "继续执行..."
        ;;
    *)
        echo "已取消安装。"
        exit 0
        ;;
esac

echo "Step 1(安装基础工具)"
sudo pacman -S file 7zip gcc btop neovim fastfetch base-devel git curl wget unzip

sleep 2

echo "Step 2(安装开发工具)"
sudo pacman -S ripgrep fd lazygit tmux python python-pip python-pipx fzf bat

CURRENT_SHELL=$(basename "$SHELL")
# ============================================
# 配置 fzf (包含自定义主题和快捷键)
# ============================================

echo ""
echo "正在配置 fzf (FLT18355 定制版)..."

case "$CURRENT_SHELL" in
    bash)
        CONFIG_FILE="$HOME/.bashrc"
        # 检查是否已存在 fzf 配置
        if ! grep -q "FZF_DEFAULT_OPTS" "$CONFIG_FILE" 2>/dev/null; then
            cat >> "$CONFIG_FILE" << 'EOF'

# ===== fzf 配置 (FLT18355 定制版) =====
export FZF_DEFAULT_OPTS="\
--highlight-line \
--info=inline-right \
--ansi \
--layout=reverse \
--border=rounded \
--height=80% \
--margin=1,2 \
--padding=0,1 \
--cycle \
--border \
--header=\"FLT18355的FZF\" \
--header-border inline \
--header-first \
--keep-right \
--scroll-off=5 \
--bind='ctrl-u:clear-query' \
--bind='ctrl-y:accept' \
--bind='ctrl-a:select-all' \
--bind='ctrl-d:deselect-all' \
--bind='ctrl-t:toggle-all' \
--bind='?:toggle-preview' \
--bind='alt-up:preview-page-up' \
--bind='alt-down:preview-page-down' \
--color=bg+:#1E1E2E,bg:#2A2A3E,spinner:#F9E2AF,hl:#F38BA8:underline \
--color=fg:#CDD6F4,header:#F38BA8:bold,info:#CBA6F7,pointer:#F9E2AF \
--color=marker:#B4BEFE,fg+:#A6E3A1,prompt:#CBA6F7,hl+:#F38BA8:reverse \
--color=selected-bg:#45475A \
--color=border:#CBA6F7,label:#CDD6F4 \
--color=query:#CDD6F4 \
--color=disabled:#585B70 \
--color=preview-bg:#2A2A3E \
--color=preview-border:#6C7086 \
--color=preview-label:#89B4FA:bold \
--color=list-fg:#CDD6F4 \
--color=list-bg:#2A2A3E \
--color=selected-fg:#CDD6F4 \
--color=scrollbar:#6C7086 \
--color=separator:#6C7086"

export FZF_CTRL_T_OPTS="--preview 'bat --color=always --style=numbers --line-range=:500 {}'"

# 加载 fzf 快捷键和补全
source /usr/share/fzf/key-bindings.bash
source /usr/share/fzf/completion.bash
EOF
            echo "✅ 已添加 fzf 配置到 $CONFIG_FILE"
        else
            echo "⚠️ fzf 配置已存在，跳过写入"
        fi
        ;;
    zsh)
        CONFIG_FILE="$HOME/.zshrc"
        if ! grep -q "FZF_DEFAULT_OPTS" "$CONFIG_FILE" 2>/dev/null; then
            cat >> "$CONFIG_FILE" << 'EOF'

# ===== fzf 配置 (FLT18355 定制版) =====
export FZF_DEFAULT_OPTS="\
--highlight-line \
--info=inline-right \
--ansi \
--layout=reverse \
--border=rounded \
--height=80% \
--margin=1,2 \
--padding=0,1 \
--cycle \
--border \
--header=\"FLT18355的FZF\" \
--header-border inline \
--header-first \
--keep-right \
--scroll-off=5 \
--bind='ctrl-u:clear-query' \
--bind='ctrl-y:accept' \
--bind='ctrl-a:select-all' \
--bind='ctrl-d:deselect-all' \
--bind='ctrl-t:toggle-all' \
--bind='?:toggle-preview' \
--bind='alt-up:preview-page-up' \
--bind='alt-down:preview-page-down' \
--color=bg+:#1E1E2E,bg:#2A2A3E,spinner:#F9E2AF,hl:#F38BA8:underline \
--color=fg:#CDD6F4,header:#F38BA8:bold,info:#CBA6F7,pointer:#F9E2AF \
--color=marker:#B4BEFE,fg+:#A6E3A1,prompt:#CBA6F7,hl+:#F38BA8:reverse \
--color=selected-bg:#45475A \
--color=border:#CBA6F7,label:#CDD6F4 \
--color=query:#CDD6F4 \
--color=disabled:#585B70 \
--color=preview-bg:#2A2A3E \
--color=preview-border:#6C7086 \
--color=preview-label:#89B4FA:bold \
--color=list-fg:#CDD6F4 \
--color=list-bg:#2A2A3E \
--color=selected-fg:#CDD6F4 \
--color=scrollbar:#6C7086 \
--color=separator:#6C7086"

export FZF_CTRL_T_OPTS="--preview 'bat --color=always --style=numbers --line-range=:500 {}'"

# 加载 fzf 快捷键和补全
source /usr/share/fzf/key-bindings.zsh
source /usr/share/fzf/completion.zsh
EOF
            echo "✅ 已添加 fzf 配置到 $CONFIG_FILE"
        else
            echo "⚠️ fzf 配置已存在，跳过写入"
        fi
        ;;
    fish)
        CONFIG_DIR="$HOME/.config/fish"
        CONFIG_FILE="$CONFIG_DIR/config.fish"
        mkdir -p "$CONFIG_DIR"
        if ! grep -q "FZF_DEFAULT_OPTS" "$CONFIG_FILE" 2>/dev/null; then
            cat >> "$CONFIG_FILE" << 'EOF'

# ===== fzf 配置 (FLT18355 定制版) =====
set -gx FZF_DEFAULT_OPTS "\
--highlight-line \
--info=inline-right \
--ansi \
--layout=reverse \
--border=rounded \
--height=80% \
--margin=1,2 \
--padding=0,1 \
--cycle \
--border \
--header=\"FLT18355的FZF\" \
--header-border inline \
--header-first \
--keep-right \
--scroll-off=5 \
--bind='ctrl-u:clear-query' \
--bind='ctrl-y:accept' \
--bind='ctrl-a:select-all' \
--bind='ctrl-d:deselect-all' \
--bind='ctrl-t:toggle-all' \
--bind='?:toggle-preview' \
--bind='alt-up:preview-page-up' \
--bind='alt-down:preview-page-down' \
--color=bg+:#1E1E2E,bg:#2A2A3E,spinner:#F9E2AF,hl:#F38BA8:underline \
--color=fg:#CDD6F4,header:#F38BA8:bold,info:#CBA6F7,pointer:#F9E2AF \
--color=marker:#B4BEFE,fg+:#A6E3A1,prompt:#CBA6F7,hl+:#F38BA8:reverse \
--color=selected-bg:#45475A \
--color=border:#CBA6F7,label:#CDD6F4 \
--color=query:#CDD6F4 \
--color=disabled:#585B70 \
--color=preview-bg:#2A2A3E \
--color=preview-border:#6C7086 \
--color=preview-label:#89B4FA:bold \
--color=list-fg:#CDD6F4 \
--color=list-bg:#2A2A3E \
--color=selected-fg:#CDD6F4 \
--color=scrollbar:#6C7086 \
--color=separator:#6C7086"

set -gx FZF_CTRL_T_OPTS "--preview 'bat --color=always --style=numbers --line-range=:500 {}'"

# 加载 fzf fish 支持
fzf --fish | source
EOF
            echo "✅ 已添加 fzf 配置到 $CONFIG_FILE"
        else
            echo "⚠️ fzf 配置已存在，跳过写入"
        fi
        ;;
    *)
        echo "⚠️ 未知 Shell: $CURRENT_SHELL"
        echo "请手动将以下配置添加到你的 Shell 配置文件中："
        echo ""
        echo "  Bash/Zsh:"
        echo "    export FZF_DEFAULT_OPTS=\"...\"  # (完整配置)"
        echo "    export FZF_CTRL_T_OPTS=\"--preview 'bat --color=always --style=numbers --line-range=:500 {}'\""
        echo "    source /usr/share/fzf/key-bindings.bash  # Bash"
        echo "    source /usr/share/fzf/completion.bash    # Bash"
        echo "    # 或"
        echo "    source /usr/share/fzf/key-bindings.zsh   # Zsh"
        echo "    source /usr/share/fzf/completion.zsh     # Zsh"
        echo ""
        echo "  Fish:"
        echo "    set -gx FZF_DEFAULT_OPTS \"...\""
        echo "    set -gx FZF_CTRL_T_OPTS \"--preview 'bat --color=always --style=numbers --line-range=:500 {}'\""
        echo "    fzf --fish | source"
        echo ""
        ;;
esac

sleep 2

echo "Step 3(安装额外的包)"

# ===== 询问是否继续 =====
read -p "是否继续？接下来要安装的包:zoxide, fish(y/N): " choice
case "$choice" in
    y|Y|yes|Yes|YES)
        echo "继续执行..."
        ;;
    *)
        echo "已取消安装。"
        exit 0
        ;;
esac

sudo pacman -S zoxide

echo "OK, zoxide已完成安装, 正在写入配置..."

# ============================================
# 检测当前 Shell 并配置 zoxide
# ============================================

# 获取当前 Shell 名称
CURRENT_SHELL=$(basename "$SHELL")

echo "检测到当前 Shell: $CURRENT_SHELL"

case "$CURRENT_SHELL" in
    bash)
        echo "正在配置 Bash..."
        CONFIG_FILE="$HOME/.bashrc"
        if ! grep -q "zoxide init" "$CONFIG_FILE" 2>/dev/null; then
            echo 'eval "$(zoxide init bash)"' >> "$CONFIG_FILE"
            echo "✅ 已添加 zoxide 配置到 $CONFIG_FILE"
        else
            echo "⚠️ zoxide 配置已存在，跳过写入"
        fi
        ;;
    zsh)
        echo "正在配置 Zsh..."
        CONFIG_FILE="$HOME/.zshrc"
        if ! grep -q "zoxide init" "$CONFIG_FILE" 2>/dev/null; then
            echo 'eval "$(zoxide init zsh)"' >> "$CONFIG_FILE"
            echo "✅ 已添加 zoxide 配置到 $CONFIG_FILE"
        else
            echo "⚠️ zoxide 配置已存在，跳过写入"
        fi
        ;;
    fish)
        echo "正在配置 Fish..."
        CONFIG_DIR="$HOME/.config/fish"
        CONFIG_FILE="$CONFIG_DIR/config.fish"
        mkdir -p "$CONFIG_DIR"
        if ! grep -q "zoxide init" "$CONFIG_FILE" 2>/dev/null; then
            echo 'zoxide init fish | source' >> "$CONFIG_FILE"
            echo "✅ 已添加 zoxide 配置到 $CONFIG_FILE"
        else
            echo "⚠️ zoxide 配置已存在，跳过写入"
        fi
        ;;
    *)
        echo "⚠️ 未知 Shell: $CURRENT_SHELL"
        echo "请手动将以下命令添加到你的 Shell 配置文件中："
        echo ""
        echo "  Bash:   eval \"\$(zoxide init bash)\""
        echo "  Zsh:    eval \"\$(zoxide init zsh)\""
        echo "  Fish:   zoxide init fish | source"
        echo ""
        ;;
esac

echo ""
echo "✅ zoxide 配置完成！"
echo "请执行以下命令使配置生效："
echo "  source $CONFIG_FILE"
echo ""
echo "或者重新打开终端即可使用 'z' 命令跳转目录。"

sudo pacman -S fish nano