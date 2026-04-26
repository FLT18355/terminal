# ============================================
# FLTERS Fish 配置
# ============================================

# --------------------------------------------
# 别名 (Aliases)
# --------------------------------------------
alias chcolor='/data/data/com.termux/files/home/.termux/colors.sh'
alias chfont='/data/data/com.termux/files/home/.termux/fonts.sh'

# 系统优化
alias ST='py ~/终端专用文件夹/f-tools/ST.py'
alias 中国日历='py ~/终端专用文件夹/f-tools/中国日历.py'
alias ydd='py ~/终端专用文件夹/f-tools/yd下载器.py'
alias 清理='bash ~/.termux/boot/01-clean-termux'
alias clock='clock-rs | lolcat'

alias tp="cd ~/终端专用文件夹"
alias td="cd /storage/emulated/0/Download/"
alias th='cd ~'
alias troot="cd /"
alias tsd="cd /storage/emulated/0/"
alias tdc="cd /storage/emulated/0/DCIM/"
alias tpic="cd /storage/emulated/0/Pictures/"

alias upd="oma upgrade && oma upgrade -y && oma refresh"
alias clean="oma clean && apt autoremove -y && pkg clean && apt clean"
alias list="pkg list-installed | bat"
alias prw='pip-review --local --interactive'
alias sa="mkdir -p /data/data/com.termux/cache/apt/archives && upd && clean && go clean -modcache && pip cache purge && go clean -cache && prw && pip cache purge"

# 文件操作
alias li="LS_COLORS= eza --icons --color=always -a"
alias ll="LS_COLORS= eza --icons --color=always -la"
alias la="ls -A --color=always"
alias lt="ls -lt --color=always"
alias lsize="ls -lS --color=always"

# 开发工具
alias py="python3"
alias ipy="ipython"
alias py2="python2"
alias pip="pip3"

# 下载工具
alias wget="wget --show-progress"
alias curl-head="curl -I"
alias down="aria2c -x 16 -s 16"

alias cl='clear && echo "󰄛 打扫干净啦！"'

# 压缩解压
alias untar="tar -xvf"
alias untgz="tar -xzvf"
alias unbz2="tar -xjvf"
alias zipf="zip -r"
alias unzipf="unzip"
alias 7zf="7z a"
alias un7z="7z x"

# 文件操作增强
alias mkdir="mkdir -p"
alias cp="cp -iv"
alias mv="mv -iv"
alias rm="rm -i"
alias ln="ln -s"
alias backup="cp -r"

# 计时工具
alias timer='time read'
alias stopwatch='time cat'
alias countdown='seq'

# 目录操作
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....='cd ../../../..'

# 查找增强
alias ftext="grep -r --include='*.txt'"
alias fcode="grep -r --include='*.{py,js,c}'"

# 系统维护
alias sync="sync && echo '同步完成'"
alias reboot="reboot"
alias poweroff="poweroff"
alias df="df -h"
alias du="du -h"
alias du-max="du -sh * | sort -hr"
alias vs='python -m visidata'

# 文件管理
alias mk="mkdir -p"
alias tch="touch"
alias head="head -n"
alias tail="tail -n"

# Python 快捷
alias py3="python3"
alias py2="python2"
alias grep="grep --color=auto"

alias e='exit' # 退出快捷

# 工具
alias glow='glow -s ~/.config/glow/catppuccin-mocha.json'
alias vfishrc="vim ~/.config/fish/config.fish && ci"
alias lf="yazi"
alias ncat='nyancat'
alias tmux='zellij'
alias tldr='tldr -L zh'
alias ffc='fastfetch'
alias fs="fish"
alias fsr="fisher"

# Git 别名
alias gs='git status'
alias ga='git add'
alias gp='git push'
alias gl='git pull'
alias gc='git commit'
alias gd='git diff'
alias ga.='git add .'
alias ggap='git gc --aggressive --prune=now'
alias yt-dlp='yt-dlp --cookies ~/终端专用文件夹/cookies.txt'

# --------------------------------------------
# 缩写 (Abbreviations - Fish 特色)
# --------------------------------------------
abbr --add gst "git status"
abbr --add ga "git add"
abbr --add gp "git push"
abbr --add gl "git pull"
abbr --add gc "git commit"
abbr --add gd "git diff"
abbr --add g git
abbr --add cl "clear && echo '󰄛 打扫干净啦！'"
abbr --add tma "am start com.termux.api/com.termux.api.activities.TermuxAPIMainActivity"
abbr --add gga "git gc --aggressive"

# --------------------------------------------
# 环境变量 (set -gx)
# --------------------------------------------
set -gx PATH $PATH $HOME/go/bin
set -gx EDITOR nvim
set -gx VISUAL nvim
set -gx PATH $PATH $HOME/.cargo/bin
set -gx PATH $PATH $HOME/.local/bin
set -gx PATH $PREFIX/bin $PATH

# FZF 配置
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
--color=fg:#94E2D5,header:#F38BA8:bold,info:#CBA6F7,pointer:#F9E2AF \
--color=marker:#B4BEFE,fg+:#89B4FA,prompt:#CBA6F7,hl+:#F38BA8:reverse \
--color=selected-bg:#45475A \
--color=border:#CBA6F7,label:#CDD6F4 \
--color=query:#CDD6F4 \
--color=disabled:#585B70 \
--color=preview-bg:#2A2A3E \
--color=preview-border:#6C7086 \
--color=preview-label:#89B4FA:bold \
--color=list-fg:#94E2D5 \
--color=list-bg:#2A2A3E \
--color=selected-fg:#94E2D5 \
--color=scrollbar:#6C7086 \
--color=separator:#6C7086"

set -gx FZF_CTRL_T_OPTS "--preview 'bat --color=always --style=numbers --line-range=:500 {}'"

# 历史配置 (Fish 用环境变量)
set -gx HISTFILE ~/.local/share/fish/fish_history
set -gx fish_history_max 500000

# Carapace 补全
set -gx CARAPACE_BRIDGES "zsh,fish,bash,inshellisense"
# Fish 中 Carapace 需要这样加载
carapace _carapace | source

# Bat 主题
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

# 语言设置
set -gx TLDR_LANGUAGE zh

# 用户信息
set -gx USER FLT18355_
set -gx HOST FLTERS_OS

# 光标设置
set -gx KEYTIMEOUT 10

# EZA 配置
set -gx EZA_COLORS ignore

# --------------------------------------------
# Zoxide (目录跳转)
# --------------------------------------------
# Fish 中 zoxide 的初始化
zoxide init fish | source

# --------------------------------------------
# fzf 集成
# --------------------------------------------
fzf --fish | source

# Oh My Posh 主题
oh-my-posh init fish --config $PREFIX/share/oh-my-posh/themes/poshcat.omp.json | source
# atuin
atuin init fish | source

# --------------------------------------------
# 函数 (Functions)
# --------------------------------------------

# sa-t 函数
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
    go clean -modcache
    pip cache purge
    go clean -cache
    rm -rf ~/.cargo/registry
    sqlite3 ~/.local/share/atuin/history.db "PRAGMA wal_checkpoint(TRUNCATE);"
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

# Yazi 包装函数：退出时自动切换到浏览的目录
function y
    set -l tmp (mktemp -t "yazi-cwd.XXXXXX")
    yazi $argv --cwd-file=$tmp
    set -l cwd (cat $tmp)
    if test -n "$cwd" && test "$cwd" != "$PWD"
        builtin cd $cwd
    end
    rm -f $tmp
end

# v 函数 (打开 vim)
function v
    vi $argv[1]
    ci
end

# 调用 Termux 的 command-not-found 工具
function fish_command_not_found
    /data/data/com.termux/files/usr/libexec/termux/command-not-found $argv[1]
end

# --------------------------------------------
# 光标设置
# --------------------------------------------
# 设置光标为闪烁的竖线
echo -ne '\e[5 q'

# ci 函数：恢复光标
function ci
    echo -ne '\e[5 q'
end

# --------------------------------------------
# 启动画面(欢迎语)[启动运行]
# --------------------------------------------

echo ""
~/logo.sh
am start com.termux.api/com.termux.api.activities.TermuxAPIMainActivity # 每次启动的时候启动termux:api

# --------------------------------------------
# 提示符 (Prompt)
# --------------------------------------------

# --------------------------------------------
# 主题
# --------------------------------------------
fish_config theme choose catppuccin-mocha

# ============================================
# Vi 模式完整配置 (默认启用及增强)
# ============================================

# 设置 Vi 键绑定为默认模式
# set -g fish_key_bindings fish_vi_key_bindings
