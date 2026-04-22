-- ~/.config/nvim/lua/plugins/blink.lua
return {
  {
    "saghen/blink.cmp",
    opts = {
      -- 确保补全菜单显示图标
      completion = {
        menu = {
          draw = {
            columns = {
              { "kind_icon" },  -- 必须有这一列
              { "label", "label_description", gap = 1 },
              { "source_name" },
            },
          },
        },
      },
    },
  },
}
