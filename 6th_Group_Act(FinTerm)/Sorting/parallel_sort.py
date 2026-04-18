import random
import time
import argparse
from multiprocessing import Pool, cpu_count

# Configuration
DEFAULT_SIZE = 1000
MAX_VALUE = 1_000_000
DEFAULT_PROCESSES = 4
STANDARD_SIZES = [
    ("Small", 1_000),
    ("Medium", 100_000),
    ("Large", 1_000_000),
]


def format_preview(arr, preview_count=10):
    """Return a compact preview with first/last values."""
    if len(arr) <= preview_count * 2:
        return str(arr)
    head = arr[:preview_count]
    tail = arr[-preview_count:]
    return f"first {preview_count}: {head} ... last {preview_count}: {tail}"


def is_non_decreasing(arr):
    """Return True if the array is sorted in non-decreasing order."""
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

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

def merge_sorted_chunks(sorted_chunks):
    """
    Iteratively merge a list of sorted arrays into one sorted array.
    Works for any number of chunks (not just powers of two).
    """
    while len(sorted_chunks) > 1:
        merged = []
        # Pair up adjacent chunks and merge them
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged.append(merge(sorted_chunks[i], sorted_chunks[i + 1]))
            else:
                merged.append(sorted_chunks[i])
        sorted_chunks = merged
    return sorted_chunks[0]

def parallel_merge_sort(arr, num_processes=None):
    """
    1. Partition  – split arr into equal-sized chunks
    2. Sort       – each chunk is sorted by a separate worker process
    3. Merge      – sorted chunks are combined into one globally sorted list
    """
    if num_processes is None:
        num_processes = DEFAULT_PROCESSES

    chunk_size = max(1, len(arr) // num_processes)
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    print(f"  Partitioned into {len(chunks)} chunks "
          f"(chunk_size ≈ {chunk_size}, processes used: {min(num_processes, len(chunks))})")

    with Pool(processes=min(num_processes, len(chunks))) as pool:
        sorted_chunks = pool.map(merge_sort, chunks)   # each chunk → its own process

    result = merge_sorted_chunks(sorted_chunks)
    return result

# Helpers

def verify(original, sorted_result, label):
    """Check correctness: result must equal Python's built-in sort."""
    expected = sorted(original)
    ok = sorted_result == expected
    status = "CORRECT" if ok else "MISMATCH"
    print(f"  Verification [{label}]: {status}")
    return ok


def run_sequential_dataset(label, dataset, show_output):
    print(f"\n{'-'*50}")
    print(f"Dataset : {label}  ({len(dataset)} elements)")
    start = time.perf_counter()
    result = merge_sort(dataset)
    elapsed = time.perf_counter() - start
    ok = is_non_decreasing(result)
    print(f"  Sequential time : {elapsed*1000:.3f} ms")
    print(f"  Sequential check: {'CORRECT' if ok else 'MISMATCH'}")
    if show_output:
        print(f"  Sequential output: {result}")
    else:
        print(f"  Sequential preview: {format_preview(result)}")
    return elapsed * 1000, ok, result[0], result[-1]


def run_dataset(label, dataset, num_processes, show_output):
    print(f"\n{'-'*50}")
    print(f"Dataset : {label}  ({len(dataset)} elements)")
    start = time.perf_counter()
    result = parallel_merge_sort(dataset, num_processes=num_processes)
    elapsed = time.perf_counter() - start
    ok = verify(dataset, result, label)
    print(f"  Time   : {elapsed*1000:.3f} ms")
    if show_output:
        print(f"  Output : {result}")
    else:
        print(f"  Preview: {format_preview(result)}")
    return (label, len(dataset), elapsed * 1000, ok, result[0], result[-1])


def run_comparison(label, dataset, num_processes, show_output):
    print(f"\n{'='*50}")
    print(f"Dataset : {label}  ({len(dataset)} elements)")

    seq_start = time.perf_counter()
    seq_result = merge_sort(dataset)
    seq_elapsed = time.perf_counter() - seq_start
    seq_ok = is_non_decreasing(seq_result)

    par_start = time.perf_counter()
    par_result = parallel_merge_sort(dataset, num_processes=num_processes)
    par_elapsed = time.perf_counter() - par_start
    par_ok = verify(dataset, par_result, f"{label} (parallel)")

    speedup = seq_elapsed / par_elapsed if par_elapsed > 0 else float("inf")

    print(f"  Sequential time : {seq_elapsed*1000:.3f} ms")
    print(f"  Sequential check: {'CORRECT' if seq_ok else 'MISMATCH'}")
    print(f"  Parallel time   : {par_elapsed*1000:.3f} ms")
    print(f"  Parallel check  : {'CORRECT' if par_ok else 'MISMATCH'}")
    print(f"  Speedup         : {speedup:.2f}x")

    if show_output:
        print(f"  Sequential output: {seq_result}")
        print(f"  Parallel output  : {par_result}")
    else:
        print(f"  Sequential preview: {format_preview(seq_result)}")
        print(f"  Parallel preview  : {format_preview(par_result)}")

    return (label, len(dataset), seq_elapsed * 1000, par_elapsed * 1000, speedup, seq_ok and par_ok)

# Main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parallel Merge Sort Benchmark")
    parser.add_argument(
        "--size", 
        type=int, 
        default=DEFAULT_SIZE,
        help=f"Dataset size (default: {DEFAULT_SIZE})"
    )
    parser.add_argument(
        "--processes",
        type=int,
        default=DEFAULT_PROCESSES,
        help=f"Number of processes (default: {DEFAULT_PROCESSES})"
    )
    parser.add_argument(
        "--show-output",
        action="store_true",
        help="Print full sorted output"
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare sequential and parallel merge sort side by side"
    )
    parser.add_argument(
        "--all-sizes",
        action="store_true",
        help="Run the selected mode for small, medium, and large datasets"
    )
    args = parser.parse_args()

    if args.all_sizes:
        selected_sizes = STANDARD_SIZES
    else:
        selected_sizes = [(f"Custom ({args.size:,})", args.size)]

    if not args.compare and not args.all_sizes and args.size == DEFAULT_SIZE:
        selected_sizes = [("Default", DEFAULT_SIZE)]

    comparison_summary = []
    parallel_summary = []

    if args.compare:
        print("="*60)
        print("   SORTING COMPARISON  (sequential vs parallel)")
        print(f"   CPU cores available: {cpu_count()}")
        print(f"   Processes to use: {args.processes}")
        print("="*60)

        for label, size in selected_sizes:
            data, already_sorted, reverse_sorted = generate_datasets(size)
            comparison_summary.append(run_comparison(f"{label} - Random Data", data, args.processes, args.show_output))
            comparison_summary.append(run_comparison(f"{label} - Already Sorted Data", already_sorted, args.processes, args.show_output))
            comparison_summary.append(run_comparison(f"{label} - Reverse Sorted Data", reverse_sorted, args.processes, args.show_output))

        print("\n" + "=" * 90)
        print("  COMPARISON SUMMARY")
        print(f"  {'Dataset':<24} {'N':>10} {'Seq (ms)':>12} {'Par (ms)':>12} {'Speedup':>10} {'Status':>10}")
        print(f"  {'-'*24} {'-'*10} {'-'*12} {'-'*12} {'-'*10} {'-'*10}")
        for label, n, seq_ms, par_ms, speedup, ok in comparison_summary:
            print(f"  {label:<24} {n:>10,} {seq_ms:>12.3f} {par_ms:>12.3f} {speedup:>10.2f} {('OK' if ok else 'FAIL'):>10}")
        print("=" * 90)
    else:
        data, already_sorted, reverse_sorted = generate_datasets(args.size)
        
        parallel_summary.append(run_dataset("Random Data", data, args.processes, args.show_output))
        parallel_summary.append(run_dataset("Already Sorted Data", already_sorted, args.processes, args.show_output))
        parallel_summary.append(run_dataset("Reverse Sorted Data", reverse_sorted, args.processes, args.show_output))
        
        print("\n" + "=" * 78)
        print("  SUMMARY")
        print(f"  {'Dataset':<22} {'N':>10} {'Time (ms)':>12} {'Status':>10} {'Min':>10} {'Max':>10}")
        print(f"  {'-'*22} {'-'*10} {'-'*12} {'-'*10} {'-'*10} {'-'*10}")
        for label, n, time_ms, ok, min_val, max_val in parallel_summary:
            print(f"  {label:<22} {n:>10,} {time_ms:>12.3f} {('OK' if ok else 'FAIL'):>10} {min_val:>10} {max_val:>10}")
        print("=" * 78)
    
        print("\nAll datasets sorted and verified successfully.")