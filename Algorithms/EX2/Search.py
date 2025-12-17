import random

def generate_random_array(n):
    """生成包含n个不重复整数的随机数组"""
    if n <= 0:
        return None
    return random.sample(range(-10**6, 10**6), n)

def input_array():
    """手动输入数组，确保元素不重复"""
    while True:
        s = input("请输入整数数组（元素用逗号分隔，互不相同）：")
        try:
            arr = list(map(int, s.split(',')))
            if len(arr) == len(set(arr)):
                return arr
            print("元素存在重复，请重新输入！")
        except ValueError:
            print("输入格式错误，请使用逗号分隔整数（例如：1,3,5）！")

def check_sorted(arr):
    """判断数组排序状态：0-未排序，1-升序，2-降序，3-先升后降，4-先降后升"""
    if len(arr) <= 1:
        return 1  # 长度为0或1视为升序
    
    # 检查升序
    is_asc = all(arr[i] < arr[i+1] for i in range(len(arr)-1))
    if is_asc:
        return 1
    
    # 检查降序
    is_desc = all(arr[i] > arr[i+1] for i in range(len(arr)-1))
    if is_desc:
        return 2
    
    # 检查先升后降
    peak = -1
    for i in range(1, len(arr)-1):
        if arr[i-1] < arr[i] and arr[i] > arr[i+1]:
            peak = i
            break
    if peak != -1:
        left_ok = all(arr[i] < arr[i+1] for i in range(peak))
        right_ok = all(arr[i] > arr[i+1] for i in range(peak, len(arr)-1))
        if left_ok and right_ok:
            return 3
    
    # 检查先降后升
    valley = -1
    for i in range(1, len(arr)-1):
        if arr[i-1] > arr[i] and arr[i] < arr[i+1]:
            valley = i
            break
    if valley != -1:
        left_ok = all(arr[i] > arr[i+1] for i in range(valley))
        right_ok = all(arr[i] < arr[i+1] for i in range(valley, len(arr)-1))
        if left_ok and right_ok:
            return 4
    
    return 0  # 未排序

def sequential_search(arr, target):
    """顺序检索，返回(位置, 比较次数)，未找到返回(-1, 次数)"""
    count = 0
    for i, num in enumerate(arr):
        count += 1
        if num == target:
            return (i, count)
    return (-1, count)

def binary_search_asc(arr, target):
    """升序数组二分查找"""
    low, high = 0, len(arr)-1
    count = 0
    while low <= high:
        mid = (low + high) // 2
        count += 1
        if arr[mid] == target:
            return (mid, count)
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return (-1, count)

def binary_search_desc(arr, target):
    """降序数组二分查找"""
    low, high = 0, len(arr)-1
    count = 0
    while low <= high:
        mid = (low + high) // 2
        count += 1
        if arr[mid] == target:
            return (mid, count)
        elif arr[mid] < target:
            high = mid - 1
        else:
            low = mid + 1
    return (-1, count)

def ternary_search_asc(arr, target):
    """升序数组三分查找"""
    low, high = 0, len(arr)-1
    count = 0
    while low <= high:
        if high - low < 3:
            for i in range(low, high+1):
                count += 1
                if arr[i] == target:
                    return (i, count)
            return (-1, count)
        
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3
        count += 2
        
        if arr[mid1] == target:
            return (mid1, count)
        if arr[mid2] == target:
            return (mid2, count)
        
        if target < arr[mid1]:
            high = mid1 - 1
        elif target > arr[mid2]:
            low = mid2 + 1
        else:
            low, high = mid1 + 1, mid2 - 1
    return (-1, count)

def ternary_search_desc(arr, target):
    """降序数组三分查找"""
    low, high = 0, len(arr)-1
    count = 0
    while low <= high:
        if high - low < 3:
            for i in range(low, high+1):
                count += 1
                if arr[i] == target:
                    return (i, count)
            return (-1, count)
        
        mid1 = low + (high - low) // 3
        mid2 = high - (high - low) // 3
        count += 2
        
        if arr[mid1] == target:
            return (mid1, count)
        if arr[mid2] == target:
            return (mid2, count)
        
        if target > arr[mid1]:
            high = mid1 - 1
        elif target < arr[mid2]:
            low = mid2 + 1
        else:
            low, high = mid1 + 1, mid2 - 1
    return (-1, count)

def find_closest(arr, target):
    """查找最接近目标值的元素及位置"""
    min_diff = abs(arr[0] - target)
    closest_val, closest_idx = arr[0], 0
    for i, num in enumerate(arr):
        diff = abs(num - target)
        if diff < min_diff:
            min_diff, closest_val, closest_idx = diff, num, i
    return (closest_val, closest_idx)

def find_max_asc_desc(arr):
    """先升后降数组找最大值（二分法）"""
    low, high = 0, len(arr)-1
    count = 0
    while low < high:
        mid = (low + high) // 2
        count += 1
        if arr[mid] < arr[mid+1]:
            low = mid + 1
        else:
            high = mid
    return (low, count)

def find_min_desc_asc(arr):
    """先降后升数组找最小值（二分法）"""
    low, high = 0, len(arr)-1
    count = 0
    while low < high:
        mid = (low + high) // 2
        count += 1
        if arr[mid] > arr[mid+1]:
            low = mid + 1
        else:
            high = mid
    return (low, count)

def kth_smallest_brute(arr, k):
    """蛮力法找第k小元素"""
    arr_copy = arr.copy()
    count = 0
    for i in range(k):
        min_idx = i
        for j in range(i+1, len(arr_copy)):
            count += 1
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
    val = arr_copy[k-1]
    return (val, arr.index(val), count)

def selection_sort_with_count(arr):
    """带比较次数统计的选择排序"""
    arr_copy = arr.copy()
    count = 0
    for i in range(len(arr_copy)):
        min_idx = i
        for j in range(i+1, len(arr_copy)):
            count += 1
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
    return arr_copy, count

def kth_smallest_sorted(arr, k):
    """预排序法找第k小元素"""
    sorted_arr, count = selection_sort_with_count(arr)
    val = sorted_arr[k-1]
    return (val, arr.index(val), count)

def main():
    current_array = None
    status_map = {0: "未排序", 1: "升序", 2: "降序", 3: "先升后降", 4: "先降后升"}
    
    while True:
        print("\n===== 检索算法实验系统 =====")
        print("1. 生成/输入数组")
        print("2. 查看当前数组")
        print("3. 判断数组排序状态")
        print("4. 顺序检索元素")
        print("5. 有序数组多方法查找")
        print("6. 特殊数组查找最值")
        print("7. 无序数组找第k小元素")
        print("8. 退出系统")
        
        choice = input("请选择功能(1-8): ")
        
        if choice == '1':
            while True:
                try:
                    n = int(input("请输入数组长度(正整数): "))
                    if n > 0:
                        break
                    print("长度必须为正整数!")
                except ValueError:
                    print("输入错误，请输入数字!")
            
            gen_choice = input("1-随机生成 2-手动输入: ")
            if gen_choice == '1':
                current_array = generate_random_array(n)
                print(f"已生成{len(current_array)}个不重复元素的数组")
            elif gen_choice == '2':
                current_array = input_array()
                print(f"已输入{len(current_array)}个元素的数组")
            else:
                print("无效选择")
        
        elif choice == '2':
            if current_array:
                print(f"当前数组: {current_array}")
            else:
                print("请先生成/输入数组(选择1)")
        
        elif choice == '3':
            if current_array:
                status = check_sorted(current_array)
                print(f"数组状态: {status_map[status]} (代码: {status})")
            else:
                print("请先生成/输入数组(选择1)")
        
        elif choice == '4':
            if current_array:
                try:
                    target = int(input("请输入检索目标: "))
                    idx, count = sequential_search(current_array, target)
                    if idx != -1:
                        print(f"找到元素! 位置: {idx}, 比较次数: {count}")
                    else:
                        print(f"未找到元素, 比较次数: {count}")
                except ValueError:
                    print("请输入整数!")
            else:
                print("请先生成/输入数组(选择1)")
        
        elif choice == '5':
            if current_array:
                status = check_sorted(current_array)
                if status not in (1, 2):
                    print("仅支持升序或降序数组!")
                    continue
                
                try:
                    target = int(input("请输入检索目标: "))
                    seq_idx, seq_cnt = sequential_search(current_array, target)
                    
                    if status == 1:
                        bin_idx, bin_cnt = binary_search_asc(current_array, target)
                        ter_idx, ter_cnt = ternary_search_asc(current_array, target)
                    else:
                        bin_idx, bin_cnt = binary_search_desc(current_array, target)
                        ter_idx, ter_cnt = ternary_search_desc(current_array, target)
                    
                    print("\n查找结果:")
                    print(f"顺序查找: {'找到(位置'+str(seq_idx)+')' if seq_idx!=-1 else '未找到'}, 比较次数: {seq_cnt}")
                    print(f"二分查找: {'找到(位置'+str(bin_idx)+')' if bin_idx!=-1 else '未找到'}, 比较次数: {bin_cnt}")
                    print(f"三分查找: {'找到(位置'+str(ter_idx)+')' if ter_idx!=-1 else '未找到'}, 比较次数: {ter_cnt}")
                    
                    if seq_idx == -1:
                        closest_val, closest_idx = find_closest(current_array, target)
                        print(f"最接近元素: {closest_val} (位置: {closest_idx})")
                except ValueError:
                    print("请输入整数!")
            else:
                print("请先生成/输入数组(选择1)")
        
        elif choice == '6':
            if current_array:
                status = check_sorted(current_array)
                if status == 3:
                    idx, cnt = find_max_asc_desc(current_array)
                    print(f"先升后降数组的最大值: {current_array[idx]} (位置: {idx}), 比较次数: {cnt}")
                elif status == 4:
                    idx, cnt = find_min_desc_asc(current_array)
                    print(f"先降后升数组的最小值: {current_array[idx]} (位置: {idx}), 比较次数: {cnt}")
                else:
                    print("仅支持先升后降或先降后升数组!")
            else:
                print("请先生成/输入数组(选择1)")
        
        elif choice == '7':
            if current_array:
                try:
                    k = int(input(f"请输入k(1-{len(current_array)}): "))
                    if not (1 <= k <= len(current_array)):
                        print(f"k必须在1-{len(current_array)}之间!")
                        continue
                    
                    brute_val, brute_idx, brute_cnt = kth_smallest_brute(current_array, k)
                    sort_val, sort_idx, sort_cnt = kth_smallest_sorted(current_array, k)
                    
                    print("\n查找结果:")
                    print(f"蛮力法: 第{k}小元素为{brute_val} (位置: {brute_idx}), 比较次数: {brute_cnt}")
                    print(f"预排序法: 第{k}小元素为{sort_val} (位置: {sort_idx}), 比较次数: {sort_cnt}")
                except ValueError:
                    print("请输入整数!")
            else:
                print("请先生成/输入数组(选择1)")
        
        elif choice == '8':
            print("感谢使用，再见!")
            break
        
        else:
            print("无效选择，请输入1-8之间的数字!")

if __name__ == "__main__":
    main()