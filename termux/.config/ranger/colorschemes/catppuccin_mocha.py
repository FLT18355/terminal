# Catppuccin Mocha 配色方案
from ranger.gui.colorscheme import ColorScheme
from ranger.gui.color import *

class CatppuccinMocha(ColorScheme):
    def use(self, context):
        fg, bg, attr = default_colors

        # 基础色
        if context.reset:
            pass
        elif context.in_browser:
            if context.selected:
                fg = 218  # 粉色
                bg = 237  # surface1
                attr = bold
            elif context.directory:
                fg = 75   # 蓝色
                attr = bold
            elif context.link:
                fg = 147  # 薰衣草
            elif context.executable:
                fg = 157  # 绿色
                attr = bold
            else:
                fg = 253  # 文本色
        elif context.in_statusbar:
            if context.permissions:
                fg = 157
            elif context.marked:
                fg = 218
        elif context.in_titlebar:
            if context.hostname:
                fg = 75
            elif context.directory:
                fg = 75
            elif context.tab:
                if context.good:
                    fg = 157
                elif context.bad:
                    fg = 210
                else:
                    fg = 253
        elif context.in_console:
            if context.input:
                fg = 253
        elif context.in_pager:
            if context.help:
                fg = 75

        return fg, bg, attr
