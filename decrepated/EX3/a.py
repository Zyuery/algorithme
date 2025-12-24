import sys
import time
from functools import lru_cache
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


class KnapsackSolver:
    def __init__(self):
        self.items = []  # 存储物品 (weight, value)
        self.capacity = 0
        self.n = 0

    def set_problem(self, weights, values, capacity):
        """设置背包问题实例"""
        self.items = list(zip(weights, values))
        self.n = len(weights)
        self.capacity = capacity

    def fractional_knapsack(self):
        """分数背包贪心算法"""
        if self.n == 0:
            return 0, []
        
        # 按单位价值降序排序
        items_with_ratio = [(w, v, v/w) for w, v in self.items]
        items_with_ratio.sort(key=lambda x: x[2], reverse=True)
        
        total_value = 0
        total_weight = 0
        selection = []
        
        for w, v, ratio in items_with_ratio:
            if total_weight + w <= self.capacity:
                # 能装下整个物品
                total_weight += w
                total_value += v
                selection.append((w, v, 1.0))  # 1.0表示全选
            else:
                # 只能装部分
                remaining = self.capacity - total_weight
                fraction = remaining / w
                total_value += v * fraction
                selection.append((w, v, fraction))
                break
        
        return total_value, selection

    def zero_one_knapsack_greedy(self):
        """0-1背包贪心近似算法（按单位价值）"""
        if self.n == 0:
            return 0, []
        
        # 按单位价值降序排序，保留原始索引
        indexed_items = [(i, w, v, v/w) for i, (w, v) in enumerate(self.items)]
        indexed_items.sort(key=lambda x: x[3], reverse=True)
        
        total_value = 0
        total_weight = 0
        selection = [0] * self.n
        
        for i, w, v, ratio in indexed_items:
            if total_weight + w <= self.capacity:
                total_weight += w
                total_value += v
                selection[i] = 1
        
        return total_value, selection

    def zero_one_knapsack_brute_force(self):
        """0-1背包蛮力法（枚举所有子集）"""
        max_value = 0
        best_selection = [0] * self.n
        
        # 枚举所有可能的子集 (0 ~ 2^n - 1)
        for mask in range(0, 1 << self.n):
            current_weight = 0
            current_value = 0
            current_selection = [0] * self.n
            
            for i in range(self.n):
                if mask & (1 << i):
                    current_weight += self.items[i][0]
                    current_value += self.items[i][1]
            
            if current_weight <= self.capacity and current_value > max_value:
                max_value = current_value
                best_selection = [(mask & (1 << i)) != 0 for i in range(self.n)]
        
        return max_value, best_selection

    def zero_one_knapsack_dp(self):
        """0-1背包动态规划算法（二维数组）"""
        # 创建dp表，dp[i][j]表示前i个物品，容量j的最大价值
        dp = [[0] * (self.capacity + 1) for _ in range(self.n + 1)]
        
        for i in range(1, self.n + 1):
            w, v = self.items[i-1]
            for j in range(1, self.capacity + 1):
                if j < w:
                    # 装不下第i个物品
                    dp[i][j] = dp[i-1][j]
                else:
                    # 选或不选第i个物品，取最大值
                    dp[i][j] = max(dp[i-1][j], dp[i-1][j-w] + v)
        
        # 回溯找到选择的物品
        selection = [0] * self.n
        j = self.capacity
        for i in range(self.n, 0, -1):
            if dp[i][j] != dp[i-1][j]:
                selection[i-1] = 1
                j -= self.items[i-1][0]
        
        return dp[self.n][self.capacity], selection

    def zero_one_knapsack_memoization(self):
        """0-1背包记忆化递归算法"""
        # 使用lru_cache缓存结果
        @lru_cache(maxsize=None)
        def dp(i, j):
            if i == 0 or j == 0:
                return 0
            w, v = self.items[i-1]
            if j < w:
                return dp(i-1, j)
            else:
                return max(dp(i-1, j), dp(i-1, j-w) + v)
        
        max_value = dp(self.n, self.capacity)
        
        # 回溯找选择
        selection = [0] * self.n
        j = self.capacity
        for i in range(self.n, 0, -1):
            if dp(i, j) != dp(i-1, j):
                selection[i-1] = 1
                j -= self.items[i-1][0]
        
        # 清除缓存
        dp.cache_clear()
        return max_value, selection

    def show_greedy_counterexample(self):
        """展示0-1背包贪心算法的反例"""
        counterexample = {
            "weights": [3, 2, 2],
            "values": [5, 3, 3],
            "capacity": 4
        }
        
        # 贪心算法结果（按单位价值排序：物品0(5/3≈1.67), 物品1(1.5), 物品2(1.5)）
        greedy_selection = [1, 0, 0]  # 选物品0，总价值5，重量3
        greedy_value = 5
        
        # 最优解（选物品1和2）
        optimal_selection = [0, 1, 1]  # 总价值6，重量4
        optimal_value = 6
        
        return counterexample, greedy_value, greedy_selection, optimal_value, optimal_selection


class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("背包问题求解系统")
        self.root.geometry("800x600")
        
        self.solver = KnapsackSolver()
        
        self._create_widgets()
    
    def _create_widgets(self):
        # 输入区域
        input_frame = ttk.LabelFrame(self.root, text="问题输入")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 物品数量
        ttk.Label(input_frame, text="物品数量:").grid(row=0, column=0, padx=5, pady=5)
        self.n_entry = ttk.Entry(input_frame, width=10)
        self.n_entry.grid(row=0, column=1, padx=5, pady=5)
        self.n_entry.insert(0, "3")
        
        # 背包容量
        ttk.Label(input_frame, text="背包容量:").grid(row=0, column=2, padx=5, pady=5)
        self.capacity_entry = ttk.Entry(input_frame, width=10)
        self.capacity_entry.grid(row=0, column=3, padx=5, pady=5)
        self.capacity_entry.insert(0, "5")
        
        # 物品详情输入区域
        self.items_frame = ttk.LabelFrame(self.root, text="物品详情")
        self.items_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 添加默认物品行
        self._update_item_entries(3)
        
        # 更新物品数量按钮
        ttk.Button(input_frame, text="更新物品行", command=self._update_item_entries).grid(row=0, column=4, padx=5, pady=5)
        
        # 算法选择区域
        algo_frame = ttk.LabelFrame(self.root, text="算法选择")
        algo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.algo_var = tk.StringVar()
        algos = [
            ("分数背包贪心算法", "fractional"),
            ("0-1背包贪心近似算法", "zero_one_greedy"),
            ("0-1背包蛮力法", "zero_one_brute"),
            ("0-1背包动态规划", "zero_one_dp"),
            ("0-1背包记忆化递归", "zero_one_memo"),
            ("展示贪心反例", "counterexample")
        ]
        
        for text, value in algos:
            ttk.Radiobutton(algo_frame, text=text, variable=self.algo_var, value=value).pack(side=tk.LEFT, padx=10)
        
        self.algo_var.set("fractional")
        
        # 执行按钮 - 修复：使用self.root而不是root
        ttk.Button(self.root, text="执行计算", command=self._run_algorithm).pack(pady=10)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(self.root, text="结果输出")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, width=100, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def _update_item_entries(self, n=None):
        """更新物品输入行"""
        if n is None:
            try:
                n = int(self.n_entry.get())
            except ValueError:
                messagebox.showerror("错误", "物品数量必须是整数！")
                return
        
        # 清除现有内容
        for widget in self.items_frame.winfo_children():
            widget.destroy()
        
        # 添加表头
        ttk.Label(self.items_frame, text="物品").grid(row=0, column=0, padx=10, pady=5)
        ttk.Label(self.items_frame, text="重量").grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(self.items_frame, text="价值").grid(row=0, column=2, padx=10, pady=5)
        
        # 存储条目引用
        self.weight_entries = []
        self.value_entries = []
        
        # 添加物品行
        for i in range(n):
            ttk.Label(self.items_frame, text=f"物品{i+1}:").grid(row=i+1, column=0, padx=10, pady=5)
            
            w_entry = ttk.Entry(self.items_frame, width=10)
            w_entry.grid(row=i+1, column=1, padx=10, pady=5)
            w_entry.insert(0, str(i+1))
            self.weight_entries.append(w_entry)
            
            v_entry = ttk.Entry(self.items_frame, width=10)
            v_entry.grid(row=i+1, column=2, padx=10, pady=5)
            v_entry.insert(0, str((i+1)*2))
            self.value_entries.append(v_entry)
    
    def _get_input_data(self):
        """获取输入数据"""
        try:
            n = int(self.n_entry.get())
            capacity = int(self.capacity_entry.get())
            
            weights = []
            values = []
            for w_entry, v_entry in zip(self.weight_entries, self.value_entries):
                w = int(w_entry.get())
                v = int(v_entry.get())
                weights.append(w)
                values.append(v)
            
            return weights, values, capacity
        except ValueError as e:
            messagebox.showerror("输入错误", f"请输入有效的整数！{e}")
            return None, None, None
    
    def _run_algorithm(self):
        """执行选择的算法"""
        self.result_text.delete(1.0, tk.END)
        
        algo = self.algo_var.get()
        
        if algo == "counterexample":
            self._show_counterexample()
            return
        
        weights, values, capacity = self._get_input_data()
        if weights is None:
            return
        
        self.solver.set_problem(weights, values, capacity)
        
        start_time = time.time()
        
        if algo == "fractional":
            max_value, selection = self.solver.fractional_knapsack()
            self._display_fractional_result(max_value, selection)
        elif algo == "zero_one_greedy":
            max_value, selection = self.solver.zero_one_knapsack_greedy()
            self._display_zero_one_result(max_value, selection, "贪心近似算法")
        elif algo == "zero_one_brute":
            max_value, selection = self.solver.zero_one_knapsack_brute_force()
            self._display_zero_one_result(max_value, selection, "蛮力法")
        elif algo == "zero_one_dp":
            max_value, selection = self.solver.zero_one_knapsack_dp()
            self._display_zero_one_result(max_value, selection, "动态规划")
        elif algo == "zero_one_memo":
            max_value, selection = self.solver.zero_one_knapsack_memoization()
            self._display_zero_one_result(max_value, selection, "记忆化递归")
        
        end_time = time.time()
        self.result_text.insert(tk.END, f"\n计算耗时: {end_time - start_time:.6f} 秒")
    
    def _display_fractional_result(self, max_value, selection):
        """显示分数背包结果"""
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, "分数背包贪心算法结果\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"背包容量: {self.solver.capacity}\n")
        self.result_text.insert(tk.END, f"最大总价值: {max_value:.2f}\n\n")
        self.result_text.insert(tk.END, "物品选择详情:\n")
        
        total_weight = 0
        for i, (w, v, fraction) in enumerate(selection):
            if fraction == 1.0:
                self.result_text.insert(tk.END, f"物品{i+1}: 重量={w}, 价值={v}, 选择比例=100%\n")
                total_weight += w
            else:
                self.result_text.insert(tk.END, f"物品{i+1}: 重量={w}, 价值={v}, 选择比例={fraction*100:.1f}% (实际重量={w*fraction:.1f})\n")
                total_weight += w * fraction
        
        self.result_text.insert(tk.END, f"\n总重量: {total_weight:.2f}")
        self.result_text.insert(tk.END, f"\n\n时间复杂度分析: O(n log n) (主要来自排序)")
    
    def _display_zero_one_result(self, max_value, selection, algo_name):
        """显示0-1背包结果"""
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"0-1背包{algo_name}结果\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, f"背包容量: {self.solver.capacity}\n")
        self.result_text.insert(tk.END, f"最大总价值: {max_value}\n\n")
        self.result_text.insert(tk.END, "物品选择详情:\n")
        
        total_weight = 0
        selected_items = []
        for i, (w, v) in enumerate(self.solver.items):
            if selection[i]:
                self.result_text.insert(tk.END, f"物品{i+1}: 重量={w}, 价值={v} ✅\n")
                total_weight += w
                selected_items.append(i+1)
            else:
                self.result_text.insert(tk.END, f"物品{i+1}: 重量={w}, 价值={v} ❌\n")
        
        self.result_text.insert(tk.END, f"\n选中物品: {selected_items}")
        self.result_text.insert(tk.END, f"\n总重量: {total_weight}")
        
        # 时间复杂度分析
        if algo_name == "贪心近似算法":
            self.result_text.insert(tk.END, f"\n\n时间复杂度分析: O(n log n) (主要来自排序)")
        elif algo_name == "蛮力法":
            self.result_text.insert(tk.END, f"\n\n时间复杂度分析: O(2^n) (枚举所有子集)")
        else:
            self.result_text.insert(tk.END, f"\n\n时间复杂度分析: O(nC) (n为物品数，C为背包容量)")
    
    def _show_counterexample(self):
        """展示贪心算法反例"""
        counterexample, greedy_value, greedy_sel, optimal_value, optimal_sel = self.solver.show_greedy_counterexample()
        
        self.result_text.insert(tk.END, "="*60 + "\n")
        self.result_text.insert(tk.END, "0-1背包贪心算法反例\n")
        self.result_text.insert(tk.END, "="*60 + "\n\n")
        
        self.result_text.insert(tk.END, "问题实例:\n")
        self.result_text.insert(tk.END, f"物品1: 重量={counterexample['weights'][0]}, 价值={counterexample['values'][0]}, 单位价值={counterexample['values'][0]/counterexample['weights'][0]:.2f}\n")
        self.result_text.insert(tk.END, f"物品2: 重量={counterexample['weights'][1]}, 价值={counterexample['values'][1]}, 单位价值={counterexample['values'][1]/counterexample['weights'][1]:.2f}\n")
        self.result_text.insert(tk.END, f"物品3: 重量={counterexample['weights'][2]}, 价值={counterexample['values'][2]}, 单位价值={counterexample['values'][2]/counterexample['weights'][2]:.2f}\n")
        self.result_text.insert(tk.END, f"背包容量: {counterexample['capacity']}\n\n")
        
        self.result_text.insert(tk.END, "贪心算法选择:\n")
        self.result_text.insert(tk.END, f"选择物品: {[i+1 for i, sel in enumerate(greedy_sel) if sel]}\n")
        self.result_text.insert(tk.END, f"总价值: {greedy_value}\n")
        self.result_text.insert(tk.END, f"总重量: {sum(w for i, w in enumerate(counterexample['weights']) if greedy_sel[i])}\n\n")
        
        self.result_text.insert(tk.END, "最优解选择:\n")
        self.result_text.insert(tk.END, f"选择物品: {[i+1 for i, sel in enumerate(optimal_sel) if sel]}\n")
        self.result_text.insert(tk.END, f"总价值: {optimal_value}\n")
        self.result_text.insert(tk.END, f"总重量: {sum(w for i, w in enumerate(counterexample['weights']) if optimal_sel[i])}\n\n")
        
        self.result_text.insert(tk.END, "结论: 贪心算法无法保证得到0-1背包问题的最优解！")


def main():
    """主函数"""
    root = tk.Tk()
    app = KnapsackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()