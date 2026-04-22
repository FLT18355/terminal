return {
  "folke/snacks.nvim",
  opts = {
    zen = {
      enabled = true,
      -- 全屏配置
      win = {
        width = vim.o.columns,   -- 宽度设为终端全宽
        height = vim.o.lines,    -- 高度设为终端全高
        backdrop = {
          transparent = false,   -- 背景不透明
          blend = 0,             -- 透明度为 0
        },
      },
      -- 隐藏的界面元素
      toggles = {
        number = true,           -- 隐藏行号
        relativenumber = true,   -- 隐藏相对行号
        signcolumn = true,       -- 隐藏符号列
        tabline = true,          -- 隐藏标签栏
        statusline = true,       -- 隐藏状态栏
        foldcolumn = true,       -- 隐藏折叠列
        laststatus = true,       -- 隐藏最后状态栏
      },
    },
  },
}
