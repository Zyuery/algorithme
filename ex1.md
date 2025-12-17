
# 斐波那契数列计算实验详细说明文档

## 一、实验概述

本实验旨在通过实现和比较多种斐波那契数列计算算法，深入理解不同算法设计方法在时间复杂度、空间复杂度和实际性能上的差异。实验包含5种核心算法实现和7个功能测试模块。

### 1.1 实验目标
- 掌握多种斐波那契数列计算算法
- 理解算法复杂度分析
- 比较不同算法的实际性能
- 分析算法在不同场景下的适用性
- 学习GUI界面设计与实现

### 1.2 技术栈
- **编程语言**: Python 3.x
- **GUI框架**: Tkinter
- **核心库**: time, math, sys

---

## 二、核心算法实现

### 2.1 迭代法（数组存储）

#### 算法描述
使用数组存储所有计算过的斐波那契数，通过迭代方式逐步计算。

#### 实现代码
```python
def fibonacciIterative(n):
    """
    迭代法：使用数组存储所有斐波那契数
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
fibArray = [0] * (n + 1)
fibArray[0] = 0
fibArray[1] = 1

for i in range(2, n + 1):
    fibArray[i] = fibArray[i - 1] + fibArray[i - 2]

return fibArray[n]
```


#### 算法特点
- **时间复杂度**: O(n) - 需要遍历n次
- **空间复杂度**: O(n) - 需要存储n+1个元素
- **优点**: 实现简单，可以保存所有中间结果
- **缺点**: 空间开销较大

#### 核心思想
1. 创建大小为n+1的数组
2. 初始化F(0)=0, F(1)=1
3. 通过循环计算F(i) = F(i-1) + F(i-2)

---

### 2.2 迭代改进法（空间优化）

#### 算法描述
只保存最近的两个斐波那契数，大幅减少空间使用。

#### 实现代码
```python
def fibonacciIterativeImproved(n):
    """
    迭代改进法：只保存最近的两个值，节省空间
    时间复杂度：O(n)
    空间复杂度：O(1)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    prev = 0
    curr = 1
    
    for i in range(2, n + 1):
        nextVal = prev + curr
        prev = curr
        curr = nextVal
    
    return curr
```

#### 算法特点
- **时间复杂度**: O(n) - 需要遍历n次
- **空间复杂度**: O(1) - 只使用常数个变量
- **优点**: 空间效率高，适合大数计算
- **缺点**: 无法保存中间结果

#### 核心思想
1. 只维护prev和curr两个变量
2. 每次迭代更新：nextVal = prev + curr
3. 更新prev和curr为下一轮做准备

---

### 2.3 递归法

#### 算法描述
直接使用递归定义计算斐波那契数。

#### 实现代码
```python
def fibonacciRecursive(n):
    """
    递归法：直接递归计算
    时间复杂度：O(2^n)
    空间复杂度：O(n)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2)
```

#### 算法特点
- **时间复杂度**: O(2^n) - 存在大量重复计算
- **空间复杂度**: O(n) - 递归调用栈深度
- **优点**: 代码简洁，符合数学定义
- **缺点**: 效率极低，不适合大数计算

#### 核心思想
1. 递归终止条件：n <= 0 返回0，n == 1 返回1
2. 递归关系：F(n) = F(n-1) + F(n-2)
3. 存在大量重复子问题（未优化）

#### 性能分析
- 计算F(5)需要调用函数15次
- 计算F(10)需要调用函数177次
- 计算F(20)需要调用函数21891次
- 计算F(30)需要调用函数2692537次

---

### 2.4 公式法（Binet公式）

#### 算法描述
使用Binet公式直接计算斐波那契数。

#### 数学原理
Binet公式：
```
F(n) = (φ^n - ψ^n) / √5
```
其中：
- φ = (1 + √5) / 2 ≈ 1.618（黄金比例）
- ψ = (1 - √5) / 2 ≈ -0.618

#### 实现代码
```python
def fibonacciFormula(n):
    """
    公式法：使用Binet公式 F(n) = (φ^n - ψ^n) / sqrt(5)
    其中 φ = (1 + sqrt(5)) / 2, ψ = (1 - sqrt(5)) / 2
    时间复杂度：O(1)
    空间复杂度：O(1)
    """
    if n <= 0:
        return 0
    
    sqrt5 = math.sqrt(5)
    phi = (1 + sqrt5) / 2
    psi = (1 - sqrt5) / 2
    
    result = (phi ** n - psi ** n) / sqrt5
    return int(round(result))
```

#### 算法特点
- **时间复杂度**: O(1) - 常数时间计算
- **空间复杂度**: O(1) - 只使用常数个变量
- **优点**: 计算速度快
- **缺点**: 浮点数精度问题，大n值可能产生误差

#### 核心思想
1. 计算黄金比例φ和ψ
2. 计算φ^n和ψ^n
3. 应用Binet公式并四舍五入

#### 精度问题
- 由于浮点数精度限制，当n较大时可能出现误差
- 需要与迭代法结果对比验证

---

### 2.5 矩阵法（矩阵快速幂）

#### 算法描述
利用矩阵乘法和快速幂算法计算斐波那契数。

#### 数学原理
斐波那契数列的矩阵表示：
```python
[F(n+1)]   [1  1]^n  [F(1)]
[F(n)  ] = [1  0]    [F(0)]
```

#### 实现代码
```python
def fibonacciMatrix(n):
    """
    矩阵法：使用矩阵快速幂
    时间复杂度：O(log n)
    空间复杂度：O(1)
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    def matrixMultiply(A, B):
        """矩阵乘法"""
        return [
            [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
            [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]]
        ]
    
    def matrixPower(matrix, power):
        """矩阵快速幂"""
        if power == 1:
            return matrix
        
        if power % 2 == 0:
            half = matrixPower(matrix, power // 2)
            return matrixMultiply(half, half)
        else:
            return matrixMultiply(matrix, matrixPower(matrix, power - 1))
    
    baseMatrix = [[1, 1], [1, 0]]
    resultMatrix = matrixPower(baseMatrix, n)
    return resultMatrix[0][1]
```

#### 算法特点
- **时间复杂度**: O(log n) - 快速幂算法
- **空间复杂度**: O(1) - 递归栈深度为O(log n)，但通常视为O(1)
- **优点**: 时间复杂度最优，适合超大数计算
- **缺点**: 实现相对复杂

#### 核心思想
1. 定义2×2矩阵乘法函数
2. 实现矩阵快速幂算法（分治思想）
3. 计算基础矩阵的n次幂
4. 提取结果矩阵中的F(n)

#### 快速幂原理
- 如果n是偶数：A^n = (A^(n/2))^2
- 如果n是奇数：A^n = A × A^(n-1)
- 将O(n)次乘法优化为O(log n)次

---

## 三、功能测试模块

### 3.1 功能2：五种方法比较

#### 功能要求
对相同的输入n，使用5种方法计算斐波那契数，并比较：
- 计算结果
- 执行时间
- 估算的基本操作次数
- 结果一致性验证

#### 实现代码
```python
    def compareFiveMethods(self):
        """功能2: 对相同输入n，用5种方法计算并比较"""
        try:
            n = int(self.nEntry.get())
            if n < 0:
                messagebox.showerror("错误", "n值必须为非负整数")
                return
            
            self.appendOutput(f"\n{'='*60}")
            self.appendOutput(f"功能2: 计算第{n}个斐波那契数（五种方法比较）")
            self.appendOutput(f"{'='*60}\n")
            
            methods = [
                ("迭代法（数组）", fibonacciIterative),
                ("迭代改进法", fibonacciIterativeImproved),
                ("递归法", fibonacciRecursive),
                ("公式法", fibonacciFormula),
                ("矩阵法", fibonacciMatrix)
            ]
            
            results = []
            
            for methodName, methodFunc in methods:
                startTime = time.time()
                try:
                    if methodName == "递归法" and n > 35:
                        self.appendOutput(f"{methodName}: 跳过（n={n}太大，递归会非常慢）")
                        continue
                    
                    result = methodFunc(n)
                    endTime = time.time()
                    elapsedTime = (endTime - startTime) * 1000  # 转换为毫秒
                    
                    # 估算基本操作次数
                    if methodName == "迭代法（数组）":
                        operations = n
                    elif methodName == "迭代改进法":
                        operations = n
                    elif methodName == "递归法":
                        operations = 2 ** n  # 近似
                    elif methodName == "公式法":
                        operations = 1
                    else:  # 矩阵法
                        operations = int(math.log2(n)) if n > 0 else 0
                    
                    results.append({
                        'name': methodName,
                        'result': result,
                        'time': elapsedTime,
                        'operations': operations
                    })
                    
                    self.appendOutput(f"{methodName}:")
                    self.appendOutput(f"  结果: {result}")
                    self.appendOutput(f"  执行时间: {elapsedTime:.6f} 毫秒")
                    self.appendOutput(f"  估算基本操作次数: {operations}")
                    self.appendOutput("")
                    
                except Exception as e:
                    self.appendOutput(f"{methodName}: 计算失败 - {str(e)}\n")
            
            # 验证结果一致性
            if len(results) > 1:
                firstResult = results[0]['result']
                allSame = all(r['result'] == firstResult for r in results)
                if allSame:
                    self.appendOutput(f"✓ 所有方法结果一致: {firstResult}")
                else:
                    self.appendOutput("⚠ 警告: 不同方法的结果不一致！")
                    for r in results:
                        self.appendOutput(f"  {r['name']}: {r['result']}")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数")
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")
```

#### 测试要点
1. **输入验证**: 检查n是否为非负整数
2. **性能保护**: 递归法在n>35时自动跳过
3. **时间测量**: 使用time.time()精确测量执行时间
4. **操作次数估算**: 根据算法特性估算基本操作次数
5. **结果验证**: 自动检查所有方法结果是否一致

#### 预期输出
- 每种方法的计算结果
- 执行时间（毫秒）
- 估算的基本操作次数
- 结果一致性报告

---

### 3.2 功能3：迭代找最大序号

#### 功能要求
使用迭代算法找出不超过系统最大整数的最大斐波那契数序号。

#### 实现代码
```python
    def findMaxWithIterative(self):
        """功能3: 用迭代算法找不超过最大整数的斐波那契数序号"""
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能3: 迭代算法寻找最大斐波那契数序号")
        self.appendOutput(f"{'='*60}\n")
        
        # 确定最大整数
        maxInt = sys.maxsize
        self.appendOutput(f"系统支持的最大整数: {maxInt}")
        self.appendOutput(f"整数位数: {maxInt.bit_length()} 位\n")
        
        startTime = time.time()
        n = 0
        prev = 0
        curr = 1
        
        while curr <= maxInt:
            n += 1
            if n == 1:
                continue
            
            nextVal = prev + curr
            if nextVal > maxInt:
                break
            
            prev = curr
            curr = nextVal
        
        endTime = time.time()
        elapsedTime = (endTime - startTime) * 1000
        
        self.appendOutput(f"最大斐波那契数序号: {n}")
        self.appendOutput(f"第{n}个斐波那契数: {curr}")
        self.appendOutput(f"执行时间: {elapsedTime:.6f} 毫秒")
        self.appendOutput(f"第{n+1}个斐波那契数会溢出（值为: {prev + curr}）\n")
        
        # 保存结果供功能5使用
        self.maxN = n
```

#### 测试要点
1. **系统限制**: 获取sys.maxsize确定最大整数
2. **迭代计算**: 使用迭代改进法逐步计算
3. **溢出检测**: 当nextVal > maxInt时停止
4. **结果保存**: 保存最大序号供功能5使用

#### 预期结果
- 系统最大整数值
- 最大斐波那契数序号（通常约为90-95）
- 对应的斐波那契数值
- 执行时间

---

### 3.3 功能4：递归找最大序号

#### 功能要求
使用递归算法找出不超过系统最大整数的最大斐波那契数序号。

#### 实现代码
```python
    def findMaxWithRecursive(self):
        """功能4: 用递归算法找不超过最大整数的斐波那契数序号"""
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能4: 递归算法寻找最大斐波那契数序号")
        self.appendOutput(f"{'='*60}\n")
        self.appendOutput("注意: 递归算法效率很低，将使用迭代法先找到范围，再用递归验证\n")
        
        maxInt = sys.maxsize
        self.appendOutput(f"系统支持的最大整数: {maxInt}\n")
        
        # 先用迭代法找到大概范围
        startTime = time.time()
        n = 0
        prev = 0
        curr = 1
        
        while curr <= maxInt:
            n += 1
            if n == 1:
                continue
            nextVal = prev + curr
            if nextVal > maxInt:
                break
            prev = curr
            curr = nextVal
        
        # 用递归验证边界
        self.appendOutput(f"使用迭代法找到的最大序号: {n}")
        self.appendOutput(f"开始用递归法验证...\n")
        
        # 递归验证（只验证几个关键值，因为递归太慢）
        testValues = [n - 2, n - 1, n] if n > 2 else [n]
        for testN in testValues:
            recStart = time.time()
            try:
                recResult = fibonacciRecursive(testN)
                recEnd = time.time()
                recTime = (recEnd - recStart) * 1000
                self.appendOutput(f"递归计算 F({testN}) = {recResult}, 耗时: {recTime:.2f} 毫秒")
                if recResult > maxInt:
                    self.appendOutput(f"F({testN}) 超过最大整数")
                    break
            except Exception as e:
                self.appendOutput(f"递归计算 F({testN}) 失败: {str(e)}")
                break
        
        endTime = time.time()
        elapsedTime = (endTime - startTime) * 1000
        
        self.appendOutput(f"\n总执行时间: {elapsedTime:.6f} 毫秒")
        self.appendOutput(f"最大斐波那契数序号: {n} (主要由迭代法确定)\n")
```

#### 测试要点
1. **性能优化**: 先用迭代法找到范围，再用递归验证
2. **选择性验证**: 只验证关键边界值（n-2, n-1, n）
3. **异常处理**: 捕获递归计算可能的异常

#### 设计考虑
- 纯递归方法在n较大时几乎不可行
- 采用混合策略：迭代定位 + 递归验证
- 体现了算法选择的重要性

---

### 3.4 功能5：递归计算最大序号

#### 功能要求
使用递归方式计算功能3找到的最大序号n对应的斐波那契数，测试是否能在1分钟内完成。

#### 实现代码
```python
    def recursiveComputeMax(self):
        """功能5: 用递归方式计算第n个斐波那契数（n来自功能3），看是否能在1分钟内完成"""
        if not hasattr(self, 'maxN'):
            messagebox.showwarning("警告", "请先执行功能3获取最大序号n")
            return
        
        n = self.maxN
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput(f"功能5: 递归计算第{n}个斐波那契数（1分钟限制）")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput(f"开始递归计算 F({n})...")
        self.appendOutput("警告: 递归算法效率极低，可能需要很长时间\n")
        
        startTime = time.time()
        timeout = 60  # 60秒超时
        
        try:
            # 使用一个简单的递归包装器来检测超时
            result = None
            exceptionOccurred = False
            
            def recursiveWithTimeout(n, startTime, timeout):
                if time.time() - startTime > timeout:
                    return None, True
                if n <= 0:
                    return 0, False
                if n == 1:
                    return 1, False
                
                result1, timeout1 = recursiveWithTimeout(n - 1, startTime, timeout)
                if timeout1:
                    return None, True
                
                result2, timeout2 = recursiveWithTimeout(n - 2, startTime, timeout)
                if timeout2:
                    return None, True
                
                return result1 + result2, False
            
            result, timedOut = recursiveWithTimeout(n, startTime, timeout)
            
            endTime = time.time()
            elapsedTime = endTime - startTime
            
            if timedOut:
                self.appendOutput(f"✗ 超时！在60秒内无法完成计算")
                self.appendOutput(f"已用时间: {elapsedTime:.2f} 秒")
            else:
                self.appendOutput(f"✓ 计算完成！")
                self.appendOutput(f"结果: F({n}) = {result}")
                self.appendOutput(f"执行时间: {elapsedTime:.6f} 秒")
                if elapsedTime < 60:
                    self.appendOutput(f"在1分钟内完成（剩余时间: {60 - elapsedTime:.2f} 秒）")
                else:
                    self.appendOutput(f"超过1分钟限制")
        
        except Exception as e:
            endTime = time.time()
            elapsedTime = endTime - startTime
            self.appendOutput(f"计算失败: {str(e)}")
            self.appendOutput(f"已用时间: {elapsedTime:.2f} 秒\n")
```

#### 测试要点
1. **依赖检查**: 确保先执行功能3
2. **超时机制**: 实现60秒超时检测
3. **递归包装**: 在递归过程中检查超时
4. **结果报告**: 详细报告计算状态和时间

#### 预期结果
- 对于n≈90的情况，递归法几乎不可能在60秒内完成
- 演示递归算法的性能瓶颈

---

### 3.5 功能6：30秒内最大序号

#### 功能要求
分别测试递归算法和迭代算法在30秒内能计算的最大斐波那契数序号。

#### 实现代码
```python
    def findMaxIn30Seconds(self):
        """功能6: 找30秒内能计算的最大斐波那契数序号（递归和迭代）"""
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能6: 30秒内能计算的最大斐波那契数序号")
        self.appendOutput(f"{'='*60}\n")
        
        timeout = 30  # 30秒
        
        # 递归算法
        self.appendOutput("【递归算法】")
        self.appendOutput("开始测试...\n")
        
        recMaxN = 0
        recStartTime = time.time()
        
        for n in range(1, 50):  # 递归很慢，从小的开始
            if time.time() - recStartTime > timeout:
                break
            
            testStart = time.time()
            try:
                result = fibonacciRecursive(n)
                testEnd = time.time()
                testTime = testEnd - testStart
                
                if testTime < timeout - (time.time() - recStartTime):
                    recMaxN = n
                    self.appendOutput(f"F({n}) = {result}, 耗时: {testTime:.3f} 秒")
                else:
                    break
            except:
                break
        
        recTotalTime = time.time() - recStartTime
        self.appendOutput(f"\n递归算法最大序号: {recMaxN}")
        self.appendOutput(f"总耗时: {recTotalTime:.2f} 秒")
        
        # 计算下一个的时间
        if recMaxN > 0:
            nextN = recMaxN + 1
            self.appendOutput(f"\n计算下一个 F({nextN})...")
            nextStart = time.time()
            try:
                nextResult = fibonacciRecursive(nextN)
                nextEnd = time.time()
                nextTime = nextEnd - nextStart
                self.appendOutput(f"F({nextN}) = {nextResult}, 耗时: {nextTime:.3f} 秒")
            except Exception as e:
                self.appendOutput(f"计算失败: {str(e)}")
        
        # 迭代算法
        self.appendOutput(f"\n【迭代算法】")
        self.appendOutput("开始测试...\n")
        
        iterMaxN = 0
        iterStartTime = time.time()
        
        n = 1
        prev = 0
        curr = 1
        
        while time.time() - iterStartTime < timeout:
            if n == 1:
                iterMaxN = n
                n += 1
                continue
            
            nextVal = prev + curr
            if nextVal > sys.maxsize:
                break
            
            testStart = time.time()
            # 迭代计算很快，直接计算到n
            for i in range(iterMaxN + 1, n + 1):
                if i == 1:
                    continue
                temp = prev + curr
                prev = curr
                curr = temp
            
            testEnd = time.time()
            testTime = testEnd - testStart
            
            iterMaxN = n
            if n % 1000 == 0 or n < 100:  # 只输出部分结果
                self.appendOutput(f"F({n}) = {curr}, 耗时: {testTime:.6f} 秒")
            
            n += 1
            if n > 1000000:  # 防止无限循环
                break
        
        iterTotalTime = time.time() - iterStartTime
        self.appendOutput(f"\n迭代算法最大序号: {iterMaxN}")
        self.appendOutput(f"总耗时: {iterTotalTime:.2f} 秒")
        
        # 计算下一个的时间
        if iterMaxN > 0:
            nextN = iterMaxN + 1
            self.appendOutput(f"\n计算下一个 F({nextN})...")
            nextStart = time.time()
            nextResult = fibonacciIterativeImproved(nextN)
            nextEnd = time.time()
            nextTime = nextEnd - nextStart
            self.appendOutput(f"F({nextN}) = {nextResult}, 耗时: {nextTime:.6f} 秒")
        
        self.appendOutput("")
```

#### 测试要点
1. **时间限制**: 严格控制在30秒内
2. **算法对比**: 同时测试递归和迭代两种算法
3. **性能差异**: 清晰展示两种算法的性能差距
4. **输出优化**: 迭代算法只输出部分结果（避免输出过多）

#### 预期结果
- **递归算法**: 30秒内可能只能计算到n≈35-40
- **迭代算法**: 30秒内可以计算到n≈数百万甚至更多
- 清晰展示O(2^n)和O(n)的差异

---

### 3.6 功能7：公式法找误差

#### 功能要求
找出公式法计算结果与迭代法不一致的最小n值，分析浮点数精度问题。

#### 实现代码
```python
    def findFormulaError(self):
        """功能7: 用公式法找出出现误差时的最小n值"""
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能7: 公式法找出误差时的最小n值")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput("比较公式法和迭代法的结果，找出第一个不一致的n值...\n")
        
        maxN = 100  # 先测试到100
        errorN = None
        
        for n in range(1, maxN + 1):
            formulaResult = fibonacciFormula(n)
            iterativeResult = fibonacciIterativeImproved(n)
            
            if formulaResult != iterativeResult:
                errorN = n
                self.appendOutput(f"✗ 发现误差！")
                self.appendOutput(f"n = {n}")
                self.appendOutput(f"公式法结果: {formulaResult}")
                self.appendOutput(f"迭代法结果: {iterativeResult}")
                self.appendOutput(f"误差: {abs(formulaResult - iterativeResult)}")
                break
            
            if n % 10 == 0:
                self.appendOutput(f"已测试到 n={n}, 结果一致")
        
        if errorN is None:
            self.appendOutput(f"在 n=1 到 n={maxN} 范围内未发现误差")
            self.appendOutput("继续扩大测试范围...\n")
            
            # 扩大测试范围
            for n in range(maxN + 1, maxN + 100):
                formulaResult = fibonacciFormula(n)
                iterativeResult = fibonacciIterativeImproved(n)
                
                if formulaResult != iterativeResult:
                    errorN = n
                    self.appendOutput(f"✗ 发现误差！")
                    self.appendOutput(f"n = {n}")
                    self.appendOutput(f"公式法结果: {formulaResult}")
                    self.appendOutput(f"迭代法结果: {iterativeResult}")
                    self.appendOutput(f"误差: {abs(formulaResult - iterativeResult)}")
                    break
        
        if errorN:
            self.appendOutput(f"\n最小误差n值: {errorN}")
        else:
            self.appendOutput(f"\n在测试范围内未发现误差（可能是浮点精度问题在更大n值才出现）")
        
        self.appendOutput("")
```

#### 测试要点
1. **结果对比**: 逐项比较公式法和迭代法的结果
2. **误差检测**: 找出第一个不一致的n值
3. **范围扩展**: 如果初始范围未发现误差，自动扩大测试范围
4. **误差分析**: 计算并显示误差值

#### 预期结果
- 通常在n=70-80左右开始出现误差
- 误差随着n增大而增大
- 演示浮点数精度限制

#### 误差原因分析
1. **浮点数精度**: Python的float类型精度有限
2. **舍入误差**: 多次浮点运算累积误差
3. **大数计算**: φ^n在n较大时精度损失明显

---

## 四、GUI界面设计

### 4.1 界面布局

#### 实现代码
```python
class FibonacciGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("斐波那契数列计算实验")
        self.root.geometry("800x700")
        
        # 输入框
        inputFrame = Frame(root)
        inputFrame.pack(pady=10)
        
        Label(inputFrame, text="输入n值:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        self.nEntry = Entry(inputFrame, width=20, font=("Arial", 12))
        self.nEntry.pack(side=LEFT, padx=5)
        
        # 按钮框架
        buttonFrame = Frame(root)
        buttonFrame.pack(pady=10)
        
        # 功能按钮
        Button(buttonFrame, text="功能2: 五种方法比较", command=self.compareFiveMethods, 
               width=20, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(buttonFrame, text="功能3: 迭代找最大序号", command=self.findMaxWithIterative, 
               width=20, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        
        buttonFrame2 = Frame(root)
        buttonFrame2.pack(pady=10)
        
        Button(buttonFrame2, text="功能4: 递归找最大序号", command=self.findMaxWithRecursive, 
               width=20, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(buttonFrame2, text="功能5: 递归计算最大序号", command=self.recursiveComputeMax, 
               width=20, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        
        buttonFrame3 = Frame(root)
        buttonFrame3.pack(pady=10)
        
        Button(buttonFrame3, text="功能6: 30秒内最大序号", command=self.findMaxIn30Seconds, 
               width=20, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(buttonFrame3, text="功能7: 公式法找误差", command=self.findFormulaError, 
               width=20, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        
        # 输出文本框
        outputFrame = Frame(root)
        outputFrame.pack(pady=10, padx=10, fill=BOTH, expand=True)
        
        Label(outputFrame, text="输出结果:", font=("Arial", 12)).pack(anchor=W)
        self.outputText = scrolledtext.ScrolledText(outputFrame, width=80, height=25, 
                                                     font=("Consolas", 10))
        self.outputText.pack(fill=BOTH, expand=True)
        
        # 清空按钮
        Button(root, text="清空输出", command=self.clearOutput, 
               width=15, font=("Arial", 10)).pack(pady=5)
```

### 4.2 界面组件

1. **输入区域**
   - n值输入框：用于功能2的输入

2. **功能按钮区域**
   - 6个功能按钮，分为3行排列
   - 每个按钮对应一个测试功能

3. **输出区域**
   - 滚动文本框：显示所有测试结果
   - 使用等宽字体（Consolas）便于阅读

4. **辅助功能**
   - 清空输出按钮：清除所有输出内容

### 4.3 辅助方法

```177:185:fibonacci_gui.py
    def clearOutput(self):
        """清空输出文本框"""
        self.outputText.delete(1.0, END)
    
    def appendOutput(self, text):
        """追加输出文本"""
        self.outputText.insert(END, text + "\n")
        self.outputText.see(END)
        self.root.update()
```

---

## 五、算法复杂度对比总结

| 算法 | 时间复杂度 | 空间复杂度 | 适用场景 | 优缺点 |
|------|-----------|-----------|---------|--------|
| 迭代法（数组） | O(n) | O(n) | 需要保存所有中间结果 | 简单但空间开销大 |
| 迭代改进法 | O(n) | O(1) | 一般计算场景 | 空间效率高，推荐使用 |
| 递归法 | O(2^n) | O(n) | 教学演示 | 代码简洁但效率极低 |
| 公式法 | O(1) | O(1) | 小到中等n值 | 速度快但有精度问题 |
| 矩阵法 | O(log n) | O(1) | 超大数计算 | 时间复杂度最优 |

---

## 六、实验运行说明

### 6.1 环境要求
- Python 3.x
- Tkinter（通常随Python安装）

### 6.2 运行方法
```bash
python fibonacci_gui.py
```

### 6.3 使用步骤
1. 启动程序，打开GUI界面
2. 对于功能2，在输入框输入n值
3. 点击相应功能按钮执行测试
4. 查看输出区域的详细结果
5. 使用"清空输出"按钮清除结果

### 6.4 注意事项
- 功能5依赖功能3的结果，需先执行功能3
- 递归算法在n较大时可能非常慢或超时
- 公式法在大n值时可能出现精度误差

---

## 七、实验总结

### 7.1 核心收获
1. **算法选择的重要性**: 不同算法在不同场景下性能差异巨大
2. **复杂度分析**: 理论复杂度与实际性能的关系
3. **优化策略**: 空间优化、时间优化的不同方法
4. **精度问题**: 浮点数计算中的精度限制

### 7.2 关键发现
- 递归法虽然代码简洁，但效率极低，不适合实际应用
- 迭代改进法在大多数场景下是最佳选择
- 矩阵法在超大数计算时具有明显优势
- 公式法虽然时间复杂度为O(1)，但受精度限制

### 7.3 扩展思考
- 如何进一步优化递归算法？（记忆化、动态规划）
- 如何处理超大数计算？（使用大数库）
- 如何提高公式法的精度？（使用高精度浮点数库）

---

## 八、代码文件结构

```
fibonacci_gui.py
├── 核心算法部分（14-119行）
│   ├── fibonacciIterative() - 迭代法
│   ├── fibonacciIterativeImproved() - 迭代改进法
│   ├── fibonacciRecursive() - 递归法
│   ├── fibonacciFormula() - 公式法
│   └── fibonacciMatrix() - 矩阵法
│
├── GUI类定义（124-575行）
│   ├── __init__() - 界面初始化
│   ├── clearOutput() - 清空输出
│   ├── appendOutput() - 追加输出
│   ├── compareFiveMethods() - 功能2
│   ├── findMaxWithIterative() - 功能3
│   ├── findMaxWithRecursive() - 功能4
│   ├── recursiveComputeMax() - 功能5
│   ├── findMaxIn30Seconds() - 功能6
│   └── findFormulaError() - 功能7
│
└── 主程序（578-585行）
    └── main() - 程序入口
```

---

**文档版本**: 1.0  
**最后更新**: 2024  
**作者**: 实验程序开发者
```

该文档包含：
1. 实验概述与目标
2. 5种算法的实现与复杂度分析
3. 7个功能模块的说明与代码
4. GUI界面设计说明
5. 算法对比总结
6. 运行说明与注意事项
7. 实验总结与扩展思考

可直接保存为 Markdown 文件使用。
```