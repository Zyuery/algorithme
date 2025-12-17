import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple
import time

# 核心算法函数

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
        if dp[i][w] != dp[i - 1][w]:
            selected.append(i - 1)
            weight, _ = items[i - 1]
            w -= weight
    
    selected.reverse()
    return dp[n][capacity], selected


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


# GUI界面

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
    
    def get_capacity(self):
        """获取背包容量"""
        try:
            capacity = int(self.capacity_entry.get())
            if capacity <= 0:
                raise ValueError("背包容量必须大于0")
            return capacity
        except ValueError as e:
            messagebox.showerror("错误", f"请输入有效的背包容量: {e}")
            return None
    
    def output(self, text):
        """输出文本到结果框"""
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)
    
    def clear_output(self):
        """清空输出"""
        self.output_text.delete(1.0, tk.END)
    
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
    
    def solve_01_greedy(self):
        """求解0-1背包问题（贪心算法近似解）"""
        items = self.get_items()
        capacity = self.get_capacity()
        if items is None or capacity is None:
            return
        
        self.clear_output()
        self.output("=" * 50)
        self.output("贪心算法 - 0-1背包问题（近似解）")
        self.output("=" * 50)
        
        start_time = time.time()
        total_value, selected = knapsack_01_greedy(items, capacity)
        elapsed_time = time.time() - start_time
        
        self.output(f"\n近似最大总价值: {total_value}")
        self.output(f"\n选择的物品索引: {[i+1 for i in selected]}")
        self.output(f"\n选择的物品详情:")
        total_weight = 0
        for idx in selected:
            weight, value = items[idx]
            total_weight += weight
            self.output(f"  物品{idx+1}: 重量={weight}, 价值={value}")
        self.output(f"\n总重量: {total_weight}/{capacity}")
        
        self.output(f"\n算法时间复杂度: O(n log n)")
        self.output(f"注意: 此算法不能保证总是得到最优解")
        self.output(f"实际运行时间: {elapsed_time*1000:.4f} 毫秒")
    
    def solve_01_bruteforce(self):
        """求解0-1背包问题（蛮力法）"""
        items = self.get_items()
        capacity = self.get_capacity()
        if items is None or capacity is None:
            return
        
        if len(items) > 20:
            if not messagebox.askyesno("警告", f"物品数量为{len(items)}，蛮力法可能需要很长时间。是否继续？"):
                return
        
        self.clear_output()
        self.output("=" * 50)
        self.output("蛮力法 - 0-1背包问题（最优解）")
        self.output("=" * 50)
        
        start_time = time.time()
        total_value, selected = knapsack_01_bruteforce(items, capacity)
        elapsed_time = time.time() - start_time
        
        self.output(f"\n最大总价值: {total_value}")
        self.output(f"\n选择的物品索引: {[i+1 for i in selected]}")
        self.output(f"\n选择的物品详情:")
        total_weight = 0
        for idx in selected:
            weight, value = items[idx]
            total_weight += weight
            self.output(f"  物品{idx+1}: 重量={weight}, 价值={value}")
        self.output(f"\n总重量: {total_weight}/{capacity}")
        
        self.output(f"\n算法时间复杂度: O(2^n)")
        self.output(f"实际运行时间: {elapsed_time*1000:.4f} 毫秒")
    
    def solve_01_dp(self):
        """求解0-1背包问题（动态规划）"""
        items = self.get_items()
        capacity = self.get_capacity()
        if items is None or capacity is None:
            return
        
        self.clear_output()
        self.output("=" * 50)
        self.output("动态规划 - 0-1背包问题（最优解）")
        self.output("=" * 50)
        
        start_time = time.time()
        total_value, selected = knapsack_01_dp(items, capacity)
        elapsed_time = time.time() - start_time
        
        self.output(f"\n最大总价值: {total_value}")
        self.output(f"\n选择的物品索引: {[i+1 for i in selected]}")
        self.output(f"\n选择的物品详情:")
        total_weight = 0
        for idx in selected:
            weight, value = items[idx]
            total_weight += weight
            self.output(f"  物品{idx+1}: 重量={weight}, 价值={value}")
        self.output(f"\n总重量: {total_weight}/{capacity}")
        
        self.output(f"\n算法时间复杂度: O(n * capacity)")
        self.output(f"空间复杂度: O(n * capacity)")
        self.output(f"实际运行时间: {elapsed_time*1000:.4f} 毫秒")
    
    def solve_01_dp_memo(self):
        """求解0-1背包问题（记忆化动态规划）"""
        items = self.get_items()
        capacity = self.get_capacity()
        if items is None or capacity is None:
            return
        
        self.clear_output()
        self.output("=" * 50)
        self.output("记忆化动态规划 - 0-1背包问题（最优解）")
        self.output("=" * 50)
        
        start_time = time.time()
        total_value, selected = knapsack_01_dp_memo(items, capacity)
        elapsed_time = time.time() - start_time
        
        self.output(f"\n最大总价值: {total_value}")
        self.output(f"\n选择的物品索引: {[i+1 for i in selected]}")
        self.output(f"\n选择的物品详情:")
        total_weight = 0
        for idx in selected:
            weight, value = items[idx]
            total_weight += weight
            self.output(f"  物品{idx+1}: 重量={weight}, 价值={value}")
        self.output(f"\n总重量: {total_weight}/{capacity}")
        
        self.output(f"\n算法时间复杂度: O(n * capacity)（只计算需要的状态）")
        self.output(f"空间复杂度: O(n * capacity)")
        self.output(f"实际运行时间: {elapsed_time*1000:.4f} 毫秒")
    
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


def main():
    root = tk.Tk()
    app = KnapsackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

