import random
import time
import os
import argparse
from multiprocessing import Process, Queue

# Configuration
DEFAULT_SIZE = 1000
MAX_VALUE = 1_000_000
DEFAULT_PROCESSES = 4


def generate_dataset(n, mode="random"):
    """Generate dataset with specified mode and size."""
    base = [random.randint(1, MAX_VALUE) for _ in range(n)]
    if mode == "random":
        return base
    elif mode == "sorted":
        return sorted(base)
    elif mode == "reverse":
        return sorted(base, reverse=True)
    return base


def sequential_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


def worker(sub_data, target, q, offset):
    for local_index in range(len(sub_data)):
        if sub_data[local_index] == target:
            q.put(offset + local_index)
            return
    q.put(-1)


def parallel_search(data, target, num_processes=DEFAULT_PROCESSES):
    """Search using multiple processes."""
    chunk_size = len(data) // num_processes
    q = Queue()
    processes = []

    for i in range(num_processes):
        offset = i * chunk_size
        sub_data = data[offset:] if i == num_processes - 1 else data[offset:offset + chunk_size]
        p = Process(target=worker, args=(sub_data, target, q, offset))
        p.start()
        processes.append(p)

    results = [q.get() for _ in processes]
    for p in processes:
        p.join()

    found = [idx for idx in results if idx != -1]
    return min(found) if found else -1


def run_one(label, func, data, target):
    start = time.time()
    result = func(data, target)
    end = time.time()
    print(f"    {label:<26} index={result:<8}  time={end - start:.6f}s")
    return result, end - start


def run_correctness_tests():
    print("=" * 62)
    print("  CORRECTNESS TESTS")
    print("=" * 62)

    cases = [
        ("Target at beginning",    [7, 1, 2, 3, 4],   7,   0),
        ("Target at end",          [1, 2, 3, 4, 7],   7,   4),
        ("Target in middle",       [1, 2, 7, 4, 5],   7,   2),
        ("Target not found",       [1, 2, 3, 4, 5],   9,  -1),
        ("Single element (found)", [42],              42,   0),
        ("Single element (miss)",  [42],              99,  -1),
        ("First occurrence kept",  [3, 7, 1, 7, 5],   7,   1),
        ("Across chunk boundary",  list(range(20)),   13,  13),
    ]

    all_pass = True
    for desc, data, target, expected in cases:
        seq = sequential_search(data, target)
        par = parallel_search(data, target)
        ok = seq == expected and par == expected
        status = "PASS" if ok else "FAIL"
        if not ok:
            all_pass = False
        print(f"  [{status}] {desc:<28}  seq={seq:<5} par={par:<5} expected={expected}")

    print()
    return all_pass


def run_benchmark(test_sizes=None, num_processes=DEFAULT_PROCESSES):
    """Run benchmark for specified sizes."""
    if test_sizes is None:
        test_sizes = [("Small", 1_000), ("Medium", 100_000), ("Large", 1_000_000)]
    
    print("=" * 62)
    print("  WORKLOAD BENCHMARK")
    print(f"  System CPU count: {os.cpu_count()}  |  Parallel processes: {num_processes}")
    print("=" * 62)

    summary = []

    for label, n in test_sizes:
        print(f"\n  [{label} Dataset -- {n:,} elements]  mode=random")
        print(f"  {'-' * 56}")
        data = generate_dataset(n, mode="random")
        target = data[n // 2]
        _, seq_time = run_one("Sequential", sequential_search, data, target)
        _, par_time = run_one(f"Parallel ({num_processes} proc)", lambda d, t: parallel_search(d, t, num_processes), data, target)
        speedup = seq_time / par_time if par_time > 0 else float("inf")
        note = "Parallel faster" if speedup > 1.05 else "Parallel slower (overhead)"
        print(f"    Speedup: {speedup:.2f}x  -> {note}")
        summary.append((label, n, seq_time, par_time, speedup))

    print(f"\n\n  [Special Case 1 -- Already Sorted Data]")
    print(f"  {'-' * 56}")
    for label, n in test_sizes:
        print(f"\n    {label} ({n:,})")
        data = generate_dataset(n, mode="sorted")
        target = data[n // 2]
        run_one("  Sequential", sequential_search, data, target)
        run_one("  Parallel", lambda d, t: parallel_search(d, t, num_processes), data, target)

    print(f"\n\n  [Special Case 2 -- Reverse Sorted Data]")
    print(f"  {'-' * 56}")
    for label, n in test_sizes:
        print(f"\n    {label} ({n:,})")
        data = generate_dataset(n, mode="reverse")
        target = data[n // 2]
        run_one("  Sequential", sequential_search, data, target)
        run_one("  Parallel", lambda d, t: parallel_search(d, t, num_processes), data, target)

    print(f"\n\n  [Special Case 3 -- Target Not Found (full scan)]")
    print(f"  {'-' * 56}")
    for label, n in test_sizes:
        print(f"\n    {label} ({n:,})  target=0 (never in dataset)")
        data = generate_dataset(n, mode="random")
        run_one("  Sequential", sequential_search, data, 0)
        run_one("  Parallel", lambda d, t: parallel_search(d, t, num_processes), data, 0)

    print(f"\n\n{'=' * 62}")
    print("  SUMMARY -- Random Dataset")
    print(f"  {'Size':<8} {'N':>10}  {'Seq (s)':>10}  {'Par (s)':>10}  {'Speedup':>8}")
    print(f"  {'-'*8} {'-'*10}  {'-'*10}  {'-'*10}  {'-'*8}")
    for lbl, n, s, p, sp in summary:
        print(f"  {lbl:<8} {n:>10,}  {s:>10.6f}  {p:>10.6f}  {sp:>7.2f}x")
    print("=" * 62)


def main():
    parser = argparse.ArgumentParser(description="Parallel Linear Search Benchmark")
    parser.add_argument(
        "--size",
        type=int,
        default=None,
        help="Single dataset size to test (runs correctness tests + benchmark for that size)"
    )
    parser.add_argument(
        "--all-sizes",
        action="store_true",
        help="Run benchmarks for all standard sizes (1K, 100K, 1M)"
    )
    parser.add_argument(
        "--processes",
        type=int,
        default=DEFAULT_PROCESSES,
        help=f"Number of processes (default: {DEFAULT_PROCESSES})"
    )
    parser.add_argument(
        "--skip-correctness",
        action="store_true",
        help="Skip correctness tests and run only benchmarks"
    )
    args = parser.parse_args()
    
    print()
    print("  LINEAR SEARCH  --  Sequential vs Parallel")
    print()

    if not args.skip_correctness:
        passed = run_correctness_tests()
        if not passed:
            print("  Some correctness tests FAILED.\n")
            return
        print("  All correctness tests PASSED.\n")
    
    # Determine which sizes to benchmark
    if args.size is not None:
        test_sizes = [(f"Custom", args.size)]
    elif args.all_sizes:
        test_sizes = [("Small", 1_000), ("Medium", 100_000), ("Large", 1_000_000)]
    else:
        test_sizes = [("Small", 1_000), ("Medium", 100_000), ("Large", 1_000_000)]
    
    run_benchmark(test_sizes, args.processes)
    print()


if __name__ == "__main__":
    main()