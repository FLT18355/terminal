#!/bin/bash

# FLTERS - Termux 配置安装脚本
# 用法: chmod +x install.sh && ./install.sh

# 颜色定义，让输出更美观
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的绝对路径
DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 打印带颜色的信息
info() {
	echo -e "${BLUE}[INFO]${NC} $1"
}

success() {
	echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warn() {
	echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
	echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在 Termux 环境中运行
check_termux() {
	if [[ -z "$PREFIX" || "$PREFIX" != *"com.termux"* ]]; then
		error "请在 Termux 环境中运行此脚本。"
		exit 1
	fi
	success "Termux 环境检查通过"
}

# 更新包管理器并安装基础软件包
install_packages() {
	info "更新包管理器并安装基础软件包..."

	pkg update -y
	pkg upgrade -y || warn "部分包升级失败，继续执行..."

	local packages=(
		zsh neovim git lazygit ripgrep fzf
		nodejs-lts python rust cmake
		ffmpeg sox bat eza zoxide
		openssh termux-api termux-tools
	)

	for pkg in "${packages[@]}"; do
		info "正在安装: $pkg"
		pkg install -y "$pkg" || warn "安装 $pkg 失败，继续执行..."
	done

	success "基础软件包安装完成"
}

# 创建必要的目录结构
create_directories() {
	info "创建配置目录..."

	mkdir -p ~/.config
	mkdir -p ~/.local/bin
	mkdir -p ~/.termux
	mkdir -p ~/.oh-my-zsh/custom/plugins
	mkdir -p ~/.zsh

	success "目录结构创建完成"
}

# 创建配置文件软链接
create_symlinks() {
	info "创建配置文件软链接..."

	# 主目录配置文件
	for file in .bashrc .zshrc .gitconfig .p10k.zsh; do
		if [[ -f "$DOTFILES_DIR/$file" ]]; then
			ln -sf "$DOTFILES_DIR/$file" ~/"$file"
			info "已链接: ~/$file"
		else
			warn "未找到: $DOTFILES_DIR/$file，跳过"
		fi
	done

	# termux 配置
	if [[ -d "$DOTFILES_DIR/termux" ]]; then
		for config in "$DOTFILES_DIR/termux"/*; do
			if [[ -f "$config" ]]; then
				local basename=$(basename "$config")
				ln -sf "$config" ~/.termux/"$basename"
				info "已链接: ~/.termux/$basename"
			fi
		done
	else
		warn "termux 配置目录不存在，跳过"
	fi

	# termux/config 下的所有配置
	if [[ -d "$DOTFILES_DIR/termux/config" ]]; then
		for config in "$DOTFILES_DIR/termux/config"/*; do
			if [[ -e "$config" ]]; then
				local basename=$(basename "$config")
				ln -sf "$config" ~/.config/"$basename"
				info "已链接: ~/.config/$basename"
			fi
		done
	else
		warn "termux/config 配置目录不存在，跳过"
	fi

	success "所有配置文件链接完成"
}

# 安装 Oh My Zsh
install_ohmyzsh() {
	if [[ ! -d ~/.oh-my-zsh ]]; then
		info "安装 Oh My Zsh..."
		sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
		success "Oh My Zsh 安装完成"
	else
		warn "Oh My Zsh 已存在，跳过安装"
	fi
}

# 安装 Zinit 插件管理器
install_zinit() {
	if [[ ! -d ~/.local/share/zinit ]]; then
		info "安装 Zinit 插件管理器..."
		bash -c "$(curl -fsSL https://raw.githubusercontent.com/zdharma-continuum/zinit/HEAD/scripts/install.sh)"
		success "Zinit 安装完成"
	else
		warn "Zinit 已存在，跳过安装"
	fi
}

# 安装额外的 Python 包
install_python_packages() {
	info "安装 Python 工具包..."
	pip install --upgrade pip
	pip install pynvim neovim-remote || warn "Python 包安装失败，可稍后手动安装"

	success "Python 包安装完成"
}

# 安装 Node.js 全局包
install_node_packages() {
	info "安装 Node.js 全局包..."
	npm install -g neovim tree-sitter-cli || warn "Node.js 包安装失败，可稍后手动安装"

	success "Node.js 包安装完成"
}

# 安装 LazyVim（带备份）
install_lazyvim() {
	if [[ -d ~/.config/nvim ]]; then
		warn "检测到已存在的 Neovim 配置，将备份到 ~/.config/nvim.bak"
		mv ~/.config/nvim ~/.config/nvim.bak
	fi
	info "安装 LazyVim..."
	git clone https://github.com/LazyVim/starter ~/.config/nvim
	rm -rf ~/.config/nvim/.git
	success "LazyVim 安装完成"
}

# 配置 Termux 终端
configure_termux() {
	info "配置 Termux 终端..."

	# 应用 termux 配置
	termux-reload-settings

	# 请求存储权限
	if [[ ! -d ~/storage ]]; then
		info "请求存储权限，请在弹窗中允许..."
		termux-setup-storage
		# 等待用户授权
		sleep 3
	fi

	success "Termux 配置完成"
}

# 设置 Zsh 为默认 Shell
set_default_shell() {
	if [[ "$SHELL" != "$PREFIX/bin/zsh" ]]; then
		if command -v chsh &>/dev/null; then
			info "设置 Zsh 为默认 Shell..."
			chsh -s zsh
			success "默认 Shell 已更改为 Zsh，请重启 Termux 生效"
		else
			warn "chsh 命令不可用，请手动将默认 Shell 改为 zsh"
		fi
	else
		warn "Zsh 已经是默认 Shell"
	fi
}

# 清理临时文件和缓存
cleanup() {
	info "清理临时文件..."
	# 清理 pip 缓存
	pip cache purge 2>/dev/null || true
	# 清理 npm 缓存
	npm cache clean --force 2>/dev/null || true
	success "清理完成"
}

# 打印安装后提示
print_post_install_guide() {
	echo ""
	echo "========================================="
	success "FLTERS 安装完成！"
	echo "========================================="
	echo ""
	echo "📋 下一步操作："
	echo ""
	echo "1. 🔄 重启 Termux 应用"
	echo "2. 🎨 运行 'nvim' 让 LazyVim 完成插件安装"
	echo "3. 🚀 可选：运行 'yazi' 配置 Yazi 主题"
	echo "4. 📝 可选：运行 'git config --global user.name \"你的名字\"'"
	echo "5. 📝 可选：运行 'git config --global user.email \"你的邮箱\"'"
	echo ""
	echo "💡 提示："
	echo "   - 如果遇到任何问题，请检查 ~/.zshrc 配置文件"
	echo "   - 欢迎访问项目主页：https://github.com/FLT18355/terminal"
	echo ""
}

# 主函数
main() {
	echo "========================================="
	echo "   FLTERS - Termux 配置安装脚本 v2.0"
	echo "========================================="
	echo ""

	check_termux
	install_packages
	create_directories
	create_symlinks
	install_ohmyzsh
	install_zinit
	install_python_packages
	install_node_packages
	install_lazyvim
	configure_termux
	set_default_shell
	cleanup

	print_post_install_guide
}

# 执行主函数
main "$@"
