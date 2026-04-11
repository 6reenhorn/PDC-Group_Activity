r"""
Distributed Order Processing System
Uses mpi4py for inter-process communication and multiprocessing
for shared memory and synchronization.


First you need to: cd "5th_Group_Act(FinTerm)" directory, then run the following command in terminal:

Quick Setup:
Baseline deterministic run

    & "C:\Program Files\Microsoft MPI\Bin\mpiexec.exe" -n 4 python distributed_orders.py --orders 7 --seed 42 --recv-timeout 20

Higher workload

    & "C:\Program Files\Microsoft MPI\Bin\mpiexec.exe" -n 4 python distributed_orders.py --orders 30 --seed 42 --recv-timeout 30

Stress timing variation

    & "C:\Program Files\Microsoft MPI\Bin\mpiexec.exe" -n 4 python distributed_orders.py --orders 30 --seed 42 --min-delay 0.1 --max-delay 2.0 --recv-timeout 40
"""

# ============================================================
#  PART 1 — ANTONIO
#  Imports, Constants, and Order Generation
#  Covers: all imports, ITEMS list, generate_orders(), parse_args()
# ============================================================

import time
import random
import argparse
import queue
import multiprocessing as mp

ITEMS = [
    "Laptop", "Wireless Mouse", "Mechanical Keyboard", "USB-C Hub",
    "Monitor", "Webcam", "Headset", "Desk Lamp", "Chair Mat", "Notebook"
]


def generate_orders(n):
    return [
        {"order_id": f"ORD-{1000 + i}", "item": random.choice(ITEMS)}
        for i in range(n)
    ]


def parse_args():
    parser = argparse.ArgumentParser(description="Distributed Order Processing with MPI + multiprocessing")
    parser.add_argument("--orders", type=int, default=None, help="Number of orders to generate (default: random 5-8)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible runs")
    parser.add_argument("--min-delay", type=float, default=0.3, help="Minimum simulated processing delay in seconds")
    parser.add_argument("--max-delay", type=float, default=1.5, help="Maximum simulated processing delay in seconds")
    parser.add_argument("--recv-timeout", type=float, default=20.0, help="Master receive timeout per run in seconds")
    return parser.parse_args()

# ============================================================
#  PART 2 — FLORES
#  Order Processing Functions
#  Covers: process_order(), process_order_mp()
# ============================================================

def process_order(order, worker_rank, min_delay, max_delay):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    result = {
        **order,
        "status": "COMPLETED",
        "worker_rank": worker_rank,
        "processed_by": f"Worker-{worker_rank}",
        "processing_time_s": round(delay, 2),
    }
    print(
        f"  [Worker-{worker_rank}] Processed {order['order_id']} "
        f"({order['item']}) in {delay:.2f}s",
        flush=True,
    )
    return result


def process_order_mp(order, worker_rank, result_queue, lock, completed_counter, min_delay, max_delay):
    """Child process task: process one order and update shared state safely."""
    try:
        result = process_order(order, worker_rank, min_delay, max_delay)
    except Exception as exc:
        result = {
            **order,
            "status": "FAILED",
            "worker_rank": worker_rank,
            "processed_by": f"Worker-{worker_rank}",
            "processing_time_s": 0.0,
            "error": str(exc),
        }
    result_queue.put(result)
    with lock:
        completed_counter.value += 1

# ============================================================
#  PART 3 — CASIA
#  Worker Summary and MPI Initialization
#  Covers: print_worker_summary(), main() setup up to order generation
# ============================================================

def print_worker_summary(all_results, buckets):
    print("\n" + "="*55)
    print("  WORKER SUMMARY")
    print("="*55)

    num_workers = len(buckets)
    for worker_rank in range(1, num_workers + 1):
        assigned = len(buckets[worker_rank - 1])
        entries = [r for r in all_results if r.get("worker_rank") == worker_rank]
        completed = [r for r in entries if r.get("status") == "COMPLETED"]
        failed = [r for r in entries if r.get("status") != "COMPLETED"]
        avg_time = (
            round(sum(r.get("processing_time_s", 0.0) for r in completed) / len(completed), 2)
            if completed else 0.0
        )
        print(
            f"  Worker-{worker_rank}: assigned={assigned}, completed={len(completed)}, "
            f"failed={len(failed)}, avg_time={avg_time:.2f}s"
        )
    print("="*55)


def main():
    from mpi4py import MPI

    args = parse_args()

    # Initialize MPI only in the main interpreter process.
    # This avoids MPI init side effects when multiprocessing spawns child processes on Windows.
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if args.seed is not None:
        random.seed(args.seed + rank)

    # ── MASTER ──────────────────────────────────────
    if rank == 0:
        if args.orders is not None and args.orders > 0:
            num_orders = args.orders
        else:
            num_orders = random.randint(5, 8)

        if size < 2:
            print("Need at least 2 MPI processes: 1 master + >=1 worker.")
            return

        run_start = time.perf_counter()
        orders = generate_orders(num_orders)
        num_workers = size - 1

        print("\n" + "="*55)
        print(f"  MASTER  |  {num_orders} orders  |  {num_workers} worker(s)")
        print("="*55)
        for o in orders:
            print(f"  Generated: {o['order_id']} -> {o['item']}")
        print("-"*55 + "\n")