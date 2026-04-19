-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here
vim.opt.guicursor = "i:ver25"
-- 开启自动换行
vim.opt.wrap = true

-- 设置换行边界（可选，默认80列）
vim.opt.textwidth = 0

-- 换行时自动缩进
vim.opt.breakindent = true

-- 换行时显示的对齐符号（可选）
vim.opt.showbreak = "↪ "
