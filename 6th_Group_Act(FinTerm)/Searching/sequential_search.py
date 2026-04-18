import time
import random
import argparse

# Configuration
DEFAULT_SIZE = 1000
MAX_VALUE = 1_000_000

def sequential_linear_search(data: list, target: int) -> int:
    for index, value in enumerate(data):
        if value == target:
            return index
    return -1

# Dataset helpers 
def make_random(n: int) -> list:
    return [random.randint(1, MAX_VALUE) for _ in range(n)]

def make_sorted(n: int) -> list:
    return sorted([random.randint(1, MAX_VALUE) for _ in range(n)])

def make_reverse(n: int) -> list:
    return sorted([random.randint(1, MAX_VALUE) for _ in range(n)], reverse=True)


# Benchmark 
def benchmark(label: str, data: list, target: int):
    start = time.time()
    idx = sequential_linear_search(data, target)
    elapsed = time.time() - start
    found_str = f"index {idx}" if idx != -1 else "NOT FOUND"
    print(f"[SEQ SEARCH] {label:40s} target={target:<8d} → {found_str:>14s}  ({elapsed:.4f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sequential Linear Search Benchmark")
    parser.add_argument(
        "--size",
        type=int,
        default=DEFAULT_SIZE,
        help=f"Dataset size (default: {DEFAULT_SIZE}). Use -1 for all standard sizes."
    )
    parser.add_argument(
        "--all-sizes",
        action="store_true",
        help="Run benchmarks for all standard sizes (1K, 100K, 1M)"
    )
    args = parser.parse_args()
    
    print("=" * 80)
    print("  SEQUENTIAL LINEAR SEARCH — BENCHMARK")
    print("=" * 80)

    if args.all_sizes or args.size == -1:
        sizes = [
            ("Small  (1 000)",      1_000),
            ("Medium (100 000)",   100_000),
            ("Large  (1 000 000)", 1_000_000),
        ]
    else:
        sizes = [(f"Custom ({args.size:,})", args.size)]

    for label, n in sizes:
        data = make_random(n)

        # Case 1: target exists somewhere in the list
        target_present = data[n // 2]
        benchmark(f"{label} — target present",  data, target_present)

        # Case 2: target is very unlikely to exist
        benchmark(f"{label} — target absent",   data, -1)

        # Special case: already sorted
        sorted_data = make_sorted(n)
        benchmark(f"{label} — sorted, worst case", sorted_data, 99_999_999)

        # Special case: reverse sorted
        rev_data = make_reverse(n)
        benchmark(f"{label} — reverse, best case", rev_data, rev_data[0])  
        print()