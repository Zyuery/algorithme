"""
检索算法实验程序
包含核心算法：顺序查找、二分查找、三分查找
"""

import random
import time
from tkinter import *
from tkinter import scrolledtext, messagebox

# ==================== 核心算法部分 ====================

def sequentialSearch(arr, target):
    """
    顺序查找算法
    时间复杂度：O(n)
    返回：(位置索引, 比较次数)
    """
    comparisons = 0
    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            return i, comparisons
    return -1, comparisons


def binarySearch(arr, target):
    """
    二分查找算法（要求数组已排序）
    时间复杂度：O(log n)
    返回：(位置索引, 比较次数, 最接近的元素信息)
    """
    comparisons = 0
    left = 0
    right = len(arr) - 1
    closestIdx = -1
    closestDiff = float('inf')
    
    while left <= right:
        mid = (left + right) // 2
        comparisons += 1
        
        if arr[mid] == target:
            return mid, comparisons, (arr[mid], mid)
        
        # 记录最接近的元素
        diff = abs(arr[mid] - target)
        if diff < closestDiff:
            closestDiff = diff
            closestIdx = mid
        
        comparisons += 1
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    # 如果没找到，检查边界值
    if closestIdx == -1:
        if left < len(arr):
            closestIdx = left
        elif right >= 0:
            closestIdx = right
    
    closestInfo = (arr[closestIdx], closestIdx) if closestIdx != -1 else None
    return -1, comparisons, closestInfo


def ternarySearch(arr, target):
    """
    三分查找算法（要求数组已排序）
    时间复杂度：O(log3 n)
    返回：(位置索引, 比较次数, 最接近的元素信息)
    """
    comparisons = 0
    left = 0
    right = len(arr) - 1
    closestIdx = -1
    closestDiff = float('inf')
    
    while left <= right:
        if right - left < 2:
            # 区间太小，用顺序查找
            for i in range(left, right + 1):
                comparisons += 1
                diff = abs(arr[i] - target)
                if diff < closestDiff:
                    closestDiff = diff
                    closestIdx = i
                if arr[i] == target:
                    closestInfo = (arr[closestIdx], closestIdx) if closestIdx != -1 else None
                    return i, comparisons, closestInfo
            break
        
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        comparisons += 1
        if arr[mid1] == target:
            return mid1, comparisons, (arr[mid1], mid1)
        
        comparisons += 1
        if arr[mid2] == target:
            return mid2, comparisons, (arr[mid2], mid2)
        
        # 记录最接近的元素
        diff1 = abs(arr[mid1] - target)
        diff2 = abs(arr[mid2] - target)
        if diff1 < closestDiff:
            closestDiff = diff1
            closestIdx = mid1
        if diff2 < closestDiff:
            closestDiff = diff2
            closestIdx = mid2
        
        comparisons += 1
        if target < arr[mid1]:
            right = mid1 - 1
        elif target > arr[mid2]:
            left = mid2 + 1
        else:
            left = mid1 + 1
            right = mid2 - 1
    
    closestInfo = (arr[closestIdx], closestIdx) if closestIdx != -1 else None
    return -1, comparisons, closestInfo


def ternarySearchPeak(arr, findMax=True):
    """
    三分查找找峰值（最大值或最小值）
    用于先升后降或先降后升数组
    时间复杂度：O(log3 n)
    返回：(位置索引, 值, 比较次数)
    """
    comparisons = 0
    left = 0
    right = len(arr) - 1
    
    while right - left > 2:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        comparisons += 2
        if findMax:
            if arr[mid1] < arr[mid2]:
                left = mid1 + 1
            else:
                right = mid2 - 1
        else:
            if arr[mid1] > arr[mid2]:
                left = mid1 + 1
            else:
                right = mid2 - 1
    
    # 在剩余区间找最值
    if findMax:
        maxIdx = left
        for i in range(left + 1, right + 1):
            comparisons += 1
            if arr[i] > arr[maxIdx]:
                maxIdx = i
        return maxIdx, arr[maxIdx], comparisons
    else:
        minIdx = left
        for i in range(left + 1, right + 1):
            comparisons += 1
            if arr[i] < arr[minIdx]:
                minIdx = i
        return minIdx, arr[minIdx], comparisons


def binarySearchPeak(arr, findMax=True):
    """
    二分查找找峰值（最大值或最小值）
    用于先升后降或先降后升数组
    时间复杂度：O(log n)
    返回：(位置索引, 值, 比较次数)
    """
    comparisons = 0
    left = 0
    right = len(arr) - 1
    
    while left < right:
        mid = (left + right) // 2
        comparisons += 1
        
        if findMax:
            if arr[mid] < arr[mid + 1]:
                left = mid + 1
            else:
                right = mid
        else:
            if arr[mid] > arr[mid + 1]:
                left = mid + 1
            else:
                right = mid
    
    return left, arr[left], comparisons


# ==================== 辅助算法 ====================

def checkArrayOrder(arr):
    """
    判断数组的排序状态
    返回：0-未排序, 1-升序, 2-降序, 3-先升后降, 4-先降后升
    """
    if len(arr) <= 1:
        return 1  # 单个元素视为升序
    
    # 检查是否完全升序
    isAscending = all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    if isAscending:
        return 1
    
    # 检查是否完全降序
    isDescending = all(arr[i] >= arr[i + 1] for i in range(len(arr) - 1))
    if isDescending:
        return 2
    
    # 找峰值点
    peakIdx = -1
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1]:
            peakIdx = i
            break
    
    if peakIdx != -1:
        # 检查峰值前是否升序，峰值后是否降序
        beforeAsc = all(arr[i] <= arr[i + 1] for i in range(peakIdx))
        afterDesc = all(arr[i] >= arr[i + 1] for i in range(peakIdx, len(arr) - 1))
        if beforeAsc and afterDesc:
            return 3
    
    # 找谷值点
    valleyIdx = -1
    for i in range(1, len(arr) - 1):
        if arr[i] < arr[i - 1] and arr[i] < arr[i + 1]:
            valleyIdx = i
            break
    
    if valleyIdx != -1:
        # 检查谷值前是否降序，谷值后是否升序
        beforeDesc = all(arr[i] >= arr[i + 1] for i in range(valleyIdx))
        afterAsc = all(arr[i] <= arr[i + 1] for i in range(valleyIdx, len(arr) - 1))
        if beforeDesc and afterAsc:
            return 4
    
    return 0  # 未排序


def findKthSmallestBruteForce(arr, k):
    """
    蛮力法找第k个最小元素
    时间复杂度：O(n*k)
    返回：(元素值, 位置索引, 比较次数)
    """
    if k < 1 or k > len(arr):
        return None, -1, 0
    
    comparisons = 0
    arrCopy = arr.copy()
    
    for i in range(k):
        minIdx = i
        for j in range(i + 1, len(arrCopy)):
            comparisons += 1
            if arrCopy[j] < arrCopy[minIdx]:
                minIdx = j
        arrCopy[i], arrCopy[minIdx] = arrCopy[minIdx], arrCopy[i]
    
    kthValue = arrCopy[k - 1]
    # 在原数组中找到该值的位置
    originalIdx = arr.index(kthValue)
    return kthValue, originalIdx, comparisons


def findKthSmallestPreSort(arr, k):
    """
    预排序法找第k个最小元素（使用快速排序）
    时间复杂度：O(n log n)
    返回：(元素值, 位置索引, 比较次数)
    """
    if k < 1 or k > len(arr):
        return None, -1, 0
    
    # 使用快速排序
    sortedArr, comparisons = quickSort(arr)
    kthValue = sortedArr[k - 1]
    originalIdx = arr.index(kthValue)
    
    return kthValue, originalIdx, comparisons


def quickSort(arr):
    """
    快速排序算法
    时间复杂度：平均O(n log n)，最坏O(n^2)
    返回：(排序后的数组, 比较次数)
    """
    if len(arr) <= 1:
        return arr, 0
    
    comparisons = 0
    arrCopy = arr.copy()
    
    def partition(low, high):
        nonlocal comparisons
        pivot = arrCopy[high]
        i = low - 1
        
        for j in range(low, high):
            comparisons += 1
            if arrCopy[j] <= pivot:
                i += 1
                arrCopy[i], arrCopy[j] = arrCopy[j], arrCopy[i]
        
        arrCopy[i + 1], arrCopy[high] = arrCopy[high], arrCopy[i + 1]
        return i + 1
    
    def quickSortRecursive(low, high):
        nonlocal comparisons
        if low < high:
            pi = partition(low, high)
            quickSortRecursive(low, pi - 1)
            quickSortRecursive(pi + 1, high)
    
    quickSortRecursive(0, len(arrCopy) - 1)
    return arrCopy, comparisons


# ==================== GUI部分 ====================

class SearchGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("检索算法实验")
        self.root.geometry("900x750")
        
        self.currentArray = []
        
        # 数组生成区域
        arrayFrame = Frame(root)
        arrayFrame.pack(pady=10)
        
        Label(arrayFrame, text="数组长度n:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        self.nEntry = Entry(arrayFrame, width=15, font=("Arial", 12))
        self.nEntry.pack(side=LEFT, padx=5)
        
        Button(arrayFrame, text="随机生成数组", command=self.generateRandomArray, 
               width=15, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(arrayFrame, text="手动输入数组", command=self.inputArrayManually, 
               width=15, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(arrayFrame, text="快速排序", command=self.sortArray, 
               width=15, font=("Arial", 10), bg="lightgreen").pack(side=LEFT, padx=5)
        
        Label(arrayFrame, text="当前数组:", font=("Arial", 10)).pack(side=LEFT, padx=5)
        self.arrayLabel = Label(arrayFrame, text="[]", font=("Arial", 10), fg="blue")
        self.arrayLabel.pack(side=LEFT, padx=5)
        
        # 功能按钮区域
        buttonFrame1 = Frame(root)
        buttonFrame1.pack(pady=10)
        
        Button(buttonFrame1, text="功能3: 判断数组排序状态", command=self.checkOrder, 
               width=25, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(buttonFrame1, text="功能4: 顺序检索", command=self.sequentialSearchFunc, 
               width=25, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        
        buttonFrame2 = Frame(root)
        buttonFrame2.pack(pady=10)
        
        Button(buttonFrame2, text="功能5: 多种方法检索", command=self.multipleSearch, 
               width=25, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Button(buttonFrame2, text="功能6: 查找峰值", command=self.findPeak, 
               width=25, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        
        buttonFrame3 = Frame(root)
        buttonFrame3.pack(pady=10)
        
        Button(buttonFrame3, text="功能7: 查找第k小元素", command=self.findKthSmallest, 
               width=25, height=2, font=("Arial", 10)).pack(side=LEFT, padx=5)
        
        # 输入框区域（用于功能4、5、7）
        inputFrame = Frame(root)
        inputFrame.pack(pady=10)
        
        Label(inputFrame, text="查找元素:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        self.targetEntry = Entry(inputFrame, width=15, font=("Arial", 12))
        self.targetEntry.pack(side=LEFT, padx=5)
        
        Label(inputFrame, text="k值:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        self.kEntry = Entry(inputFrame, width=15, font=("Arial", 12))
        self.kEntry.pack(side=LEFT, padx=5)
        
        # 输出文本框
        outputFrame = Frame(root)
        outputFrame.pack(pady=10, padx=10, fill=BOTH, expand=True)
        
        Label(outputFrame, text="输出结果:", font=("Arial", 12)).pack(anchor=W)
        self.outputText = scrolledtext.ScrolledText(outputFrame, width=90, height=25, 
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
    
    def generateRandomArray(self):
        """随机生成数组"""
        try:
            n = int(self.nEntry.get())
            if n <= 0:
                messagebox.showerror("错误", "数组长度必须为正整数")
                return
            if n > 1000:
                messagebox.showwarning("警告", "数组长度过大，建议不超过1000")
            
            # 生成0到n*2范围内的n个不重复随机数
            maxVal = n * 2
            self.currentArray = random.sample(range(maxVal), n)
            
            self.arrayLabel.config(text=str(self.currentArray[:20]) + ("..." if len(self.currentArray) > 20 else ""))
            self.appendOutput(f"\n{'='*60}")
            self.appendOutput(f"随机生成数组（长度={n}）")
            self.appendOutput(f"数组: {self.currentArray}")
            self.appendOutput("")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的整数")
        except Exception as e:
            messagebox.showerror("错误", f"生成数组失败: {str(e)}")
    
    def inputArrayManually(self):
        """手动输入数组"""
        dialog = Toplevel(self.root)
        dialog.title("手动输入数组")
        dialog.geometry("500x200")
        
        Label(dialog, text="请输入数组元素（用逗号或空格分隔）:", font=("Arial", 12)).pack(pady=10)
        
        entry = Entry(dialog, width=60, font=("Arial", 12))
        entry.pack(pady=10)
        
        def confirm():
            try:
                text = entry.get().strip()
                # 支持逗号或空格分隔
                if ',' in text:
                    elements = [int(x.strip()) for x in text.split(',')]
                else:
                    elements = [int(x.strip()) for x in text.split()]
                
                # 检查是否有重复
                if len(elements) != len(set(elements)):
                    messagebox.showerror("错误", "数组元素必须互不相同")
                    return
                
                self.currentArray = elements
                self.nEntry.delete(0, END)
                self.nEntry.insert(0, str(len(elements)))
                self.arrayLabel.config(text=str(self.currentArray[:20]) + ("..." if len(self.currentArray) > 20 else ""))
                self.appendOutput(f"\n{'='*60}")
                self.appendOutput(f"手动输入数组（长度={len(elements)}）")
                self.appendOutput(f"数组: {self.currentArray}")
                self.appendOutput("")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "请输入有效的整数")
            except Exception as e:
                messagebox.showerror("错误", f"输入失败: {str(e)}")
        
        Button(dialog, text="确认", command=confirm, width=15, font=("Arial", 10)).pack(pady=10)
    
    def sortArray(self):
        """快速排序数组"""
        if not self.currentArray:
            messagebox.showwarning("警告", "请先生成或输入数组")
            return
        
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("快速排序")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput(f"排序前数组: {self.currentArray}")
        self.appendOutput(f"数组长度: {len(self.currentArray)}\n")
        
        startTime = time.time()
        sortedArray, comparisons = quickSort(self.currentArray)
        endTime = time.time()
        elapsedTime = (endTime - startTime) * 1000  # 转换为毫秒
        
        self.currentArray = sortedArray
        
        self.appendOutput(f"排序后数组: {sortedArray}")
        self.appendOutput(f"关键字比较次数: {comparisons}")
        self.appendOutput(f"执行时间: {elapsedTime:.6f} 毫秒")
        self.appendOutput("")
        
        # 更新显示
        self.arrayLabel.config(text=str(self.currentArray[:20]) + ("..." if len(self.currentArray) > 20 else ""))
    
    def checkOrder(self):
        """功能3: 判断数组排序状态"""
        if not self.currentArray:
            messagebox.showwarning("警告", "请先生成或输入数组")
            return
        
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能3: 判断数组排序状态")
        self.appendOutput(f"{'='*60}\n")
        
        orderType = checkArrayOrder(self.currentArray)
        orderNames = {
            0: "未排序",
            1: "升序",
            2: "降序",
            3: "先升后降",
            4: "先降后升"
        }
        
        self.appendOutput(f"数组: {self.currentArray}")
        self.appendOutput(f"排序状态: {orderType} ({orderNames[orderType]})")
        self.appendOutput("")
    
    def sequentialSearchFunc(self):
        """功能4: 顺序检索"""
        if not self.currentArray:
            messagebox.showwarning("警告", "请先生成或输入数组")
            return
        
        try:
            target = int(self.targetEntry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的查找元素")
            return
        
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能4: 顺序检索算法")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput(f"数组: {self.currentArray}")
        self.appendOutput(f"查找元素: {target}\n")
        
        position, comparisons = sequentialSearch(self.currentArray, target)
        
        if position != -1:
            self.appendOutput(f"✓ 找到元素！")
            self.appendOutput(f"位置索引: {position}")
        else:
            self.appendOutput(f"✗ 未找到元素")
            self.appendOutput(f"位置索引: -1")
        
        self.appendOutput(f"关键字比较次数: {comparisons}")
        self.appendOutput("")
    
    def multipleSearch(self):
        """功能5: 多种方法检索（顺序、二分、三分）"""
        if not self.currentArray:
            messagebox.showwarning("警告", "请先生成或输入数组")
            return
        
        try:
            target = int(self.targetEntry.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的查找元素")
            return
        
        originalOrderType = checkArrayOrder(self.currentArray)
        orderNames = ["未排序", "升序", "降序", "先升后降", "先降后升"]
        
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能5: 多种方法检索（顺序、二分、三分）")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput(f"原数组: {self.currentArray}")
        self.appendOutput(f"原数组状态: {orderNames[originalOrderType]}")
        self.appendOutput(f"查找元素: {target}\n")
        
        # 复制数组用于查找
        searchArray = self.currentArray.copy()
        sortComparisons = 0
        isSorted = False
        
        # 如果数组不是升序或降序，自动使用快排排序
        if originalOrderType not in [1, 2]:
            self.appendOutput(f"数组不是升序或降序，自动使用快速排序...")
            sortedArray, sortComparisons = quickSort(searchArray)
            searchArray = sortedArray
            isSorted = True
            self.appendOutput(f"排序完成，排序比较次数: {sortComparisons}")
            self.appendOutput(f"排序后数组: {searchArray}\n")
        elif originalOrderType == 2:
            # 如果是降序，反转数组用于查找
            searchArray = searchArray[::-1]
            self.appendOutput("注意: 数组为降序，已反转用于查找\n")
        
        # 顺序查找（在原数组上查找，不需要排序）
        pos1, comp1 = sequentialSearch(self.currentArray, target)
        
        self.appendOutput("【顺序查找】")
        if pos1 != -1:
            self.appendOutput(f"  找到！位置索引: {pos1}")
        else:
            self.appendOutput(f"  未找到，位置索引: -1")
        self.appendOutput(f"  比较次数: {comp1}\n")
        
        # 二分查找（在排序后的数组上查找）
        pos2, comp2, closest2 = binarySearch(searchArray, target)
        # 映射位置索引到原数组
        if isSorted:
            # 排序后的位置，需要找到在原数组中的位置
            if pos2 != -1:
                originalPos2 = self.currentArray.index(searchArray[pos2])
            else:
                originalPos2 = -1
            if closest2:
                originalClosest2 = self.currentArray.index(closest2[0])
                closest2 = (closest2[0], originalClosest2)
        elif originalOrderType == 2:
            # 原数组是降序，反转后的位置需要转换
            if pos2 != -1:
                originalPos2 = len(searchArray) - 1 - pos2
            else:
                originalPos2 = -1
            if closest2:
                originalClosest2 = len(searchArray) - 1 - closest2[1]
                closest2 = (closest2[0], originalClosest2)
        else:  # 原数组是升序
            originalPos2 = pos2
        
        self.appendOutput("【二分查找】")
        if originalPos2 != -1:
            self.appendOutput(f"  找到！位置索引: {originalPos2} (原数组中的位置)")
        else:
            self.appendOutput(f"  未找到，位置索引: -1")
            if closest2:
                self.appendOutput(f"  最接近的元素: 值={closest2[0]}, 位置={closest2[1]} (原数组中的位置)")
        self.appendOutput(f"  查找比较次数: {comp2}")
        if sortComparisons > 0:
            self.appendOutput(f"  排序比较次数: {sortComparisons}")
            self.appendOutput(f"  总比较次数: {comp2 + sortComparisons}\n")
        else:
            self.appendOutput("")
        
        # 三分查找（在排序后的数组上查找）
        pos3, comp3, closest3 = ternarySearch(searchArray, target)
        # 映射位置索引到原数组
        if isSorted:
            # 排序后的位置，需要找到在原数组中的位置
            if pos3 != -1:
                originalPos3 = self.currentArray.index(searchArray[pos3])
            else:
                originalPos3 = -1
            if closest3:
                originalClosest3 = self.currentArray.index(closest3[0])
                closest3 = (closest3[0], originalClosest3)
        elif originalOrderType == 2:
            # 原数组是降序，反转后的位置需要转换
            if pos3 != -1:
                originalPos3 = len(searchArray) - 1 - pos3
            else:
                originalPos3 = -1
            if closest3:
                originalClosest3 = len(searchArray) - 1 - closest3[1]
                closest3 = (closest3[0], originalClosest3)
        else:  # 原数组是升序
            originalPos3 = pos3
        
        self.appendOutput("【三分查找】")
        if originalPos3 != -1:
            self.appendOutput(f"  找到！位置索引: {originalPos3} (原数组中的位置)")
        else:
            self.appendOutput(f"  未找到，位置索引: -1")
            if closest3:
                self.appendOutput(f"  最接近的元素: 值={closest3[0]}, 位置={closest3[1]} (原数组中的位置)")
        self.appendOutput(f"  查找比较次数: {comp3}")
        if sortComparisons > 0:
            self.appendOutput(f"  排序比较次数: {sortComparisons}")
            self.appendOutput(f"  总比较次数: {comp3 + sortComparisons}\n")
        else:
            self.appendOutput("")
        
        self.appendOutput("")
    
    def findPeak(self):
        """功能6: 查找峰值（最大值或最小值）"""
        if not self.currentArray:
            messagebox.showwarning("警告", "请先生成或输入数组")
            return
        
        orderType = checkArrayOrder(self.currentArray)
        if orderType not in [3, 4]:
            messagebox.showwarning("警告", "此功能需要先升后降或先降后升数组，当前数组状态为: " + 
                                  ["未排序", "升序", "降序", "先升后降", "先降后升"][orderType])
            return
        
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能6: 查找峰值（二分和三分检索）")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput(f"数组: {self.currentArray}")
        self.appendOutput(f"数组状态: {'先升后降' if orderType == 3 else '先降后升'}\n")
        
        findMax = (orderType == 3)  # 先升后降找最大值，先降后升找最小值
        
        # 二分查找峰值
        idx1, val1, comp1 = binarySearchPeak(self.currentArray, findMax)
        self.appendOutput("【二分检索】")
        self.appendOutput(f"  找到{'最大值' if findMax else '最小值'}: {val1}")
        self.appendOutput(f"  位置索引: {idx1}")
        self.appendOutput(f"  比较次数: {comp1}\n")
        
        # 三分查找峰值
        idx2, val2, comp2 = ternarySearchPeak(self.currentArray, findMax)
        self.appendOutput("【三分检索】")
        self.appendOutput(f"  找到{'最大值' if findMax else '最小值'}: {val2}")
        self.appendOutput(f"  位置索引: {idx2}")
        self.appendOutput(f"  比较次数: {comp2}\n")
        
        self.appendOutput("")
    
    def findKthSmallest(self):
        """功能7: 查找第k个最小元素"""
        if not self.currentArray:
            messagebox.showwarning("警告", "请先生成或输入数组")
            return
        
        try:
            k = int(self.kEntry.get())
            if k < 1 or k > len(self.currentArray):
                messagebox.showerror("错误", f"k值必须在1到{len(self.currentArray)}之间")
                return
        except ValueError:
            messagebox.showerror("错误", "请输入有效的k值")
            return
        
        self.appendOutput(f"\n{'='*60}")
        self.appendOutput("功能7: 查找第k个最小元素（蛮力法和预排序）")
        self.appendOutput(f"{'='*60}\n")
        
        self.appendOutput(f"数组: {self.currentArray}")
        self.appendOutput(f"k = {k}\n")
        
        # 蛮力法
        val1, idx1, comp1 = findKthSmallestBruteForce(self.currentArray, k)
        self.appendOutput("【蛮力法】")
        self.appendOutput(f"  第{k}个最小元素: {val1}")
        self.appendOutput(f"  位置索引: {idx1}")
        self.appendOutput(f"  比较次数: {comp1}\n")
        
        # 预排序法（使用快速排序）
        val2, idx2, comp2 = findKthSmallestPreSort(self.currentArray, k)
        self.appendOutput("【预排序法（快速排序）】")
        self.appendOutput(f"  第{k}个最小元素: {val2}")
        self.appendOutput(f"  位置索引: {idx2}")
        self.appendOutput(f"  比较次数: {comp2}\n")
        
        if val1 == val2:
            self.appendOutput(f"✓ 两种方法结果一致: {val1}")
        else:
            self.appendOutput(f"⚠ 警告: 两种方法结果不一致！")
        
        self.appendOutput("")


def main():
    root = Tk()
    app = SearchGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

