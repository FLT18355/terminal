# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
ZSH_THEME="powerlevel10k/powerlevel10k"
export ZSH="$HOME/.oh-my-zsh"
plugins=(git zsh-syntax-highlighting zsh-autosuggestions autoupdate colored-man-pages emoji aliases history-substring-search web-search encode64 emoji-clock battery history zoxide you-should-use)
export UPDATE_ZSH_DAYS=1
source $ZSH/oh-my-zsh.sh

alias chcolor='/data/data/com.termux/files/home/.termux/colors.sh'
alias chfont='/data/data/com.termux/files/home/.termux/fonts.sh'

source /data/data/com.termux/files/home/.zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

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
eval "$(zoxide init zsh)"
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
alias list="pkg list-installed | less"             # 查看已安装包
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

# 📝 文本处理
alias json='python -m json.tool'                          # 格式化JSON
alias xml='xmllint --format -'                            # 格式化XML
alias urlencode='python -c "import sys, urllib.parse as p; print(p.quote_plus(sys.argv[1]))"'
alias urldecode='python -c "import sys, urllib.parse as p; print(p.unquote_plus(sys.argv[1]))"'

# 🐍 Python 快捷
alias py3="python3"                                       # python3 你得先有py3
alias py2="python2"                                       # python2 你得先有py2
alias venv="python3 -m venv"                               # 创建虚拟环境
alias activate="source venv/bin/activate"                 # 激活虚拟环境
alias pip-freeze="pip freeze > requirements.txt"          # 导出依赖
alias pip-install="pip install -r requirements.txt"       # 安装依赖
alias grep="grep --color=auto"
alias e='exit' # 快速退出

export PATH=$PATH:$HOME/go/bin
export EDITOR=nvim
export VISUAL=nvim

# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
# p10k配置
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
typeset -g POWERLEVEL9K_EXPERIMENTAL_TIME_REALTIME=true

export PATH=$PATH:$HOME/go/bin
export tuifi_show_hidden=True

typeset -g POWERLEVEL9K_INSTANT_PROMPT=quiet

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
autoload -Uz compinit && compinit -d ~/.cache/zsh/zcompdump
source <(carapace _carapace)


# zsh-syntax-highlighting 颜色自定义
ZSH_HIGHLIGHT_STYLES[default]=none
ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=#f38ba8
ZSH_HIGHLIGHT_STYLES[reserved-word]=fg=#cba6f7
ZSH_HIGHLIGHT_STYLES[alias]=fg=#a6e3a1
ZSH_HIGHLIGHT_STYLES[builtin]=fg=#89b4fa
ZSH_HIGHLIGHT_STYLES[function]=fg=#94e2d5
ZSH_HIGHLIGHT_STYLES[command]=fg=#a6e3a1
ZSH_HIGHLIGHT_STYLES[precommand]=fg=#f9e2af
ZSH_HIGHLIGHT_STYLES[commandseparator]=fg=#f5c2e7
ZSH_HIGHLIGHT_STYLES[path]=fg=#cdd6f4,underline
ZSH_HIGHLIGHT_STYLES[path_prefix]=fg=#cdd6f4,underline
ZSH_HIGHLIGHT_STYLES[globbing]=fg=#fab387
ZSH_HIGHLIGHT_STYLES[history-expansion]=fg=#f2cdcd
export BAT_THEME="Catppuccin Mocha"

# 自定义高亮颜色
ZSH_HIGHLIGHT_STYLES[command]=fg=#89b4fa
ZSH_HIGHLIGHT_STYLES[alias]=fg=#89b4fa
ZSH_HIGHLIGHT_STYLES[builtin]=fg=#89b4fa
ZSH_HIGHLIGHT_STYLES[function]=fg=#89b4fa
ZSH_HIGHLIGHT_STYLES[arg0]=fg=#89b4fa

# 管道符 - 青色
ZSH_HIGHLIGHT_STYLES[commandseparator]=fg=#94e2d5,bold
# 重定向符 > < 也改成青色
ZSH_HIGHLIGHT_STYLES[redirection]=fg=#94e2d5,bold

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

ZSH_HIGHLIGHT_HIGHLIGHTERS=(main cursor)
typeset -gA ZSH_HIGHLIGHT_STYLES

ZSH_HIGHLIGHT_STYLES[command]=fg=#cba6f7
ZSH_HIGHLIGHT_STYLES[alias]=fg=#cba6f7
ZSH_HIGHLIGHT_STYLES[builtin]=fg=#cba6f7
ZSH_HIGHLIGHT_STYLES[function]=fg=#cba6f7
ZSH_HIGHLIGHT_STYLES[arg0]=fg=#cba6f7

alias vizshrc="vim ~/.zshrc"
alias vivirc="vim ~/.vimrc"
alias vi~="vim ~"

# lf=yazi(awa)
alias lf='yazi'

# xcmd
export X_CMD_SILENT=1
[ ! -f "$HOME/.x-cmd.root/X" ] || . "$HOME/.x-cmd.root/X" # boot up x-cmd.

# fzf
eval "$(fzf --zsh)"

alias ffc="fastfetch"
# FLTERS ==============================================================================
# echo "======================================================"
# echo "  ███████╗██╗     ████████╗███████╗██████╗ ███████╗"
# echo "  ██╔════╝██║     ╚══██╔══╝██╔════╝██╔══██╗██╔════╝"
# echo "  █████╗  ██║        ██║   █████╗  ██████╔╝███████╗"
# echo "  ██╔══╝  ██║        ██║   ██╔══╝  ██╔══██╗╚════██║"
# echo "  ██║     ███████╗   ██║   ███████╗██║  ██║███████║"
# echo "  ╚═╝     ╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝"
# echo "                     ███████╗ ██████╗"
# echo "                     ╚══════╝╚══════╝"
# echo "                      󰫳 FLT18355"
# echo "            󰈺  Welcome To My Terminal"
# echo "  FLTERS: Fast Light Terminal Elegant Reliable System"
# echo "======================================================"
# 用户名
export USER="FLT18355_"
export HOST="FLTERS_OS"
PROMPT='%F{magenta}%n@%m%f %~ %# '

# export USER="FLTERS USER"
alias flt-logo="cat ~/.config/fastfetch/logos/catppuccin.txt | tte --random-effect"
flt(){ 
	flt-logo
	echo "󰫳 FLTERS(CatppuccinOS-Mocha) 一个小工具  26.1(2026.3.28+)" | lolcat --freq=0.8
	echo "  FLT18355" | lolcat --freq=0.8
	echo "  Font: UbuntuMono" | lolcat --freq=0.8
	echo "  Themes: Catppuccin 0.2.0" | lolcat --freq=0.8
	echo "  --python 3.13.13, fastfetch, tte" | lolcat --freq=0.8
	echo "  vizshrc 查看配置" | lolcat --freq=0.8
	cat ~/终端专用文件夹/catppuccin.logo | tte print
	ffc

}
alias fzf-b="fzf --preview 'bat --color=always {}'"
alias fzf-e="fzf --preview 'eza --tree --color=always {}'"
alias fzf-v="vim \$(fzf)"
alias syso="sa-t"
# f-weather
alias f-weather='curl "wttr.in/?lang=zh"'
alias f-weather-fz='curl "wttr.in/福州?lang=zh"'
alias f-weather-xm='curl "wttr.in/厦门?lang=zh"'

alias glow='glow -s ~/.config/glow/catppuccin-mocha.json'

ipyl(){
	py ~/终端专用文件夹/ipy_launcher.ipy
}

flt-meows(){
	echo "󰄛 Meow 󰄛 " | lolcat --freq=0.8
	python /data/data/com.termux/files/home/终端专用文件夹/f-tools/catppuccin_cat.py
}

flt-meows-blue(){
	echo "󰄛 Meow 󰄛 " | lolcat --freq=0.8
	python /data/data/com.termux/files/home/终端专用文件夹/f-tools/catppuccin_cat.py -c blue
}

flt-meows-blue-cute(){
	echo "󰄛 Meow 󰄛 " | lolcat --freq=0.8
	python /data/data/com.termux/files/home/终端专用文件夹/f-tools/catppuccin_cat.py -c blue -t cute
}

flt-meows-cute(){
	echo "󰄛 Meow 󰄛 " | lolcat --freq=0.8
	python /data/data/com.termux/files/home/终端专用文件夹/f-tools/catppuccin_cat.py -t cute
}
flt-downl(){
	echo "yt_dlp 26.4" | lolcat --freq=0.8
	python /data/data/com.termux/files/home/终端专用文件夹/f-tools/yd下载器.py
}
flt-icons(){
	echo ""
	echo "   zsh 5.9            android            edge" | lolcat --freq=0.8
	echo "  oh-my-zsh           bash               json" | lolcat --freq=0.8
	echo "   termux           󰄛  catppuccin        markdown" | lolcat --freq=0.8
	echo "   vim                github             npm" | lolcat --freq=0.8
	echo "   python           󰍳  minecraft        󱥰  candy" | lolcat --freq=0.8
	echo "   node.js            html5&css3      󰫳  FLTERS" | lolcat --freq=0.8
	echo ""
}
# =============================================================================================
# 错误命令高亮 - 黄绿色（紫色补色）
ZSH_HIGHLIGHT_STYLES[unknown-token]=fg=#eba0ac
ZSH_HIGHLIGHT_STYLES[command-not-found]=fg=#eba0ac

# 路径颜色 - 青色（推荐）
ZSH_HIGHLIGHT_STYLES[path]=fg=#94e2d5,underline
ZSH_HIGHLIGHT_STYLES[path_prefix]=fg=#94e2d5,underline

# 选项高亮 - 橙色
ZSH_HIGHLIGHT_STYLES[single-hyphen-option]=fg=#fab387
ZSH_HIGHLIGHT_STYLES[double-hyphen-option]=fg=#fab387

# 操作符高亮 - 青色
ZSH_HIGHLIGHT_STYLES[commandseparator]=fg=#94e2d5,bold
ZSH_HIGHLIGHT_STYLES[redirection]=fg=#94e2d5,bold

# tree 紫色主题
alias tree='tree -C --dirsfirst'
export TREE_COLORS="di=01;38;2;203;166;247:ex=01;38;2;166;227;161:ln=01;38;2;250;179;135:fi=01;38;2;205;214;244"

# tuifi
export tuifi_vim_mode=True

# nyancat
alias ncat='nyancat'

alias tmux='zellij'

# 让 eza 不使用 LS_COLORS，只读主题文件
export EZA_COLORS=ignore

alias rust='cargo'

# lazygit
# 使用lazy代替lazygit(更方便)
alias lazy="lazygit"
