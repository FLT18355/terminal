return {
  {
    "catppuccin/nvim",
    name = "catppuccin",
    priority = 1000,
    opts = {
      flavour = "mocha", -- latte, frappe, macchiato, mocha
      transparent_background = false,
      term_colors = true,
      integrations = {
              neotree = true, -- 启用对 NeoTree 的集成支持
              blink_cmp = true,
      },
    },
  },
}
