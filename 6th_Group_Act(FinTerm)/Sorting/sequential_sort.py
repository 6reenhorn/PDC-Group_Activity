import random
import argparse
import time

# Configuration
DEFAULT_SIZE = 1000
MAX_VALUE = 1_000_000

def generate_datasets(size):
    """Generate random, sorted, and reverse-sorted datasets."""
    data = [random.randint(1, MAX_VALUE) for _ in range(size)]
    already_sorted = sorted(data)
    reverse_sorted = sorted(data, reverse=True)
    return data, already_sorted, reverse_sorted

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
    parser = argparse.ArgumentParser(description="Sequential Merge Sort Benchmark")
    parser.add_argument(
        "--size", 
        type=int, 
        default=DEFAULT_SIZE,
        help=f"Dataset size (default: {DEFAULT_SIZE})"
    )
    parser.add_argument(
        "--show-output",
        action="store_true",
        help="Print full sorted output (only first 1000 elements by default)"
    )
    args = parser.parse_args()
    
    data, already_sorted, reverse_sorted = generate_datasets(args.size)
    output_limit = args.size if args.show_output else min(1000, args.size)

    print(f"\n{'='*60}")
    print(f"  SEQUENTIAL MERGE SORT  (Size: {args.size:,})")
    print(f"{'='*60}\n")
    
    datasets = [
        ("Random Data", data),
        ("Already Sorted Data", already_sorted),
        ("Reverse Sorted Data", reverse_sorted)
    ]
    
    for label, dataset in datasets:
        print(f"{label}")
        start = time.perf_counter()
        result = merge_sort(dataset)
        elapsed = time.perf_counter() - start
        print(f"  Time: {elapsed*1000:.3f} ms")
        print(f"  Output (first {output_limit}): {result[:output_limit]}\n")