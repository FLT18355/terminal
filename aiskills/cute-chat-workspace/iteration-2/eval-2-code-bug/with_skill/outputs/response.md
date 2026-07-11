嗯... 这道代码有一个小小的bug呢～ (・◇・)

## 问题分析

`calculate_area` 函数现在的公式是 `2 * 3.14 * radius`，算出来的是**圆的周长**，而不是面积哦！(๑˘ﻬ˘๑)

圆的面积公式应该是：**π × r²**

## 修复后的代码

```python
def calculate_area(radius):
    return 3.14 * radius * radius
```

或者写成这样更清晰：

```python
def calculate_area(radius):
    area = 3.14 * radius ** 2
    return area
```

这样就能正确返回圆的面积啦！(☆ω☆)

---

顺便说一下，Python 里可以用 `math.pi` 获得更精确的 π 值哦：

```python
import math

def calculate_area(radius):
    return math.pi * radius ** 2
```

搞定啦～ 代码现在工作正常啦喵！(≧◡≦)

