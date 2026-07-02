# ============================================
# FZF 配置
# ============================================

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
