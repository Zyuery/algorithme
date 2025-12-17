import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import math
import threading

class OptimizedFibonacciExperiment:
    def __init__(self, root):
        self.root = root
        self.root.title("斐波那契计算实验")
        self.root.geometry("800x600")
        
        # 常量定义
        self.PHI = (1 + math.sqrt(5)) / 2
        self.SQRT5 = math.sqrt(5)
        self.max_iterative_n = None
        self.stop_flag = False  # 用于中断长时间运行的任务
        
        self.create_ui()
    
    def create_ui(self):
        # 输入区域
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="n值:").grid(row=0, column=0, padx=5)
        self.n_entry = ttk.Entry(input_frame, width=10)
        self.n_entry.grid(row=0, column=1, padx=5)
        self.n_entry.insert(0, "10")
        
        # 方法选择
        method_frame = ttk.Frame(self.root, padding=10)
        method_frame.pack(fill=tk.X)
        
        self.methods = {
            "iterative_basic": tk.BooleanVar(value=True),
            "iterative_optimized": tk.BooleanVar(value=True),
            "recursive": tk.BooleanVar(value=True),
            "formula": tk.BooleanVar(value=True),
            "matrix": tk.BooleanVar(value=True)
        }
        
        ttk.Checkbutton(method_frame, text="普通迭代", variable=self.methods["iterative_basic"]).grid(row=0, column=0, padx=10)
        ttk.Checkbutton(method_frame, text="迭代改进", variable=self.methods["iterative_optimized"]).grid(row=0, column=1, padx=10)
        ttk.Checkbutton(method_frame, text="递归法", variable=self.methods["recursive"]).grid(row=0, column=2, padx=10)
        ttk.Checkbutton(method_frame, text="公式法", variable=self.methods["formula"]).grid(row=0, column=3, padx=10)
        ttk.Checkbutton(method_frame, text="矩阵法", variable=self.methods["matrix"]).grid(row=0, column=4, padx=10)
        
        # 按钮区域
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="计算", command=self.calculate).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="找最大(迭代)", command=self.find_max_iterative).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="找最大(递归)", command=self.find_max_recursive).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="测试公式误差", command=self.test_formula_error).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="中断任务", command=self.stop_current_task).grid(row=0, column=4, padx=5)
        
        # 结果区域
        ttk.Label(self.root, text="结果:").pack(anchor=tk.W, padx=10)
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.result_text.config(state=tk.DISABLED)
        
        # 状态栏
        self.status = tk.StringVar(value="就绪")
        ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W).pack(side=tk.BOTTOM, fill=tk.X)
    
    def log(self, text):
        "向结果区域添加文本"
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def set_status(self, text):
        "更新状态栏"
        self.status.set(text)
    
    def stop_current_task(self):
        "中断当前运行的任务"
        self.stop_flag = True
        self.set_status("任务已中断")
    
    # 1. 普通迭代法（使用数组存储所有值）
    def fib_iterative_basic(self, n):
        """
        普通迭代法：使用数组存储所有中间值
        时间复杂度：O(n)
        空间复杂度：O(n)
        基本操作：数组赋值和加法运算
        """
        if n <= 1:
            return (n, 0)
        
        fib = [0] * (n + 1)
        fib[0] = 0
        fib[1] = 1
        ops = 2  # 初始赋值操作
        
        for i in range(2, n + 1):
            fib[i] = fib[i-1] + fib[i-2]
            ops += 1  # 每次循环：1次加法，1次赋值（计为1个基本操作）
        
        return (fib[n], ops)
    
    # 2. 迭代改进法（只使用两个变量）
    def fib_iterative_optimized(self, n):
        """
        迭代改进法：只使用两个变量，空间优化
        时间复杂度：O(n)
        空间复杂度：O(1)
        基本操作：变量赋值和加法运算
        """
        if n <= 1:
            return (n, 0)
        a, b = 0, 1
        ops = 2  # 初始赋值操作
        for i in range(2, n+1):
            a, b = b, a + b
            ops += 1  # 每次循环：1次加法，2次赋值（计为1个基本操作）
        return (b, ops)
    
    # 3. 递归法 - 带记忆化优化
    def __init_recursive_cache(self):
        self.recursive_cache = {0: 0, 1: 1}
        self.rec_ops = 0
    
    def fib_recursive(self, n):
        """
        递归法（带记忆化）：避免重复计算
        时间复杂度：O(n)
        空间复杂度：O(n)
        基本操作：递归调用和加法运算
        """
        self.rec_ops += 1  # 每次函数调用计为1个操作
        if n not in self.recursive_cache:
            self.recursive_cache[n] = self.fib_recursive(n-1) + self.fib_recursive(n-2)
            self.rec_ops += 1  # 加法操作
        return self.recursive_cache[n]
    
    def recursive_wrapper(self, n):
        self.__init_recursive_cache()
        result = self.fib_recursive(n)
        return (result, self.rec_ops)
    
    # 4. 公式法（Binet公式）
    def fib_formula(self, n):
        """
        公式法：使用Binet公式直接计算
        时间复杂度：O(1)（假设幂运算为O(1)）
        空间复杂度：O(1)
        基本操作：幂运算、减法、除法、取整
        """
        # 计算操作：2次幂运算，1次减法，1次除法，1次取整
        result = (math.pow(self.PHI, n) - math.pow(1-self.PHI, n)) / self.SQRT5
        return (round(result), 5)  # 5个基本操作
    
    # 5. 矩阵法（快速幂）
    def fib_matrix(self, n):
        """
        矩阵法：使用矩阵快速幂计算
        时间复杂度：O(log n)
        空间复杂度：O(1)
        基本操作：矩阵乘法的加法和乘法运算
        """
        if n <= 1:
            return (n, 0)
        
        def multiply(a, b):
            """
            2x2矩阵乘法
            每次乘法包含8次基本运算（4次乘法，4次加法）
            """
            return [
                [a[0][0]*b[0][0] + a[0][1]*b[1][0], a[0][0]*b[0][1] + a[0][1]*b[1][1]],
                [a[1][0]*b[0][0] + a[1][1]*b[1][0], a[1][0]*b[0][1] + a[1][1]*b[1][1]]
            ]
        
        def matrix_pow(mat, power):
            result = [[1,0], [0,1]]  # 单位矩阵
            ops = 0
            while power > 0:
                if power % 2 == 1:
                    result = multiply(result, mat)
                    ops += 8  # 矩阵乘法：8次基本操作
                mat = multiply(mat, mat)
                ops += 8  # 矩阵乘法：8次基本操作
                power //= 2
            return (result, ops)
        
        mat, ops = matrix_pow([[1,1], [1,0]], n-1)
        return (mat[0][0], ops)
    
    # 计算主函数
    def calculate(self):
        try:
            n = int(self.n_entry.get())
            if n < 0:
                messagebox.showerror("错误", "n必须是非负数")
                return
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.config(state=tk.DISABLED)
            
            self.log(f"计算第 {n} 个斐波那契数:")
            self.log(f"{'方法':<12} {'结果':<25} {'操作数':<12} {'时间(ms)':<12} {'增长率':<10}")
            self.log("-" * 80)
            
            results = []
            
            # 1. 普通迭代法
            if self.methods["iterative_basic"].get():
                start = time.time()
                res, ops = self.fib_iterative_basic(n)
                t = (time.time() - start) * 1000
                results.append(("普通迭代", res, ops, t, "O(n)"))
                self.log(f"{'普通迭代':<12} {str(res):<25} {ops:<12} {t:<12.4f} {'O(n)':<10}")
            
            # 2. 迭代改进法
            if self.methods["iterative_optimized"].get():
                start = time.time()
                res, ops = self.fib_iterative_optimized(n)
                t = (time.time() - start) * 1000
                results.append(("迭代改进", res, ops, t, "O(n)"))
                self.log(f"{'迭代改进':<12} {str(res):<25} {ops:<12} {t:<12.4f} {'O(n)':<10}")
            
            # 3. 递归法（带记忆化）
            if self.methods["recursive"].get():
                if n > 1000 and not messagebox.askyesno("警告", "n值较大，可能需要较长时间，继续?"):
                    pass
                else:
                    start = time.time()
                    res, ops = self.recursive_wrapper(n)
                    t = (time.time() - start) * 1000
                    results.append(("递归法", res, ops, t, "O(n)"))
                    self.log(f"{'递归法':<12} {str(res):<25} {ops:<12} {t:<12.4f} {'O(n)':<10}")
            
            # 4. 公式法
            if self.methods["formula"].get():
                start = time.time()
                res, ops = self.fib_formula(n)
                t = (time.time() - start) * 1000
                results.append(("公式法", res, ops, t, "O(1)"))
                self.log(f"{'公式法':<12} {str(res):<25} {ops:<12} {t:<12.4f} {'O(1)':<10}")
            
            # 5. 矩阵法
            if self.methods["matrix"].get():
                start = time.time()
                res, ops = self.fib_matrix(n)
                t = (time.time() - start) * 1000
                results.append(("矩阵法", res, ops, t, "O(log n)"))
                self.log(f"{'矩阵法':<12} {str(res):<25} {ops:<12} {t:<12.4f} {'O(log n)':<10}")
            
            # 比较分析
            if len(results) > 1:
                self.log("")
                self.log("=" * 80)
                self.log("性能比较分析:")
                self.log("=" * 80)
                
                # 验证结果一致性
                if all(r[1] == results[0][1] for r in results):
                    self.log(f"✓ 所有方法结果一致: {results[0][1]}")
                else:
                    self.log("⚠ 警告：不同方法的结果不一致！")
                    for name, res, _, _, _ in results:
                        self.log(f"  {name}: {res}")
                
                # 操作数比较
                self.log("")
                self.log("基本操作次数比较:")
                sorted_by_ops = sorted(results, key=lambda x: x[2])
                for i, (name, _, ops, _, complexity) in enumerate(sorted_by_ops):
                    if i == 0:
                        self.log(f"  {name}: {ops} 次 (最少)")
                    else:
                        ratio = ops / sorted_by_ops[0][2] if sorted_by_ops[0][2] > 0 else float('inf')
                        self.log(f"  {name}: {ops} 次 ({ratio:.2f}x)")
                
                # 执行时间比较
                self.log("")
                self.log("执行时间比较:")
                sorted_by_time = sorted(results, key=lambda x: x[3])
                for i, (name, _, _, t, _) in enumerate(sorted_by_time):
                    if i == 0:
                        self.log(f"  {name}: {t:.4f} ms (最快)")
                    else:
                        ratio = t / sorted_by_time[0][3] if sorted_by_time[0][3] > 0 else float('inf')
                        self.log(f"  {name}: {t:.4f} ms ({ratio:.2f}x)")
                
                # 复杂度分析
                self.log("")
                self.log("时间复杂度分析:")
                self.log("  - 普通迭代: O(n) - 线性增长")
                self.log("  - 迭代改进: O(n) - 线性增长（空间优化）")
                self.log("  - 递归法: O(n) - 线性增长（带记忆化）")
                self.log("  - 公式法: O(1) - 常数时间（但受浮点精度限制）")
                self.log("  - 矩阵法: O(log n) - 对数增长（最快）")
            
            self.set_status("计算完成")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数")
    
    # 找最大斐波那契数(迭代法) - 优化：使用快速倍增法加速
    def find_max_iterative(self):
        self.stop_flag = False
        self.set_status("正在查找最大斐波那契数...")
        threading.Thread(target=self._find_max_iterative, daemon=True).start()
    
    def _find_max_iterative(self):
        # 使用快速倍增法加速大n值计算
        def fast_doubling(n):
            if n == 0:
                return (0, 1)
            a, b = fast_doubling(n >> 1)
            c = a * (2*b - a)
            d = a*a + b*b
            if n & 1:
                return (d, c + d)
            else:
                return (c, d)
        
        n = 0
        max_value = float('inf')  # Python整数理论上无上限，用时间限制
        start_time = time.time()
        
        try:
            # 快速增长阶段
            while not self.stop_flag and time.time() - start_time < 10:  # 最多查找10秒
                # 指数级增长检测，加速查找
                step = 1
                while True:
                    try:
                        current, _ = fast_doubling(n + step)
                        # 检查是否过大（通过字符串长度判断，避免实际存储超大数）
                        if len(str(current)) > 100000:  # 限制数字大小
                            break
                        n += step
                        step *= 2  # 指数级增长步长
                    except:
                        break
                
                # 精细查找
                for _ in range(1000):  # 每次指数增长后精细查找1000步
                    if self.stop_flag or time.time() - start_time > 10:
                        break
                    try:
                        current, _ = fast_doubling(n + 1)
                        n += 1
                    except:
                        break
        
        finally:
            # 获取最终值
            final_value, _ = fast_doubling(n)
            self.max_iterative_n = n
            self.log(f"迭代法找到的最大斐波那契数是第 {n} 个")
            self.log(f"数值长度: {len(str(final_value))} 位")  # 不显示完整大数，只显示长度
            self.log(f"查找时间: {time.time() - start_time:.2f} 秒")
            self.set_status("查找完成")
    
    # 找最大斐波那契数(递归法) - 优化：使用记忆化递归
    def find_max_recursive(self):
        self.stop_flag = False
        self.set_status("正在用递归法查找最大斐波那契数...")
        threading.Thread(target=self._find_max_recursive, daemon=True).start()
    
    def _find_max_recursive(self):
        max_n = 0
        result = 0
        start_time = time.time()
        
        try:
            # 使用带记忆化的递归，能处理更大的n值
            for n in range(0, 10000):
                if self.stop_flag or time.time() - start_time > 10:  # 最多10秒
                    break
                try:
                    start = time.time()
                    res, _ = self.recursive_wrapper(n)
                    # 单个计算超过1秒则停止
                    if time.time() - start > 1:
                        break
                    max_n = n
                    result = res
                except:
                    break
        
        finally:
            self.log(f"递归法能计算的最大斐波那契数是第 {max_n} 个")
            self.log(f"数值: {str(result)[:50]}...")  # 只显示前50位
            self.log(f"查找时间: {time.time() - start_time:.2f} 秒")
            self.set_status("查找完成")
    
    # 测试公式误差 - 优化：使用二分法加速查找
    def test_formula_error(self):
        self.stop_flag = False
        self.set_status("正在测试公式误差...")
        threading.Thread(target=self._test_formula_error, daemon=True).start()
    
    def _test_formula_error(self):
        # 先快速检查大值，确定误差大致范围
        error_n = -1
        start_time = time.time()
        
        # 先尝试较大的n值，快速定位
        check_points = [10, 50, 100, 500, 1000, 2000, 5000, 10000]
        found = False
        
        for n in check_points:
            if self.stop_flag or time.time() - start_time > 10:
                break
                
            actual, _ = self.fib_iterative_optimized(n)
            formula, _ = self.fib_formula(n)
            
            if actual != formula:
                found = True
                break
        
        if found:
            # 二分法查找最小误差点
            low, high = 0, n
            while low < high:
                if self.stop_flag:
                    break
                    
                mid = (low + high) // 2
                actual, _ = self.fib_iterative(mid)
                formula, _ = self.fib_formula(mid)
                
                if actual != formula:
                    high = mid
                else:
                    low = mid + 1
            
            error_n = low
        else:
            # 未在检查点发现误差，线性查找至2000
            for n in range(0, 2000):
                if self.stop_flag or time.time() - start_time > 10:
                    break
                    
                actual, _ = self.fib_iterative_optimized(n)
                formula, _ = self.fib_formula(n)
                
                if actual != formula:
                    error_n = n
                    break
        
        if error_n != -1 and not self.stop_flag:
            actual, _ = self.fib_iterative(error_n)
            formula, _ = self.fib_formula(error_n)
            self.log(f"公式法首次出现误差的n值: {error_n}")
            self.log(f"实际值: {str(actual)[:50]}...")  # 只显示前50位
            self.log(f"公式计算值: {formula}")
        else:
            self.log("在限定时间或范围内，公式法未出现明显误差")
            
        self.log(f"测试时间: {time.time() - start_time:.2f} 秒")
        self.set_status("测试完成")

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizedFibonacciExperiment(root)
    root.mainloop()
