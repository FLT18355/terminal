代码中的 bug 是：`calculate_area` 函数计算的是**圆的周长**（`2 * π * r`），而不是**圆的面积**（`π * r²`）。

修复后的代码：

```python
def calculate_area(radius):
    return 3.14 * radius * radius
```
