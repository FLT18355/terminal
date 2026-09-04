#!/bin/sh
# ============================================================
#  winget-linux - Windows Package Manager 的 Linux 整活包装器
#  在 Linux 上模拟 winget 命令，实际调用系统原生包管理器
#
#  支持后端: apt, pacman, dnf, yum, zypper, apk, xbps, portage, brew
#  兼容 Shell: bash, zsh, fish, dash, ash 等所有 POSIX shell
# ============================================================

WINGET_VER="1.12.30"

# ---------- 颜色 ----------
if [ -t 1 ] && [ -t 2 ]; then
    ESC=$(printf '\033')
    C_RED="${ESC}[0;31m"
    C_GREEN="${ESC}[0;32m"
    C_YELLOW="${ESC}[0;33m"
    C_BLUE="${ESC}[0;34m"
    C_BOLD="${ESC}[1m"
    C_NC="${ESC}[0m"
else
    C_RED='' C_GREEN='' C_YELLOW='' C_BLUE='' C_BOLD='' C_NC=''
fi

# ---------- 检测包管理器 ----------
detect_pm() {
    if   command -v pacman       >/dev/null 2>&1; then PM="pacman"
    elif command -v apt-get      >/dev/null 2>&1; then PM="apt"
    elif command -v dnf          >/dev/null 2>&1; then PM="dnf"
    elif command -v yum          >/dev/null 2>&1; then PM="yum"
    elif command -v zypper       >/dev/null 2>&1; then PM="zypper"
    elif command -v apk          >/dev/null 2>&1; then PM="apk"
    elif command -v xbps-install >/dev/null 2>&1; then PM="xbps"
    elif command -v emerge       >/dev/null 2>&1; then PM="portage"
    elif command -v brew         >/dev/null 2>&1; then PM="brew"
    else
        printf "${C_RED}错误: 未找到支持的包管理器${C_NC}\n" >&2
        printf "支持: apt, pacman, dnf, yum, zypper, apk, xbps, portage, brew\n" >&2
        exit 1
    fi
}

# ---------- sudo 处理 ----------
setup_sudo() {
    if [ "$(id -u)" -eq 0 ]; then
        SUDO=""
    elif command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        SUDO=""
    fi
}

# ---------- 提取包名（跳过 --xxx 选项，原样保留用户输入） ----------
extract_packages() {
    PKGS=""
    for arg in "$@"; do
        case "$arg" in
            -*) ;;
            *)  PKGS="$PKGS $arg"
                ;;
        esac
    done
    PKGS=$(printf '%s' "$PKGS" | sed 's/^ *//')
}

# ---------- 获取发行版信息 ----------
get_distro() {
    if [ -f /etc/os-release ]; then
        (. /etc/os-release && printf '%s' "$PRETTY_NAME")
    elif command -v lsb_release >/dev/null 2>&1; then
        lsb_release -ds | tr -d '"'
    else
        uname -sr
    fi
}

# ---------- 帮助 ----------
show_help() {
    cat <<EOF
${C_BOLD}winget${C_NC} - Windows 程序包管理器 (Linux 整活版)

用法: winget <命令> [选项] [包名]

命令:
  install    <包名>     安装软件包
  uninstall  <包名>     卸载软件包
  search     <关键词>   搜索软件包
  list                  列出已安装的软件包
  upgrade    [包名]     升级软件包 (--all 升级全部)
  show       <包名>     显示软件包信息
  info                  显示 winget 版本信息
  help                  显示帮助信息

选项:
  -v, --version         显示底层包管理器版本
  -h, --help            显示帮助

当前后端: ${C_GREEN}${PM}${C_NC}
EOF
}

# ---------- install ----------
do_install() {
    extract_packages "$@"
    if [ -z "$PKGS" ]; then
        printf "${C_RED}错误: 未指定包名${C_NC}\n" >&2
        return 1
    fi
    printf "${C_BLUE}正在安装:${C_NC} %s\n" "$PKGS"
    case "$PM" in
        apt)
            if command -v apt >/dev/null 2>&1; then
                $SUDO apt install -y $PKGS
            else
                $SUDO apt-get install -y $PKGS
            fi
            ;;
        pacman)  $SUDO pacman -S --noconfirm $PKGS ;;
        dnf)     $SUDO dnf install -y $PKGS ;;
        yum)     $SUDO yum install -y $PKGS ;;
        zypper)  $SUDO zypper install -y $PKGS ;;
        apk)     $SUDO apk add $PKGS ;;
        xbps)    $SUDO xbps-install -y $PKGS ;;
        portage) $SUDO emerge $PKGS ;;
        brew)    brew install $PKGS ;;
    esac
}

# ---------- uninstall ----------
do_uninstall() {
    extract_packages "$@"
    if [ -z "$PKGS" ]; then
        printf "${C_RED}错误: 未指定包名${C_NC}\n" >&2
        return 1
    fi
    printf "${C_YELLOW}正在卸载:${C_NC} %s\n" "$PKGS"
    case "$PM" in
        apt)
            if command -v apt >/dev/null 2>&1; then
                $SUDO apt remove -y $PKGS
            else
                $SUDO apt-get remove -y $PKGS
            fi
            ;;
        pacman)  $SUDO pacman -Rns --noconfirm $PKGS ;;
        dnf)     $SUDO dnf remove -y $PKGS ;;
        yum)     $SUDO yum remove -y $PKGS ;;
        zypper)  $SUDO zypper remove -y $PKGS ;;
        apk)     $SUDO apk del $PKGS ;;
        xbps)    $SUDO xbps-remove -y $PKGS ;;
        portage) $SUDO emerge -C $PKGS ;;
        brew)    brew uninstall $PKGS ;;
    esac
}

# ---------- search ----------
do_search() {
    extract_packages "$@"
    if [ -z "$PKGS" ]; then
        printf "${C_RED}错误: 未指定搜索关键词${C_NC}\n" >&2
        return 1
    fi
    case "$PM" in
        apt)     apt search $PKGS ;;
        pacman)  pacman -Ss $PKGS ;;
        dnf)     dnf search $PKGS ;;
        yum)     yum search $PKGS ;;
        zypper)  zypper search $PKGS ;;
        apk)     apk search $PKGS ;;
        xbps)    xbps-query -Rs $PKGS ;;
        portage) emerge -s $PKGS ;;
        brew)    brew search $PKGS ;;
    esac
}

# ---------- list ----------
do_list() {
    case "$PM" in
        apt)
            if command -v apt >/dev/null 2>&1; then
                apt list --installed
            else
                dpkg -l
            fi
            ;;
        pacman)  pacman -Q ;;
        dnf)     dnf list installed ;;
        yum)     yum list installed ;;
        zypper)  zypper se -i ;;
        apk)     apk info ;;
        xbps)    xbps-query -l ;;
        portage)
            if command -v equery >/dev/null 2>&1; then
                equery l '*'
            else
                printf "${C_YELLOW}提示: 请安装 gentoolkit 以获取完整列表${C_NC}\n" >&2
                ls /var/db/pkg
            fi
            ;;
        brew)    brew list ;;
    esac
}

# ---------- 列出可升级的包 ----------
do_list_upgradable() {
    case "$PM" in
        apt)
            if command -v apt >/dev/null 2>&1; then
                apt list --upgradable
            else
                apt-get -s upgrade | grep -E '^[0-9a-zA-Z]'
            fi
            ;;
        pacman)  pacman -Qu ;;
        dnf)     dnf check-update ;;
        yum)     yum check-update ;;
        zypper)  zypper list-updates ;;
        apk)     apk version -l '<' ;;
        xbps)    xbps-install -un ;;
        portage) emerge -up --update @world ;;
        brew)    brew outdated ;;
    esac
}

# ---------- upgrade ----------
do_upgrade() {
    has_all=0
    for arg in "$@"; do
        [ "$arg" = "--all" ] && has_all=1
    done

    if [ "$has_all" -eq 1 ]; then
        printf "${C_BLUE}正在升级所有软件包...${C_NC}\n"
        case "$PM" in
            apt)
                if command -v apt >/dev/null 2>&1; then
                    $SUDO apt update && $SUDO apt upgrade -y
                else
                    $SUDO apt-get update && $SUDO apt-get upgrade -y
                fi
                ;;
            pacman)  $SUDO pacman -Syu ;;
            dnf)     $SUDO dnf upgrade -y ;;
            yum)     $SUDO yum update -y ;;
            zypper)  $SUDO zypper update -y ;;
            apk)     $SUDO apk upgrade ;;
            xbps)    $SUDO xbps-install -Su ;;
            portage) $SUDO emerge -uDN @world ;;
            brew)    brew upgrade ;;
        esac
    else
        extract_packages "$@"
        if [ -z "$PKGS" ]; then
            do_list_upgradable
        else
            printf "${C_BLUE}正在升级:${C_NC} %s\n" "$PKGS"
            case "$PM" in
                apt)
                    if command -v apt >/dev/null 2>&1; then
                        $SUDO apt install --only-upgrade -y $PKGS
                    else
                        $SUDO apt-get install --only-upgrade -y $PKGS
                    fi
                    ;;
                pacman)  $SUDO pacman -S $PKGS ;;
                dnf)     $SUDO dnf upgrade -y $PKGS ;;
                yum)     $SUDO yum update -y $PKGS ;;
                zypper)  $SUDO zypper update -y $PKGS ;;
                apk)     $SUDO apk add $PKGS ;;
                xbps)    $SUDO xbps-install -u $PKGS ;;
                portage) $SUDO emerge -u $PKGS ;;
                brew)    brew upgrade $PKGS ;;
            esac
        fi
    fi
}

# ---------- show ----------
do_show() {
    extract_packages "$@"
    if [ -z "$PKGS" ]; then
        printf "${C_RED}错误: 未指定包名${C_NC}\n" >&2
        return 1
    fi
    case "$PM" in
        apt)     apt show $PKGS ;;
        pacman)  pacman -Si $PKGS ;;
        dnf)     dnf info $PKGS ;;
        yum)     yum info $PKGS ;;
        zypper)  zypper info $PKGS ;;
        apk)     apk info -a $PKGS ;;
        xbps)    xbps-query -R $PKGS ;;
        portage) emerge -S $PKGS ;;
        brew)    brew info $PKGS ;;
    esac
}

# ---------- winget -v: 直接透传包管理器版本 ----------
do_pm_version() {
    case "$PM" in
        apt)
            if command -v apt >/dev/null 2>&1; then
                apt --version
            else
                apt-get --version
            fi
            ;;
        pacman)  pacman --version ;;
        dnf)     dnf --version ;;
        yum)     yum --version ;;
        zypper)  zypper --version ;;
        apk)     apk --version ;;
        xbps)    xbps-query --version ;;
        portage) emerge --version ;;
        brew)    brew --version ;;
    esac
}

# ---------- winget info: 输出 winget 版本信息 ----------
do_info() {
    DISTRO=$(get_distro)
    ARCH=$(uname -m)

    printf '+-------------+\n'
    printf '|      |      |  Linux Package Manager v%s\n' "$WINGET_VER"
    printf '|      |      |  Copyright (c) jihan_hanhan. MIT License.\n'
    printf '|  \   |   /  |\n'
    printf '|   \  |  /   |  Linux: %s\n' "$DISTRO"
    printf '|    \ | /    |  System Architecture: %s\n' "$ARCH"
    printf '|     \|/     |  Package: winget-linux v%s\n' "$WINGET_VER"
    printf '|      v      |\n'
    printf '+-------------+\n'
}

# ============================================================
#  主入口
# ============================================================
detect_pm
setup_sudo

if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

CMD="$1"
shift

case "$CMD" in
    install)            do_install "$@" ;;
    uninstall|remove)   do_uninstall "$@" ;;
    search)             do_search "$@" ;;
    list)               do_list ;;
    upgrade)            do_upgrade "$@" ;;
    show)               do_show "$@" ;;
    -v|--version)       do_pm_version ;;
    info|--info)        do_info ;;
    -h|--help|help)     show_help ;;
    *)
        printf "${C_RED}未知命令: %s${C_NC}\n" "$CMD" >&2
        printf "运行 'winget help' 查看帮助\n" >&2
        exit 1
        ;;
esac