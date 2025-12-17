"""
斐波那契数列计算实验程序
包含5种核心算法：迭代法、迭代改进、递归法、公式法、矩阵法
"""

import time
import math
import sys
from tkinter import *
from tkinter import scrolledtext, messagebox

# ==================== 核心算法部分 ====================

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


# ==================== GUI部分 ====================

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
    
    def clearOutput(self):
        """清空输出文本框"""
        self.outputText.delete(1.0, END)
    
    def appendOutput(self, text):
        """追加输出文本"""
        self.outputText.insert(END, text + "\n")
        self.outputText.see(END)
        self.root.update()
    
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


def main():
    root = Tk()
    app = FibonacciGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

