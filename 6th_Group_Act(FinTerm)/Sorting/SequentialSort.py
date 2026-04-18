import random

#Hello, if you want to change the amount of dataset, just change the range
data = [random.randint(1, 1000000) for _ in range(1000)]
already_sorted = sorted(data)
reverse_sorted = sorted(data, reverse=True)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
 
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
 
 
def merge(left, right):
    result = []
    a = b = 0
 
    while a < len(left) and b < len(right):
        if left[a] <= right[b]:
            result.append(left[a])
            a += 1
        else:
            result.append(right[b])
            b += 1
 
    result.extend(left[a:])
    result.extend(right[b:])
    return result

if __name__ == "__main__":

    print("Random Data")
    result1 = merge_sort(data)
    print("Sorted: ", result1[:1000])

    print("\nAlready Sorted Data")
    result2 = merge_sort(already_sorted)
    print("Sorted :", result2[:1000])

    print("\nReverse Sorted Data")
    result3 = merge_sort(reverse_sorted)
    print("Sorted :", result3[:1000])