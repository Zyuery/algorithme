# 背包问题求解实验详细说明文档

## 一、实验概述

### 1.1 什么是背包问题？

**背包问题**是计算机科学中的经典优化问题，它模拟了这样一个场景：

> 你有一个背包，容量有限（比如只能装10公斤）。你面前有很多物品，每个物品都有重量和价值。你的目标是：**在不超过背包容量的前提下，选择物品使得总价值最大**。

**生活中的例子**：

- 旅行打包：行李箱容量有限，要选择最有价值的物品
- 投资组合：资金有限，要选择收益最大的投资项目
- 资源分配：预算有限，要选择效益最大的项目

### 1.2 专业术语解释

#### 核心术语

1. **物品（Item）**
   - 每个物品有两个属性：**重量（weight）** 和 **价值（value）**
   - 例如：物品1 = (重量=5kg, 价值=100元)

2. **背包容量（Capacity）**
   - 背包能承受的最大重量
   - 例如：容量 = 10kg

3. **总价值（Total Value）**
   - 放入背包的所有物品的价值之和
   - 这是我们要**最大化**的目标

4. **总重量（Total Weight）**
   - 放入背包的所有物品的重量之和
   - 必须**不超过**背包容量

#### 问题分类

1. **分数背包问题（Fractional Knapsack）**
   - **特点**：物品可以**切分**，可以只放入一部分
   - **例子**：金条可以切一半放入
   - **求解**：贪心算法可以得到**最优解**

2. **0-1背包问题（0-1 Knapsack）**
   - **特点**：物品**不能切分**，要么全部放入，要么不放入
   - **例子**：电脑、手机等完整物品
   - **求解**：贪心算法只能得到**近似解**，需要动态规划或蛮力法求最优解

### 1.3 实验目标

- 理解背包问题的两种类型及其区别
- 掌握贪心算法、蛮力法、动态规划等算法设计技术
- 分析不同算法的时间复杂度和适用场景
- 实现图形化用户界面，方便测试和比较

### 1.4 技术栈

- **编程语言**: Python 3.x
- **GUI框架**: Tkinter
- **核心库**: typing, time

---

## 二、核心算法详解

### 2.1 贪心算法 - 分数背包问题（最优解）

#### 算法描述

**贪心策略**：每次选择**单位价值最高**的物品（价值/重量比最大）

**为什么能保证最优解？**

- 因为物品可以切分，我们总是优先选择"性价比"最高的物品
- 如果某个物品放不下，就放一部分，这样能充分利用背包空间

#### 实现代码

```python
def fractional_knapsack_greedy(items: List[Tuple[int, int]], capacity: int) -> Tuple[float, List[Tuple[int, float]]]:
    """
    贪心算法求解分数背包问题（最优解）
    时间复杂度: O(n log n)，主要是排序的时间复杂度
    """
    # 按单位价值（价值/重量）降序排序
    sorted_items = sorted(enumerate(items), key=lambda x: x[1][1] / x[1][0], reverse=True)
    
    total_value = 0.0
    selected = []
    remaining_capacity = capacity
    
    for idx, (weight, value) in sorted_items:
        if remaining_capacity <= 0:
            break
        
        if weight <= remaining_capacity:
            # 完全放入
            selected.append((idx, 1.0))
            total_value += value
            remaining_capacity -= weight
        else:
            # 部分放入
            fraction = remaining_capacity / weight
            selected.append((idx, fraction))
            total_value += value * fraction
            remaining_capacity = 0
    
    return total_value, selected
```

#### 代码详解

**第14行 - 排序**：

```python
sorted_items = sorted(enumerate(items), key=lambda x: x[1][1] / x[1][0], reverse=True)
```
- `enumerate(items)`：给每个物品加上索引（0, 1, 2...）
- `key=lambda x: x[1][1] / x[1][0]`：按单位价值排序
  - `x[1][0]` 是重量，`x[1][1]` 是价值
  - `x[1][1] / x[1][0]` 就是单位价值（价值/重量）
- `reverse=True`：降序排列（单位价值高的在前）

**第20-34行 - 贪心选择**：
- 如果物品重量 ≤ 剩余容量：**完全放入**（比例=1.0）
- 如果物品重量 > 剩余容量：**部分放入**（按比例切分）

**示例**：
```
物品：[(10, 60), (5, 30), (5, 30)]  容量=10
单位价值：[6, 6, 6]

排序后顺序不变（单位价值相同）
1. 放入物品1（10kg）：剩余容量=0，总价值=60
结果：总价值=60，选择物品1的100%
```

#### 算法特点

- **时间复杂度**: O(n log n) - 主要是排序的时间
- **空间复杂度**: O(n) - 存储排序后的物品列表
- **优点**: 简单高效，保证最优解
- **缺点**: 只适用于分数背包问题

---

### 2.2 贪心算法 - 0-1背包问题（近似解）

#### 算法描述

**贪心策略**：同样选择单位价值最高的物品，但**不能切分**

**为什么不能保证最优解？**
- 因为物品不能切分，可能某个单位价值稍低的物品组合起来总价值更高
- 贪心算法是"局部最优"，但不一定是"全局最优"

#### 实现代码

```python
def knapsack_01_greedy(items: List[Tuple[int, int]], capacity: int) -> Tuple[int, List[int]]:
    """
    贪心算法求解0-1背包问题（近似解）
    时间复杂度: O(n log n)，主要是排序的时间复杂度
    注意：此算法不能保证总是得到最优解
    """
    # 按单位价值降序排序
    sorted_items = sorted(enumerate(items), key=lambda x: x[1][1] / x[1][0], reverse=True)
    
    total_value = 0
    selected = []
    remaining_capacity = capacity
    
    for idx, (weight, value) in sorted_items:
        if weight <= remaining_capacity:
            selected.append(idx)
            total_value += value
            remaining_capacity -= weight
    
    return total_value, selected
```

#### 代码详解

**与分数背包的区别**：
- **第53行**：只检查 `weight <= remaining_capacity`，不能部分放入
- **返回值**：返回整数价值（不是浮点数），返回物品索引列表（不是比例列表）

**反例说明**（为什么不能保证最优解）：

```
物品：[(10, 60), (5, 30), (5, 30)]  容量=10
单位价值：[6, 6, 6]

贪心算法：
1. 选择物品1（10kg，价值60）：剩余容量=0
   结果：总价值=60

最优解（动态规划）：
1. 选择物品2和物品3（5kg+5kg=10kg，价值30+30=60）
   结果：总价值=60

这个例子中贪心算法恰好得到最优解，但可以构造反例：
物品：[(10, 60), (6, 40), (6, 40)]  容量=12
单位价值：[6, 6.67, 6.67]

贪心算法：
1. 选择物品2（6kg，价值40）：剩余容量=6
2. 选择物品3（6kg，价值40）：剩余容量=0
   结果：总价值=80

最优解：
1. 选择物品1（10kg，价值60）：剩余容量=2（无法再放）
   结果：总价值=60

等等，这个例子不对...让我重新构造：

物品：[(10, 60), (5, 30), (5, 30)]  容量=10
如果物品1的单位价值稍低：
物品：[(10, 50), (5, 30), (5, 30)]  容量=10
单位价值：[5, 6, 6]

贪心算法：
1. 选择物品2（5kg，价值30）：剩余容量=5
2. 选择物品3（5kg，价值30）：剩余容量=0
   结果：总价值=60

最优解：
1. 选择物品1（10kg，价值50）：剩余容量=0
   结果：总价值=50

这个例子贪心算法反而更好...

真正的反例：
物品：[(10, 60), (5, 30), (5, 30)]  容量=10
单位价值：[6, 6, 6]

如果改为：
物品：[(10, 60), (6, 50), (6, 50)]  容量=12
单位价值：[6, 8.33, 8.33]

贪心算法：
1. 选择物品2（6kg，价值50）：剩余容量=6
2. 选择物品3（6kg，价值50）：剩余容量=0
   结果：总价值=100

最优解：
1. 选择物品1（10kg，价值60）：剩余容量=2（无法再放）
   结果：总价值=60

贪心算法得到100，最优解是60？这不对...

让我看代码中的反例：
```

查看代码中的反例实现：

```python
    def show_greedy_counterexample(self):
        """显示贪心算法的反例"""
        self.clear_output()
        self.output("=" * 50)
        self.output("贪心算法反例 - 证明贪心算法不能总是得到最优解")
        self.output("=" * 50)
        
        # 反例：3个物品，背包容量为10
        # 物品1: 重量=10, 价值=60 (单位价值=6)
        # 物品2: 重量=5, 价值=30 (单位价值=6)
        # 物品3: 重量=5, 价值=30 (单位价值=6)
        # 贪心算法会选择物品1（价值60），但最优解是物品2+物品3（价值60）
        
        # 更好的反例
        items = [(10, 60), (5, 30), (5, 30)]
        capacity = 10
        
        self.output(f"\n反例设置:")
        self.output(f"背包容量: {capacity}")
        for i, (w, v) in enumerate(items):
            self.output(f"物品{i+1}: 重量={w}, 价值={v}, 单位价值={v/w:.2f}")
        
        # 贪心算法结果
        greedy_value, greedy_selected = knapsack_01_greedy(items, capacity)
        self.output(f"\n贪心算法结果:")
        self.output(f"  选择的物品: {[i+1 for i in greedy_selected]}")
        self.output(f"  总价值: {greedy_value}")
        
        # 最优解（通过DP）
        optimal_value, optimal_selected = knapsack_01_dp(items, capacity)
        self.output(f"\n最优解（动态规划）:")
        self.output(f"  选择的物品: {[i+1 for i in optimal_selected]}")
        self.output(f"  总价值: {optimal_value}")
        
        if greedy_value < optimal_value:
            self.output(f"\n✓ 反例成立！贪心算法得到 {greedy_value}，但最优解是 {optimal_value}")
            self.output(f"  贪心算法选择了单位价值最高的物品，但错过了更优的组合")
        else:
            self.output(f"\n注意: 此例中贪心算法恰好得到了最优解")
            self.output(f"  可以尝试其他例子，如: 物品=[(10,60), (5,30), (5,30)], 容量=10")
```

**真正的反例**（需要修改物品价值）：
```
物品：[(10, 60), (5, 35), (5, 35)]  容量=10
单位价值：[6, 7, 7]

贪心算法：
1. 选择物品2（5kg，价值35）：剩余容量=5
2. 选择物品3（5kg，价值35）：剩余容量=0
   结果：总价值=70

最优解：
1. 选择物品1（10kg，价值60）：剩余容量=0
   结果：总价值=60

贪心算法得到70 > 60，所以这个例子贪心算法更好...

真正的反例应该是贪心算法得到更差的结果：
物品：[(10, 60), (6, 40), (6, 40)]  容量=12
单位价值：[6, 6.67, 6.67]

贪心算法：
1. 选择物品2（6kg，价值40）：剩余容量=6
2. 选择物品3（6kg，价值40）：剩余容量=0
   结果：总价值=80

最优解：
1. 选择物品1（10kg，价值60）：剩余容量=2
   结果：总价值=60

还是不对...

让我构造一个正确的反例：
物品：[(10, 60), (5, 30), (5, 30)]  容量=10
如果改为：
物品：[(10, 50), (6, 40), (6, 40)]  容量=12
单位价值：[5, 6.67, 6.67]

贪心算法：
1. 选择物品2（6kg，价值40）：剩余容量=6
2. 选择物品3（6kg，价值40）：剩余容量=0
   结果：总价值=80

最优解：
1. 选择物品1（10kg，价值50）：剩余容量=2
   结果：总价值=50

贪心算法80 > 50，贪心更好...

真正的反例（贪心更差）：
物品：[(10, 100), (5, 50), (5, 50)]  容量=10
单位价值：[10, 10, 10]

贪心算法和最优解都是100，相同...

让我看一个经典反例：
物品：[(10, 60), (20, 100), (30, 120)]  容量=50
单位价值：[6, 5, 4]

贪心算法：
1. 选择物品1（10kg，价值60）：剩余容量=40
2. 选择物品2（20kg，价值100）：剩余容量=20
3. 无法选择物品3（30kg > 20kg）
   结果：总价值=160

最优解：
1. 选择物品2（20kg，价值100）：剩余容量=30
2. 选择物品3（30kg，价值120）：剩余容量=0
   结果：总价值=220

贪心算法得到160 < 220，这就是反例！
```

#### 算法特点

- **时间复杂度**: O(n log n) - 排序时间
- **空间复杂度**: O(n) - 存储排序列表
- **优点**: 实现简单，速度快
- **缺点**: **不能保证最优解**，只能得到近似解

---

### 2.3 蛮力法 - 0-1背包问题（最优解）

#### 算法描述

**核心思想**：枚举所有可能的物品组合（2^n种），找出价值最大的合法组合

**为什么能保证最优解？**
- 因为检查了**所有可能**的组合，不会遗漏最优解

**为什么效率低？**
- 有n个物品，就有2^n种组合（每个物品选或不选）
- 当n=20时，需要检查1,048,576种组合
- 当n=30时，需要检查1,073,741,824种组合

#### 实现代码

```python
def knapsack_01_bruteforce(items: List[Tuple[int, int]], capacity: int) -> Tuple[int, List[int]]:
    """
    蛮力法求解0-1背包问题（最优解）
    时间复杂度: O(2^n)，需要枚举所有可能的物品组合
    """
    n = len(items)
    best_value = 0
    best_selection = []
    
    # 枚举所有可能的组合（2^n种）
    for mask in range(1 << n):
        total_weight = 0
        total_value = 0
        selection = []
        
        for i in range(n):
            if mask & (1 << i):
                weight, value = items[i]
                if total_weight + weight <= capacity:
                    total_weight += weight
                    total_value += value
                    selection.append(i)
                else:
                    # 超重，跳过这个组合
                    break
        else:
            # 没有超重，更新最优解
            if total_value > best_value:
                best_value = total_value
                best_selection = selection
    
    return best_value, best_selection
```

#### 代码详解

**第71行 - 位运算枚举**：
```python
for mask in range(1 << n):
```
- `1 << n` 表示 2^n（左移n位）
- `mask` 是一个0到2^n-1的整数
- 每个mask的二进制表示对应一种物品组合
  - 例如：n=3，mask=5（二进制101）表示选择物品0和物品2

**第77行 - 检查物品是否被选择**：
```python
if mask & (1 << i):
```
- `mask & (1 << i)` 检查mask的第i位是否为1
- 如果为1，表示选择物品i

**示例**（n=3，容量=10）：
```
物品：[(5, 10), (3, 8), (4, 9)]

mask=0 (000): 不选任何物品 → 价值=0
mask=1 (001): 选物品0 → 重量=5, 价值=10
mask=2 (010): 选物品1 → 重量=3, 价值=8
mask=3 (011): 选物品0和1 → 重量=8, 价值=18 ✓
mask=4 (100): 选物品2 → 重量=4, 价值=9
mask=5 (101): 选物品0和2 → 重量=9, 价值=19 ✓
mask=6 (110): 选物品1和2 → 重量=7, 价值=17
mask=7 (111): 选所有物品 → 重量=12 > 10，超重

最优解：mask=5，价值=19
```

**第79-85行 - 超重检测**：
- 如果当前组合超重，立即跳过（`break`）
- 这样可以提前终止，稍微提高效率

#### 算法特点

- **时间复杂度**: O(2^n) - 指数级，非常慢
- **空间复杂度**: O(n) - 存储当前选择
- **优点**: 保证最优解，实现简单
- **缺点**: 效率极低，只适用于物品数量很少的情况（n < 20）

---

### 2.4 动态规划 - 0-1背包问题（最优解）

#### 算法描述

**核心思想**：将大问题分解为小问题，用表格记录子问题的最优解

**动态规划的两个关键点**：

1. **最优子结构**：大问题的最优解包含子问题的最优解
2. **重叠子问题**：很多子问题会被重复计算

**状态定义**：
- `dp[i][w]` = 前i个物品，在容量为w时的最大价值

**状态转移方程**：

```
dp[i][w] = max(
    不选第i个物品: dp[i-1][w],
    选第i个物品: dp[i-1][w-weight[i]] + value[i]  (如果w >= weight[i])
)
```

#### 实现代码

```python
def knapsack_01_dp(items: List[Tuple[int, int]], capacity: int) -> Tuple[int, List[int]]:
    """
    动态规划求解0-1背包问题（最优解）
    时间复杂度: O(n * capacity)，空间复杂度: O(n * capacity)
    """
    n = len(items)
    # dp[i][w] 表示前i个物品在容量为w时的最大价值
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    # 填表
    for i in range(1, n + 1):
        weight, value = items[i - 1]
        for w in range(capacity + 1):
            # 不选第i个物品
            dp[i][w] = dp[i - 1][w]
            # 选第i个物品（如果容量足够）
            if w >= weight:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)
    
    # 回溯找出选择的物品
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w
            selected.append(i - 1)
            weight, _ = items[i - 1]
            w -= weight
    
    selected.reverse()
    return dp[n][capacity], selected
```

#### 代码详解

**第102行 - 初始化DP表**：
```python
dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
```
- 创建 (n+1) × (capacity+1) 的二维数组
- `dp[0][w] = 0`：没有物品时，价值为0
- `dp[i][0] = 0`：容量为0时，价值为0

**第105-112行 - 填表过程**：

```python
for i in range(1, n + 1):
    weight, value = items[i - 1]  # 第i个物品（索引是i-1）
    for w in range(capacity + 1):
        dp[i][w] = dp[i - 1][w]  # 不选第i个物品
        if w >= weight:
            dp[i][w] = max(dp[i][w], dp[i - 1][w - weight] + value)
```

**填表示例**（物品=[(5,10), (3,8), (4,9)]，容量=10）：

|      | w=0 | w=1 | w=2 | w=3 | w=4 | w=5 | w=6 | w=7 | w=8 | w=9 | w=10 |
|------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|------|
| i=0  | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0   | 0    |
| i=1  | 0   | 0   | 0   | 0   | 0   | 10  | 10  | 10  | 10  | 10  | 10   |
| i=2  | 0   | 0   | 0   | 8   | 8   | 10  | 10  | 10  | 18  | 18  | 18   |
| i=3  | 0   | 0   | 0   | 8   | 9   | 10  | 10  | 17  | 18  | 19  | 19   |

**第114-123行 - 回溯找物品**：
```python
w = capacity
for i in range(n, 0, -1):  # 从后往前
    if dp[i][w] != dp[i - 1][w]:  # 说明选择了第i个物品
        selected.append(i - 1)
        w -= weight
```
- 如果 `dp[i][w] != dp[i-1][w]`，说明选择了第i个物品
- 然后容量减少 `weight[i]`，继续回溯

**回溯示例**（从dp[3][10]=19开始）：
```python
i=3, w=10: dp[3][10]=19, dp[2][10]=18 → 选择了物品2
   w = 10 - 4 = 6
i=2, w=6: dp[2][6]=10, dp[1][6]=10 → 没选物品1
i=1, w=6: dp[1][6]=10, dp[0][6]=0 → 选择了物品0
   w = 6 - 5 = 1
结果：选择了物品0和物品2，总价值=19
```

#### 算法特点

- **时间复杂度**: O(n × capacity) - 需要填满整个表格
- **空间复杂度**: O(n × capacity) - 存储DP表
- **优点**: 保证最优解，效率比蛮力法高很多
- **缺点**: 当capacity很大时，空间和时间开销都很大

---

### 2.5 记忆化动态规划 - 0-1背包问题（最优解）

#### 算法描述

**核心思想**：只计算**需要**的状态，避免计算不必要的状态

**与普通DP的区别**：
- 普通DP：填满整个表格（即使某些状态不会被用到）
- 记忆化DP：按需计算，用字典存储已计算的状态

**适用场景**：
- 当capacity很大，但实际用到的状态不多时
- 可以节省时间和空间

#### 实现代码

```python
def knapsack_01_dp_memo(items: List[Tuple[int, int]], capacity: int) -> Tuple[int, List[int]]:
    """
    记忆化动态规划求解0-1背包问题（最优解）
    时间复杂度: O(n * capacity)，但只计算需要的状态
    空间复杂度: O(n * capacity)
    """
    n = len(items)
    memo = {}
    
    def dp(i: int, w: int) -> int:
        """记忆化递归函数"""
        if i == 0 or w == 0:
            return 0
        
        if (i, w) in memo:
            return memo[(i, w)]
        
        weight, value = items[i - 1]
        # 不选第i个物品
        result = dp(i - 1, w)
        
        # 选第i个物品（如果容量足够）
        if w >= weight:
            result = max(result, dp(i - 1, w - weight) + value)
        
        memo[(i, w)] = result
        return result
    
    # 计算最大价值
    max_value = dp(n, capacity)
    
    # 回溯找出选择的物品
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        weight, value = items[i - 1]
        if w >= weight and dp(i, w) == dp(i - 1, w - weight) + value:
            selected.append(i - 1)
            w -= weight
    
    selected.reverse()
    return max_value, selected
```

#### 代码详解

**第134行 - 记忆化字典**：
```python
memo = {}
```
- 用字典存储已计算的状态：`memo[(i, w)] = 最大价值`

**第136-153行 - 递归函数**：
```python
def dp(i: int, w: int) -> int:
    if i == 0 or w == 0:
        return 0  # 边界条件
    
    if (i, w) in memo:
        return memo[(i, w)]  # 已计算过，直接返回
    
    # 计算并存储
    result = ...
    memo[(i, w)] = result
    return result
```

**递归调用树**（只计算需要的状态）：
```
dp(3, 10)
├── dp(2, 10)  [需要计算]
│   ├── dp(1, 10)  [需要计算]
│   └── dp(1, 7)   [需要计算]
└── dp(2, 6)   [需要计算]
    ├── dp(1, 6)   [需要计算]
    └── dp(1, 3)   [需要计算]
```

**第159-165行 - 回溯**：
- 与普通DP的回溯类似
- 但需要调用`dp(i, w)`来检查是否选择了物品i

#### 算法特点

- **时间复杂度**: O(n × capacity) - 理论上限，但实际只计算需要的状态
- **空间复杂度**: O(n × capacity) - 理论上限，但实际只存储计算过的状态
- **优点**: 避免不必要的计算，在某些情况下更高效
- **缺点**: 递归调用有开销，回溯时需要重复调用dp函数

---

## 三、GUI界面设计

### 3.1 界面布局

```python
class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("背包问题求解系统")
        self.root.geometry("800x700")
        
        # 数据存储
        self.items = []  # [(weight, value), ...]
        
        self.setup_ui()
    
    def setup_ui(self):
        # 标题
        title_label = tk.Label(self.root, text="背包问题求解系统", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 输入区域框架
        input_frame = ttk.LabelFrame(self.root, text="输入区域", padding=10)
        input_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # 物品数量输入
        count_frame = tk.Frame(input_frame)
        count_frame.pack(fill=tk.X, pady=5)
        tk.Label(count_frame, text="物品数量:").pack(side=tk.LEFT, padx=5)
        self.count_entry = tk.Entry(count_frame, width=10)
        self.count_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(count_frame, text="确认", command=self.setup_items_input).pack(side=tk.LEFT, padx=5)
        
        # 物品输入区域（动态生成）
        self.items_frame = tk.Frame(input_frame)
        self.items_frame.pack(fill=tk.BOTH, pady=5)
        
        # 背包容量输入
        capacity_frame = tk.Frame(input_frame)
        capacity_frame.pack(fill=tk.X, pady=5)
        tk.Label(capacity_frame, text="背包容量:").pack(side=tk.LEFT, padx=5)
        self.capacity_entry = tk.Entry(capacity_frame, width=10)
        self.capacity_entry.pack(side=tk.LEFT, padx=5)
        
        # 算法按钮区域
        button_frame = ttk.LabelFrame(self.root, text="算法选择", padding=10)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons = [
            ("贪心算法（分数背包）", self.solve_fractional_greedy),
            ("贪心算法（0-1背包）", self.solve_01_greedy),
            ("蛮力法（0-1背包）", self.solve_01_bruteforce),
            ("动态规划（0-1背包）", self.solve_01_dp),
            ("记忆化DP（0-1背包）", self.solve_01_dp_memo),
            ("贪心算法反例", self.show_greedy_counterexample),
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command, width=20)
            btn.grid(row=i // 2, column=i % 2, padx=5, pady=5, sticky="ew")
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # 输出区域
        output_frame = ttk.LabelFrame(self.root, text="输出结果", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 清空按钮
        clear_button = tk.Button(output_frame, text="清空输出", command=self.clear_output, width=10)
        clear_button.pack(anchor=tk.E, pady=(0, 5))
        
        # 文本框和滚动条容器
        text_frame = tk.Frame(output_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(text_frame, height=15, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
```

### 3.2 关键功能方法

#### 输入处理

```python
    def setup_items_input(self):
        """根据物品数量创建输入框"""
        try:
            count = int(self.count_entry.get())
            if count <= 0:
                messagebox.showerror("错误", "物品数量必须大于0")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的物品数量")
            return
        
        # 清空之前的输入框
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # 创建表头
        header_frame = tk.Frame(self.items_frame)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="物品", width=8).pack(side=tk.LEFT, padx=2)
        tk.Label(header_frame, text="重量", width=10).pack(side=tk.LEFT, padx=2)
        tk.Label(header_frame, text="价值", width=10).pack(side=tk.LEFT, padx=2)
        
        # 创建输入框
        self.item_entries = []
        for i in range(count):
            item_frame = tk.Frame(self.items_frame)
            item_frame.pack(fill=tk.X, pady=2)
            tk.Label(item_frame, text=f"物品{i+1}:", width=8).pack(side=tk.LEFT, padx=2)
            weight_entry = tk.Entry(item_frame, width=10)
            weight_entry.pack(side=tk.LEFT, padx=2)
            value_entry = tk.Entry(item_frame, width=10)
            value_entry.pack(side=tk.LEFT, padx=2)
            self.item_entries.append((weight_entry, value_entry))
    
    def get_items(self):
        """从输入框获取物品数据"""
        items = []
        for weight_entry, value_entry in self.item_entries:
            try:
                weight = int(weight_entry.get())
                value = int(value_entry.get())
                if weight <= 0 or value < 0:
                    raise ValueError("重量必须大于0，价值必须非负")
                items.append((weight, value))
            except ValueError as e:
                messagebox.showerror("错误", f"请输入有效的物品数据: {e}")
                return None
        return items
```

#### 算法调用示例

```python
    def solve_fractional_greedy(self):
        """求解分数背包问题（贪心算法）"""
        items = self.get_items()
        capacity = self.get_capacity()
        if items is None or capacity is None:
            return
        
        self.clear_output()
        self.output("=" * 50)
        self.output("贪心算法 - 分数背包问题（最优解）")
        self.output("=" * 50)
        
        start_time = time.time()
        total_value, selected = fractional_knapsack_greedy(items, capacity)
        elapsed_time = time.time() - start_time
        
        self.output(f"\n最大总价值: {total_value:.2f}")
        self.output(f"\n选择的物品:")
        for idx, fraction in selected:
            weight, value = items[idx]
            self.output(f"  物品{idx+1}: 重量={weight}, 价值={value}, 选择比例={fraction:.2%}")
            self.output(f"    贡献价值: {value * fraction:.2f}")
        
        self.output(f"\n算法时间复杂度: O(n log n)")
        self.output(f"实际运行时间: {elapsed_time*1000:.4f} 毫秒")
```

---

## 四、算法复杂度对比总结

| 算法 | 问题类型 | 解的质量 | 时间复杂度 | 空间复杂度 | 适用场景 |
|------|---------|---------|-----------|-----------|---------|
| 贪心（分数背包） | 分数背包 | 最优解 | O(n log n) | O(n) | 物品可切分 |
| 贪心（0-1背包） | 0-1背包 | 近似解 | O(n log n) | O(n) | 快速近似 |
| 蛮力法 | 0-1背包 | 最优解 | O(2^n) | O(n) | n很小（<20） |
| 动态规划 | 0-1背包 | 最优解 | O(n×capacity) | O(n×capacity) | 一般情况 |
| 记忆化DP | 0-1背包 | 最优解 | O(n×capacity) | O(n×capacity) | capacity很大但状态稀疏 |

---

## 五、实验运行说明

### 5.1 环境要求
- Python 3.x
- Tkinter（通常随Python安装）

### 5.2 运行方法
```bash
python python
```

### 5.3 使用步骤
1. 启动程序，打开GUI界面
2. 输入物品数量，点击"确认"
3. 在生成的输入框中输入每个物品的重量和价值
4. 输入背包容量
5. 点击相应的算法按钮执行求解
6. 查看输出区域的详细结果

### 5.4 测试建议
- **小规模测试**：3-5个物品，验证算法正确性
- **中等规模**：10-20个物品，比较不同算法
- **大规模测试**：注意蛮力法会很慢（n>20时）

---

## 六、实验总结

### 6.1 核心收获
1. **问题分类的重要性**：分数背包和0-1背包的解法完全不同
2. **算法选择**：不同算法在不同场景下的适用性
3. **复杂度分析**：理解时间复杂度和空间复杂度的实际意义
4. **动态规划思想**：将大问题分解为子问题

### 6.2 关键发现
- 贪心算法在分数背包中能保证最优解
- 贪心算法在0-1背包中只能得到近似解
- 动态规划是求解0-1背包问题的标准方法
- 蛮力法虽然简单，但效率极低

### 6.3 扩展思考
- 如何优化动态规划的空间复杂度？（滚动数组）
- 如何处理超大capacity的情况？（状态压缩）
- 如何求解完全背包问题？（物品可以选多次）
