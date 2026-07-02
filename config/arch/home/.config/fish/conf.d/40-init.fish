# ============================================
# 插件初始化 & 主题 & 启动信息
# ============================================

fzf --fish | source
eval "$(starship init fish)"
fish_config theme choose catppuccin-mocha

# Carapace 补全 (未启用)
# carapace _carapace | source

# Zoxide (未启用)
# zoxide init fish | source

# Vi 模式 (默认禁用)
# set -g fish_key_bindings fish_vi_key_bindings

# Termux API (默认禁用)
# am start com.termux.api/com.termux.api.activities.TermuxAPIMainActivity

set fish_greeting
ffc
