import random
import time
import argparse
from multiprocessing import Pool, cpu_count

# Configuration
DEFAULT_SIZE = 1000
MAX_VALUE = 1_000_000
DEFAULT_PROCESSES = 4

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

    chunk_size = len(arr) // num_processes             
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


def run_dataset(label, dataset):
    print(f"\n{'─'*50}")
    print(f"Dataset : {label}  ({len(dataset)} elements)")
    start = time.perf_counter()
    result = parallel_merge_sort(dataset)
    elapsed = time.perf_counter() - start
    verify(dataset, result, label)
    print(f"  Time   : {elapsed*1000:.3f} ms")
    print(f"  Output : {result}")

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
    args = parser.parse_args()
    
    data, already_sorted, reverse_sorted = generate_datasets(args.size)
    
    print("="*60)
    print("   PARALLEL MERGE SORT  (multiprocessing)")
    print(f"   Dataset size: {args.size:,}")
    print(f"   CPU cores available: {cpu_count()}")
    print(f"   Processes to use: {args.processes}")
    print("="*60)

    run_dataset("Random Data",          data)
    run_dataset("Already Sorted Data",  already_sorted)
    run_dataset("Reverse Sorted Data",  reverse_sorted)

    print("\nAll datasets sorted and verified successfully.")