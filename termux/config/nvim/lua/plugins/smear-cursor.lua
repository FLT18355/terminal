return {
  "sphamba/smear-cursor.nvim",
  opts = {
    -- 基础开关
    smear_between_buffers = true,
    smear_between_neighbor_lines = true,
    scroll_buffer_space = true,
    smear_insert_mode = true,

    -- 插入模式下使用竖线光标时的处理（Termux 终端通常用竖线）
    vertical_bar_cursor_insert_mode = true,  -- 如果设为 true，插入模式不显示拖尾
    distance_stop_animating_vertical_bar = 2, -- 光标移动超过多少字符时停止拖尾动画

    -- 拖尾动画的"手感"参数
    stiffness = 0.9,           -- 光标硬度（0-1，越高越跟手）
    trailing_stiffness = 0.5,  -- 拖尾部分的硬度
    damping = 0.95,            -- 阻尼（越高动画停止越慢，越有"惯性"）
    damping_insert_mode = 0.9, -- 插入模式的阻尼

    -- 最小移动距离（低于这个距离不显示拖尾，避免短距离移动过于花哨）
    min_horizontal_distance_smear = 0,  -- 最小水平距离
    min_vertical_distance_smear = 0,    -- 最小垂直距离

    -- 字体兼容（如果你用 Nerd Font，保持 false 即可）
    legacy_computing_symbols_support = false,

    -- 刷新间隔（毫秒，越低动画越流畅，但 CPU 占用稍高）
    time_interval = 10,

    -- 光标颜色（可选，让拖尾颜色固定）
    -- cursor_color = nil,  -- 设为 "#cba6f7" 可以固定成 Catppuccin 紫色
    cursor_color = "#89b4fa",
  },
}
