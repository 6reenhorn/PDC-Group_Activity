import random
import argparse
import time

# Configuration
DEFAULT_SIZE = 1000
MAX_VALUE = 1_000_000


def is_non_decreasing(arr):
    """Return True if the array is sorted in non-decreasing order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def format_preview(arr, preview_count=10):
    """Return a compact preview with first/last values."""
    if len(arr) <= preview_count * 2:
        return str(arr)
    head = arr[:preview_count]
    tail = arr[-preview_count:]
    return f"first {preview_count}: {head} ... last {preview_count}: {tail}"

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
    print(f"\n{'='*60}")
    print(f"  SEQUENTIAL MERGE SORT  (Size: {args.size:,})")
    print(f"{'='*60}\n")
    
    datasets = [
        ("Random Data", data),
        ("Already Sorted Data", already_sorted),
        ("Reverse Sorted Data", reverse_sorted)
    ]

    summary = []
    
    for label, dataset in datasets:
        print(f"{label}")
        start = time.perf_counter()
        result = merge_sort(dataset)
        elapsed = time.perf_counter() - start
        ok = is_non_decreasing(result)
        summary.append((label, len(dataset), elapsed * 1000, ok, result[0], result[-1]))
        print(f"  Time: {elapsed*1000:.3f} ms")
        print(f"  Check: {'CORRECT' if ok else 'MISMATCH'}")
        if args.show_output:
            print(f"  Output: {result}\n")
        else:
            print(f"  Preview: {format_preview(result)}\n")

    print("=" * 78)
    print("  SUMMARY")
    print(f"  {'Dataset':<22} {'N':>10} {'Time (ms)':>12} {'Status':>10} {'Min':>10} {'Max':>10}")
    print(f"  {'-'*22} {'-'*10} {'-'*12} {'-'*10} {'-'*10} {'-'*10}")
    for label, n, time_ms, ok, min_val, max_val in summary:
        print(f"  {label:<22} {n:>10,} {time_ms:>12.3f} {('OK' if ok else 'FAIL'):>10} {min_val:>10} {max_val:>10}")
    print("=" * 78)