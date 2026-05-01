return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        lua_ls = {
          mason = false,  -- 禁用 Mason 管理 lua-language-server
        },
      },
    },
  },
  {
    "stevearc/conform.nvim",
    opts = {
      formatters_by_ft = {
        lua = {},  -- 清空 Lua 的格式化工具，stylua 就不会被安装了
      },
    },
  },
}
