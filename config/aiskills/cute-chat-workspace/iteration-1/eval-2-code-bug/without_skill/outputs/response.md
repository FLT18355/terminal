# Bug 分析与修复

## 问题

代码中 `calculate_area(radius)` 的作用是**计算圆的面积**，但公式错误地使用了 `2 * 3.14 * radius`。

```
2 * π * r
```

这个公式实际上是**圆的周长**，而非面积。

## 修复

圆的面积公式应为：**π × r²**

```python
def calculate_area(radius):
    return 3.14 * radius * radius
```

> 更推荐使用 `math.pi` 替代硬编码的 `3.14`，以获得更高精度。
>
> ```python
> import math
>
> def calculate_area(radius):
>     return math.pi * radius ** 2
> ```
