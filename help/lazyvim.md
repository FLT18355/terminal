## lazyvim 安装指南

- 前置要求
  - Neovim ≥ 0.9.0
  - Git
  - Nerd Font
    - 推荐maple mono NF CN
  - C 编译器

检查环境

```bash
nvim --version        # 确认 Neovim 版本 ≥ 0.9.0
git --version         # 确认 Git 已安装
```

第一步：备份现有配置（重要！）

如果你已有 Neovim 配置，先备份以防丢失：

```bash
# 备份主配置目录（必须）
mv ~/.config/nvim ~/.config/nvim.bak

# 备份数据/缓存目录（推荐）
mv ~/.local/share/nvim ~/.local/share/nvim.bak
mv ~/.local/state/nvim ~/.local/state/nvim.bak
mv ~/.cache/nvim ~/.cache/nvim.bak
```

第二步：克隆 LazyVim 启动模板

```bash
git clone https://github.com/LazyVim/starter ~/.config/nvim

# 删除 .git 文件夹，方便你后续用自己的 Git 仓库管理配置
rm -rf ~/.config/nvim/.git
```

第三步：启动 Neovim

```bash
nvim
```

首次启动时，LazyVim 会自动下载并安装所有依赖插件(会黑屏一段时间)，这个过程可能需要 2-3 分钟，请耐心等待。安装完成后你会看到 LazyVim 的启动界面。

🎯 安装后验证

运行以下命令检查插件是否正确加载：

```vim
:Lazy              " 打开插件管理界面，查看插件状态
:LazyHealth        " 检查环境健康度，确认是否有缺失依赖
:checkhealth       " 全面检查 Neovim 环境
```

⚙️ 目录结构

```
~/.config/nvim/
├── lua/
│   ├── config/           # 基础配置
│   │   ├── options.lua   # 编辑器选项（行号、缩进等）
│   │   ├── keymaps.lua   # 快捷键设置
│   │   └── autocmds.lua  # 自动命令
│   └── plugins/          # 插件配置（按文件单独配置）
└── init.lua              # 入口文件
```

💡 LazyVim 的模块化设计让你可以按需增删功能，既不会臃肿，也保留了灵活性。

🔧 常见问题

1. 图标显示为方框？

说明终端字体不是 Nerd Font。解决方法：

· 下载安装 Nerd Fonts（推荐 JetBrainsMono Nerd Font）
· 在终端设置中配置使用该字体

2. 插件安装失败？

可能是网络问题，尝试：

```bash
rm -rf ~/.local/share/nvim/lazy   # 清理插件缓存
nvim                               # 重新安装
```

3. treesitter 报错缺少 C 编译器？

安装 build-essential（Debian/Ubuntu）：

```bash
sudo apt install build-essential -y
```

4. 如何更新 LazyVim？

在 Neovim 中执行：

```vim
:Lazy sync
```

5. 关于我的配置使用问题

直接复制就行(可能会出一点小小的问题)

💡 下一步

安装完成后，你可以：

1. 按 <space> 键查看所有快捷键（LazyVim 内置 which-key 提示）
2. 编辑 ~/.config/nvim/lua/plugins/colorscheme.lua 切换主题
3. 在 lua/plugins/ 下新建 .lua 文件添加自己的插件配置

享受你的 LazyVim 之旅吧！🎉
