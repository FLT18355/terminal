
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

ZSH_THEME=""

export ZSH="$HOME/.oh-my-zsh"
plugins=(git zsh-autosuggestions autoupdate colored-man-pages aliases history-substring-search history zoxide you-should-use)
export UPDATE_ZSH_DAYS=1
source $ZSH/oh-my-zsh.sh

alias chcolor='/data/data/com.termux/files/home/.termux/colors.sh'
alias chfont='/data/data/com.termux/files/home/.termux/fonts.sh'

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
# [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
echo ""

# 系统优化
alias ST='py ~/终端专用文件夹/f-tools/ST.py'
alias 中国日历='py ~/终端专用文件夹/f-tools/中国日历.py'
alias ydd='py ~/终端专用文件夹/f-tools/yd下载器.py'
alias 清理='bash ~/.termux/boot/01-clean-termux'
alias clock='clock-rs | lolcat'
# alias lf='ranger'

# 常用
# eval "$(zoxide init zsh)"
eval "$(zoxide init zsh --cmd j)"
alias tp="cd ~/终端专用文件夹"
alias td="cd /storage/emulated/0/Download/"
alias th='cd ~ && echo "󰄛 好像又回到家了 󰄛" | lolcat'
alias troot="cd /"
alias tsd="cd /storage/emulated/0/"
alias tdc="cd /storage/emulated/0/DCIM/"
alias tpic="cd /storage/emulated/0/Pictures/"
alias tmus="cd /storage/emulated/0/Music/"
alias tvid="cd /storage/emulated/0/Movies/"
alias tdoc="cd /storage/emulated/0/Documents/"

alias upd="oma upgrade && oma upgrade -y && oma refresh"           # 一键更新所有包
alias clean="oma clean && apt autoremove -y && pkg clean && apt clean"       # 清理垃圾
alias list="pkg list-installed | bat"             # 查看已安装包
alias prw='pip-review --local --interactive'
alias sa="mkdir -p /data/data/com.termux/cache/apt/archives && upd && clean && go clean -modcache && pip cache purge && go clean -cache && prw && pip cache purge"
sa-t(){
	echo "系统优化中" | lolcat
	echo "正在创建配置目录..." | lolcat
	mkdir -p /data/data/com.termux/cache/apt/archives
	echo "成功" | lolcat
	echo "正在打印当前家目录..." | lolcat
	echo $HOME | lolcat
	echo "正在运行主程序..." | lolcat
	upd
	clean
	go clean -modcache
	pip cache purge
	go clean -cache
	rm -rf ~/.cargo/registry
	echo "是否更新omz" | lolcat
	echo "1) 更新" | lolcat
	echo "2) 不更新" | lolcat
	echo -n "❯ 选择 (1/2): " | lolcat
	read choice

	case $choice in
		1|"更新"|"y"|"Y")
			echo "正在尝试更新omz" | lolcat
			omz update
			;;
		2|"不更新"|"n"|"N"|"")
			echo "不更新omz" | lolcat
			;;
		*)
			echo "无效输入,默认不更新" | lolcat
			;;
	esac
        echo "是否要运行 pip-review 更新 Python 包？" | lolcat
        echo "1) 继续运行" | lolcat
        echo "2) 跳过" | lolcat
        echo -n "❯ 选择 (1/2): " | lolcat
        read choice
    
        case $choice in
            1|"继续"|"y"|"Y")
                echo "正在运行 pip-review..." | lolcat
                prw
                ;;
            2|"跳过"|"n"|"N"|"")
                echo "跳过 pip-review" | lolcat
                ;;
            *)
                echo "无效输入，默认跳过" | lolcat
                ;;
        esac
	echo "运行完毕,再一次清理pip cache" | lolcat
	pip cache purge
	echo "所有执行程序都运行完毕,感谢您的使用,Bye" | lolcat
}
# 📁 文件操作
alias li="LS_COLORS= eza --icons --color=always -a" # 详细列表（带颜色）
alias ll="LS_COLORS= eza --icons --color=always -la"
alias la="ls -A --color=always"                     # 显示隐藏文件
alias lt="ls -lt --color=always"                    # 按时间排序
alias lsize="ls -lS --color=always"                 # 按大小排序

# 🔧 开发工具
alias py="python3"                                    # 快捷python
alias ipy="ipython"                                   # ipython
alias py2="python2"                                   # python2
alias pip="pip3"                                      # pip3

# 🌐 下载工具
alias wget="wget --show-progress"                     # 显示进度
alias curl-head="curl -I"                             # 只显示头信息
alias down="aria2c -x 16 -s 16"

alias cl='clear && echo "󰄛 打扫干净啦！"'  # 带猫猫的清屏


# 📦 压缩解压快捷
alias untar="tar -xvf"                                # 解压tar
alias untgz="tar -xzvf"                               # 解压tar.gz
alias unbz2="tar -xjvf"                               # 解压tar.bz2
alias zipf="zip -r"                                    # 压缩文件夹
alias unzipf="unzip"                                   # 解压zip
alias 7zf="7z a"                                       # 7z压缩
alias un7z="7z x"                                      # 解压7z

# 📝 文件操作增强
alias mkdir="mkdir -p"                                 # 自动创建父目录
alias cp="cp -iv"                                      # 覆盖前提示
alias mv="mv -iv"                                      # 移动前提示
alias rm="rm -i"                                       # 删除前提示
alias rmf='rm –rf'
alias ln="ln -s"                                       # 创建软链接
alias backup="cp -r"                                   # 简单备份

# ⏱️ 计时工具
alias timer='time read'                                 # 简单计时
alias stopwatch='time cat'                              # 秒表
alias countdown='seq'                                   # 倒计时

# 📁 目录操作
alias ..="cd .."                                        # 上级目录
alias ...="cd ../.."                                    # 上两级
alias ....="cd ../../.."                                # 上三级
alias .....='cd ../../../..'
# 🔍 查找增强
alias ftext="grep -r --include='*.txt'"                 # 在txt中找
alias fcode="grep -r --include='*.{py,js,c}'"           # 在代码中找

# 🛠️ 系统维护
alias sync="sync && echo '同步完成'"                    # 同步磁盘
alias reboot="reboot"                                    # 重启
alias poweroff="poweroff"                                # 关机
alias df="df -h"                                         # 磁盘空间
alias du="du -h"                                         # 目录大小
alias du-max="du -sh * | sort -hr"                       # 排序大小
alias vs='python -m visidata'
# 📂 文件管理
alias mk="mkdir -p"                                       # 创建目录
alias tch="touch"                                       # 创建文件
alias head="head -n"                                      # 指定行数
alias tail="tail -n"                                      # 指定行数

# 🐍 Python 快捷
alias py3="python3"                                       # python3 你得先有py3
alias py2="python2"                                       # python2 你得先有py2
alias grep="grep --color=auto"
alias e='exit' # 快速退出

export PATH=$PATH:$HOME/go/bin

# 默认编辑器
export EDITOR=nvim
export VISUAL=nvim

export PATH=$PATH:$HOME/go/bin

export PATH="$PYENV_ROOT/bin:$PATH"

export PATH=$PATH:$HOME/bin
#--------------------------------------
export PATH="$HOME/.cargo/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"
export PATH="$PREFIX/bin:$PATH"

export FZF_DEFAULT_OPTS=" \
--highlight-line \
--info=inline-right \
--ansi \
--layout=reverse \
--border=rounded \
--height=80% \
--margin=1,2 \
--padding=0,1 \
--cycle \
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
--color=bg+:#313244,bg:#1E1E2E,spinner:#F5E0DC,hl:#F38BA8:underline \
--color=fg:#CDD6F4,header:#F38BA8:bold,info:#CBA6F7,pointer:#F5E0DC \
--color=marker:#B4BEFE,fg+:#CDD6F4,prompt:#CBA6F7,hl+:#F38BA8:reverse \
--color=selected-bg:#45475A \
--color=border:#6C7086,label:#CDD6F4 \
--color=query:#CDD6F4 \
--color=disabled:#585B70 \
--color=preview-bg:#1E1E2E \
--color=preview-border:#6C7086 \
--color=preview-label:#89B4FA:bold \
--color=list-fg:#CDD6F4 \
--color=list-bg:#1E1E2E \
--color=selected-fg:#CDD6F4 \
--color=scrollbar:#6C7086 \
--color=separator:#6C7086"

export FZF_CTRL_T_OPTS="--preview 'bat --color=always {} 2>/dev/null || cat {}'"
export FZF_ALT_C_OPTS="--preview 'eza --tree --color=always {} | head -50'"
export FZF_ALT_R_OPTS="--preview 'echo {}' --preview-window down:3:hidden:wrap"

# 历史配置
HISTSIZE=500000
SAVEHIST=500000
HISTFILE=~/.zsh_history
setopt HIST_IGNORE_DUPS      # 忽略重复命令
setopt SHARE_HISTORY         # 共享历史

# 增强搜索：按上下键搜索历史
bindkey '^[[A' history-search-backward
bindkey '^[[B' history-search-forward

# carapace 自动补全
export CARAPACE_BRIDGES="zsh,fish,bash,inshellisense"
zstyle ":completion:*" format " %F{yellow}-- %d --%f"
zstyle ":completion:*" group-name ""
zstyle ":completion:*" verbose yes
# autoload -Uz compinit && compinit -d ~/.cache/zsh/zcompdump
source <(carapace _carapace)

export BAT_THEME="Catppuccin Mocha"

# man 手册彩色显示
export MANPAGER="less -R --use-color -Dd+r -Du+b"
export LESS_TERMCAP_mb=$'\E[1;31m'
export LESS_TERMCAP_md=$'\E[1;36m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[1;32m'
# grep 彩色输出
# diff 彩色输出
alias diff='diff --color=auto'
# lua 别名
alias lu="lua"
alias luv="lua -v"

alias player='node ~/终端专用文件夹/player.js'
# 设置 tldr 首选语言为中文
export TLDR_LANGUAGE="zh"

alias vizshrc="vim ~/.zshrc"
alias vivirc="vim ~/.vimrc"
alias vi~="vim ~"
alias v='vi'

# lf=yazi(awa)
alias lf='yazi'

# xcmd
export X_CMD_SILENT=1
[ ! -f "$HOME/.x-cmd.root/X" ] || . "$HOME/.x-cmd.root/X" # boot up x-cmd.

# fzf
eval "$(fzf --zsh)"

alias ffc="fastfetch"
# 用户名
export USER="FLT18355_"
export HOST="FLTERS_OS"
PROMPT='%F{magenta}%n@%m%f %~ %# '

# export USER="FLTERS USER"
flt(){
  PINK='\033[38;2;245;194;231m'
  BLUE='\033[38;2;137;180;250m'
  GREEN='\033[38;2;166;227;161m'
  YELLOW='\033[38;2;249;226;175m'
  PURPLE='\033[38;2;203;166;247m'
  RESET='\033[0m'
  ~/logo.sh
  echo "󰫳 ${PURPLE}FLTERS(Fast Light Terminal Elegant Reliable System) 26.2(2026.4.18+)${RESET}"
	echo "  ${BLUE}一个提前配置好的termux满血版${RESET}"
  echo "  ${BLUE}作者:FLT18355_${RESET}"
  echo "  ${BLUE}主要主题:catppuccin-mocha${RESET}"
  echo "  ${BLUE}命令行主题:oh-my-posh${RESET}"
  echo "  ${BLUE}终端环境:zsh${RESET}"
  echo "  ${BLUE}代码编辑器:neovim${RESET}"
  echo "  ${YELLOW}懒人专属,解决一切配置的问题${RESET}"
  echo "  ${YELLOW}Hello World!${RESET}"
  echo "  ${GREEN}在FLTERS创造一切可能!${RESET}"
}
alias fzb="fzf --preview 'bat --color=always {}'"
alias fze="fzf --preview 'eza --tree --color=always {}'"
alias fzv="vim \$(fzf)"

flt

# f-weather
alias weather='curl "wttr.in/?lang=zh"'
alias weather-fz='curl "wttr.in/福州?lang=zh"'
alias weather-xm='curl "wttr.in/厦门?lang=zh"'

alias glow='glow -s ~/.config/glow/catppuccin-mocha.json'

# nyancat
alias ncat='nyancat'

alias tmux='zellij'

alias tldr='tldr -L zh'
# 让 eza 不使用 LS_COLORS，只读主题文件
export EZA_COLORS=ignore

# 初始化 Oh My Posh（使用 Catppuccin Mocha 主题）
# 使用 Catppuccin Mocha 主题
eval "$(oh-my-posh init zsh --config $PREFIX/share/oh-my-posh/themes/mocha.omp.json)"
source ~/.local/share/zinit/zinit.git/zinit.zsh

zinit light zdharma-continuum/fast-syntax-highlighting

