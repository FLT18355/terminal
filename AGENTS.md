# AGENTS.md — FLT18355/terminal

Personal dotfiles repo (Catppuccin Mocha themed) for Arch Linux (NyarchOS), Debian, and Termux (Android). Version `1.2.1`.

## Structure

- `config/arch/` — Arch Linux system/home configs, logos, wallpaper
- `config/debian/` — Debian apt sources, home dotfiles, system themes
- `config/scripts/{mc,terminal}/` — Utility scripts (Python/Node.js)
- `config/web/` — Catppuccin JS userstyles (GitHub, Neovim-io, YouTube)
- `config/help/lazyvim.md` — LazyVim install guide
- `termux/` — Termux (Android) dotfiles (zsh, tmux, properties, colors)
- `nvim/` — NeoVim config built on **LazyVim** (init.lua bootstraps `config.lazy`)
- `bin/` — CLI tools: `7zf`, `gits`, `unf`, `list-packages`
- `subdir/` — **Git submodule** → `FLT18355/My-Catppuccin-Userstyles`
- `developer/setup_test.sh` — Arch Linux dev environment bootstrap (requires sudo)
- `images/` — Wallpapers & ANSI art
- `.bashrc` — Only bootstraps x-cmd

## Key commands

| Tool | What it does |
|------|-------------|
| `bin/7zf` | Smart 7z wrapper (compress/extract/list/test/hash) |
| `bin/gits` | GitHub download/sync tool (clone folders/files, push/pull) |
| `bin/unf` | Universal extractor (tar.*, zip, 7z, rar, xz, bz2, zst, lz4, gz) |
| `bin/list-packages` | Arch Linux package lister (JSON output, detects AUR vs official) |

## Submodule

```
cd subdir && git pull origin main
```

## Neovim

- LazyVim framework, extra `lazyvim.plugins.extras.lang.python`
- Catppuccin Mocha colorscheme
- `<F2>` formats Python via `ruff`, `<F9>` toggles paste mode
- stylua config: 2-space indent, 120 col width
- Mason auto-install list explicitly emptied (`ensure_installed = {}`)

## Important notes

- `setup.sh` (anywhere) is **half-finished — do not use**
- Root `.bashrc` only loads x-cmd; real shell configs are platform-specific under `config/`
- No package.json, no CI, no tests, no lint/typecheck setup — this is a flat dotfiles collection
- All configs use Catppuccin Mocha palette
- Repo URL: `https://github.com/FLT18355/terminal.git`
