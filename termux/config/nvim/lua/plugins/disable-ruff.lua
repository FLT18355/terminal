return {
  {
    "mason-org/mason-lspconfig.nvim",
    opts = {
      ensure_installed = {
        -- 这里列出你真正需要的其他 LSP 服务器（如 pyright）
        "pyright",
      },
    },
  },
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        ruff = {
          mason = false, -- 关键：告诉 LazyVim 不要让 mason 管理 ruff
        },
      },
    },
  },
}
