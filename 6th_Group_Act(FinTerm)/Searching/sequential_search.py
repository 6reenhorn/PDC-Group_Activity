import time
import random

def sequential_linear_search(data: list, target: int) -> int:
    for index, value in enumerate(data):
        if value == target:
            return index
    return -1

# Dataset helpers 
def make_random(n: int) -> list:
    return [random.randint(1, 1_000_000) for _ in range(n)]

def make_sorted(n: int) -> list:
    return list(range(1, n + 1))

def make_reverse(n: int) -> list:
    return list(range(n, 0, -1))


# Benchmark 
def benchmark(label: str, data: list, target: int):
    start = time.time()
    idx = sequential_linear_search(data, target)
    elapsed = time.time() - start
    found_str = f"index {idx}" if idx != -1 else "NOT FOUND"
    print(f"[SEQ SEARCH] {label:40s} target={target:<8d} → {found_str:>14s}  ({elapsed:.4f}s)")


if __name__ == "__main__":
    print("=" * 80)
    print("  SEQUENTIAL LINEAR SEARCH — BENCHMARK")
    print("=" * 80)

    sizes = [
        ("Small  (1 000)",      1_000),
        ("Medium (100 000)",   100_000),
        ("Large  (1 000 000)", 1_000_000),
    ]

    for label, n in sizes:
        data = make_random(n)

        # Case 1: target exists somewhere in the list
        target_present = data[n // 2]
        benchmark(f"{label} — target present",  data, target_present)

        # Case 2: target is very unlikely to exist
        benchmark(f"{label} — target absent",   data, -1)

        # Special case: already sorted
        sorted_data = make_sorted(n)
        benchmark(f"{label} — sorted, worst case", sorted_data, n + 1)

        # Special case: reverse sorted
        rev_data = make_reverse(n)
        benchmark(f"{label} — reverse, best case", rev_data, n)  
        print()