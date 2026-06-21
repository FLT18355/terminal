# ============================================
# FLTERS Fish 配置
# ============================================

# --------------------------------------------
# 环境变量
# --------------------------------------------

# 编辑器
set -gx EDITOR nvim
set -gx VISUAL nvim

# PATH
set -gx PATH $PATH $HOME/go/bin
set -gx PATH $PATH $HOME/.cargo/bin
set -gx PATH $PATH $HOME/.local/bin
set -gx PATH $PREFIX/bin $PATH
fish_add_path ~/bin
fish_add_path /home/flt18355/.opencode/bin

# FZF
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
--header "FLT18355的FZF" \
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

# Bat
set -gx BAT_THEME "Catppuccin Mocha"

# Man 手册彩色显示
set -gx MANPAGER "less -R --use-color -Dd+r -Du+b"
set -gx LESS_TERMCAP_mb (printf '\E[1;31m')
set -gx LESS_TERMCAP_md (printf '\E[1;36m')
set -gx LESS_TERMCAP_me (printf '\E[0m')
set -gx LESS_TERMCAP_se (printf '\E[0m')
set -gx LESS_TERMCAP_so (printf '\E[01;44;33m')
set -gx LESS_TERMCAP_ue (printf '\E[0m')
set -gx LESS_TERMCAP_us (printf '\E[1;32m')

# EZA
set -gx EZA_COLORS ignore

# 语言 / 本地化
set -gx TLDR_LANGUAGE zh

# Qt / 终端
set -gx SAL_USE_VCLPLUGIN qt6
set -x QT_QPA_PLATFORMTHEME qt5ct

# Fish 历史
set -gx HISTFILE ~/.local/share/fish/fish_history

# 光标
set -gx KEYTIMEOUT 10

# Homebrew (Tsinghua 镜像)
set -gx HOMEBREW_BOTTLE_DOMAIN "https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
set -gx HOMEBREW_API_DOMAIN "https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
set -gx HOMEBREW_BREW_GIT_REMOTE "https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
set -gx HOMEBREW_CORE_GIT_REMOTE "https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
set -gx HOMEBREW_INSTALL_FROM_API 1

# 其他
set -gx GLYCIN_DISABLE_SANDBOX 1
# set -gx CARAPACE_BRIDGES "zsh,fish,bash,inshellisense"

# --------------------------------------------
# Carapace 补全 (注释掉)
# --------------------------------------------
# carapace _carapace | source

# --------------------------------------------
# Zoxide (注释掉)
# --------------------------------------------
# zoxide init fish | source

# --------------------------------------------
# 插件初始化
# --------------------------------------------
fzf --fish | source
eval "$(starship init fish)"

# --------------------------------------------
# 主题 / 提示符
# --------------------------------------------
fish_config theme choose catppuccin-mocha

# --------------------------------------------
# 别名
# --------------------------------------------

# ---- Termux 专属 ----
alias chcolor='/data/data/com.termux/files/home/.termux/colors.sh'
alias chfont='/data/data/com.termux/files/home/.termux/fonts.sh'
alias 清理='bash ~/.termux/boot/01-clean-termux'

# ---- 目录导航 ----
alias tp="cd ~/终端专用文件夹"
alias td="cd /storage/emulated/0/Download/"
alias th='cd ~'
alias troot="cd /"
alias tsd="cd /storage/emulated/0/"
alias tdc="cd /storage/emulated/0/DCIM/"
alias tpic="cd /storage/emulated/0/Pictures/"
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....='cd ../../../..'

# ---- 包管理 ----
alias upd="oma upgrade && oma upgrade -y && oma refresh"
alias clean="oma clean && apt autoremove -y && pkg clean && apt clean"
alias list="pkg list-installed | bat"
alias prw='pip-review --local --interactive'

# ---- 文件列表 ----
alias li="LS_COLORS= eza --icons --color=always -a"
alias ll="LS_COLORS= eza --icons --color=always -la"
alias la="ls -A --color=always"
alias lt="ls -lt --color=always"
alias lsize="ls -lS --color=always"

# ---- 文件操作 ----
alias mkdir="mkdir -p"
alias cp="cp -iv"
alias mv="mv -iv"
alias rm="rm -i"
alias ln="ln -s"
alias mk="mkdir -p"
alias tch="touch"
alias head="head -n"
alias tail="tail -n"

# ---- 压缩解压 ----
alias untar="tar -xvf"
alias untgz="tar -xzvf"
alias unbz2="tar -xjvf"
alias zipf="zip -r"
alias unzipf="unzip"
alias 7zf="7z a"
alias un7z="7z x"

# ---- 开发工具 ----
alias py="python3"
alias py3="python3"
alias py2="python2"
alias ipy="ipython"
alias vi="nvim"
alias code="/home/flt18355/Downloads/VSCode-linux-arm64/code --no-sandbox"
alias vs='python -m visidata'
alias grep="grep --color=auto"

# ---- 下载工具 ----
alias wget="wget --show-progress"
alias curl-head="curl -I"
alias down="aria2c -x 16 -s 16"
alias bili="yt-dlp --cookies /home/flt18355/cookies.txt"
# alias yt-dlp='yt-dlp --cookies ~/终端专用文件夹/cookies.txt'

# ---- Git ----
alias gs='git status'
alias ga='git add'
alias gp='git push'
alias gl='git pull'
alias gc='git commit'
alias gd='git diff'
alias ga.='git add .'
alias ggap='git gc --aggressive --prune=now'
alias gsh='grun --shell'

# ---- 系统维护 ----
alias sync="sync && echo '同步完成'"
alias reboot="reboot"
alias poweroff="poweroff"
alias df="df -h"
alias du="du -h"
alias du-max="du -sh * | sort -hr"
alias cl='clear && echo "󰄛 打扫干净啦！" && ci'

# ---- 搜索 ----
alias ftext="grep -r --include='*.txt'"
alias fcode="grep -r --include='*.{py,js,c}'"

# ---- 工具 ----
alias glow='glow -s ~/.config/glow/catppuccin-mocha.json'
alias vfishrc="vim ~/.config/fish/config.fish && ci"
alias lf="yazi"
alias ncat='nyancat'
# alias ze='zellij'
alias tldr='tldr -L zh'
alias ffc='fastfetch'
alias fs="fish"
alias fsr="fisher"
alias clock='clock-rs | lolcat'
alias timer='time read'
alias stopwatch='time cat'
alias countdown='seq'
alias e='exit'

# ---- Termux 工具 ----
alias ST='py ~/终端专用文件夹/f-tools/ST.py'
alias 中国日历='py ~/终端专用文件夹/f-tools/中国日历.py'
alias ydd='py ~/终端专用文件夹/f-tools/yd下载器.py'

# --------------------------------------------
# 缩写 (Abbreviations)
# --------------------------------------------
abbr --add gst "git status"
abbr --add ga "git add"
abbr --add gp "git push"
abbr --add gl "git pull"
abbr --add gc "git commit"
abbr --add gd "git diff"
abbr --add g git
abbr --add gga "git gc --aggressive"
abbr --add gpa "git push && git gc --aggressive"
abbr --add tma "am start com.termux.api/com.termux.api.activities.TermuxAPIMainActivity"

# --------------------------------------------
# 函数
# --------------------------------------------

# sa：系统全面优化
function sa
    echo 系统优化中 | lolcat
    echo "正在创建配置目录..." | lolcat
    mkdir -p /data/data/com.termux/cache/apt/archives
    echo 成功 | lolcat
    echo "正在打印当前家目录..." | lolcat
    echo $HOME | lolcat
    echo "正在运行主程序..." | lolcat
    upd
    clean
    pip cache purge
    rm -rf ~/.cargo/registry
    echo "是否要运行 pip-review 更新 Python 包？" | lolcat
    echo "1) 继续运行" | lolcat
    echo "2) 跳过" | lolcat
    echo -n "❯ 选择 (1/2): " | lolcat
    read choice
    switch $choice
        case 1 继续 y Y
            echo "正在运行 pip-review..." | lolcat
            prw
        case 2 跳过 n N ""
            echo "跳过 pip-review" | lolcat
        case '*'
            echo "无效输入，默认跳过" | lolcat
    end
    echo "运行完毕,再一次清理pip cache" | lolcat
    pip cache purge
    echo "所有执行程序都运行完毕,感谢您的使用,Bye" | lolcat
end

# pacman / npkg (遮蔽原始 pacman，用 npkg 替代)
function pacman
    echo "错误: 'pacman' 命令已被禁用。请使用 'npkg' 代替。" >&2
    return 1
end
function npkg
    if contains -- -h $argv; or contains -- --help $argv
        /usr/bin/pacman $argv | sed s/pacman/npkg/g
    else
        sudo /usr/bin/pacman $argv
    end
end

# kitty 终端启动
function open_kitty
    export DISPLAY=:0
    openbox &
    kitty
end

# Yazi：退出时自动切换到浏览目录
function y
    set -l tmp (mktemp -t "yazi-cwd.XXXXXX")
    yazi $argv --cwd-file=$tmp
    set -l cwd (cat $tmp)
    if test -n "$cwd" && test "$cwd" != "$PWD"
        builtin cd $cwd
    end
    rm -f $tmp
end

# v：打开 nvim 并恢复光标
function v
    vi $argv[1]
    ci
end

# ci：恢复光标为闪烁竖线
function ci
    echo -ne '\e[5 q'
end

# Termux command-not-found
function fish_command_not_found
    /data/data/com.termux/files/usr/libexec/termux/command-not-found $argv[1]
end

# --------------------------------------------
# Vi 模式 (默认禁用)
# --------------------------------------------
# set -g fish_key_bindings fish_vi_key_bindings

# --------------------------------------------
# 启动时运行
# --------------------------------------------
# am start com.termux.api/com.termux.api.activities.TermuxAPIMainActivity

# XDG_RUNTIME_DIR（Wayland）
if not set -q XDG_RUNTIME_DIR
    set -gx XDG_RUNTIME_DIR /tmp/runtime-$USER
    mkdir -p $XDG_RUNTIME_DIR
    chmod 700 $XDG_RUNTIME_DIR
end

set -gx PULSE_SERVER 127.0.0.1
set fish_greeting
ffc
