-- bootstrap lazy.nvim, LazyVim and your plugins
require("config.lazy")
-- 切换粘贴模式
vim.keymap.set("n", "<F9>", function()
  if vim.o.paste then
    vim.o.paste = false
    print("粘贴模式关闭")
  else
    vim.o.paste = true
    print("粘贴模式开启")
  end
end, { desc = "Toggle paste mode" })

require("mason-lspconfig").setup({
  ensure_installed = {}, -- 清空自动安装列表
})
-- catppuccin
vim.cmd.colorscheme("catppuccin")

