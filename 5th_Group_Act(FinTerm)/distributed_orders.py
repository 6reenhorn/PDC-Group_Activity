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


# ============================================================
#  PART 4 — ESPINA
#  Master: Order Distribution and Result Collection
#  Covers: round-robin bucketing, comm.send() dispatch,
#          Iprobe() result collection loop, timeout handling
# ============================================================

        # Distribute orders round-robin
        buckets = [[] for _ in range(num_workers)]
        for i, order in enumerate(orders):
            buckets[i % num_workers].append(order)

        dispatch_start = time.perf_counter()
        for worker_id in range(num_workers):
            dest = worker_id + 1
            payload = buckets[worker_id]
            comm.send(payload, dest=dest, tag=10)
            print(
                f"  [Master] Sent {len(payload)} order(s) -> Worker-{dest}: "
                + ", ".join(o["order_id"] for o in payload),
                flush=True,
            )
            dispatch_time = time.perf_counter() - dispatch_start

        print("\n" + "-"*55)
        print("  [Master] Waiting for all workers to finish ...")
        print("-"*55 + "\n")

        # Collect results back from each worker via MPI with timeout protection
        all_results = []
        pending_workers = set(range(1, num_workers + 1))
        recv_start = time.perf_counter()

        while pending_workers:
            received_any = False
            for worker_rank in list(pending_workers):
                if comm.Iprobe(source=worker_rank, tag=20):
                    worker_results = comm.recv(source=worker_rank, tag=20)
                    all_results.extend(worker_results)
                    pending_workers.remove(worker_rank)
                    received_any = True

            if pending_workers and (time.perf_counter() - recv_start) > args.recv_timeout:
                print(
                    f"  [Master] Timeout reached ({args.recv_timeout:.1f}s). "
                    f"Missing workers: {sorted(pending_workers)}",
                    flush=True,
                )
                for worker_rank in sorted(pending_workers):
                    for order in buckets[worker_rank - 1]:
                        all_results.append({
                            **order,
                            "status": "TIMEOUT",
                            "worker_rank": worker_rank,
                            "processed_by": f"Worker-{worker_rank}",
                            "processing_time_s": 0.0,
                            "error": "Worker result not received before timeout",
                        })
                break

            if not received_any:
                time.sleep(0.05)

# ============================================================
#  PART 5 — ANINO
#  Master: Final Results Display + Worker Process Logic
#  Covers: final results printing, runtime summary,
#          print_worker_summary() call, and full worker (else) block
# ============================================================

        total_runtime = time.perf_counter() - run_start

        # Display final results
        print("\n" + "="*55)
        print("  FINAL RESULTS  (collected from all workers)")
        print("="*55)
        for entry in sorted(all_results, key=lambda x: x["order_id"]):
            if entry.get("status") == "COMPLETED":
                print(
                    f"  {entry['order_id']}  {entry['item']:<22}"
                    f"  {entry['status']:<9} by {entry['processed_by']}"
                    f"  ({entry['processing_time_s']}s)"
                )
            else:
                print(
                    f"  {entry['order_id']}  {entry['item']:<22}"
                    f"  {entry.get('status', 'FAILED'):<9} by {entry['processed_by']}"
                    f"  (reason: {entry.get('error', 'unknown')})"
                )
        print("-"*55)
        completed_total = sum(1 for r in all_results if r.get("status") == "COMPLETED")
        failed_total = len(all_results) - completed_total
        print(f"  Total completed: {completed_total} / {num_orders}")
        print(f"  Total failed/timeout: {failed_total}")
        print(f"  Dispatch time: {dispatch_time:.2f}s")
        print(f"  Collection window: {time.perf_counter() - recv_start:.2f}s")
        print(f"  Total runtime: {total_runtime:.2f}s")
        print("="*55 + "\n")

        print_worker_summary(all_results, buckets)

    # ── WORKERS ─────────────────────────────────────
    else:
        # Receive assigned orders from master
        my_orders = comm.recv(source=0, tag=10)
        print(
            f"  [Worker-{rank}] Received {len(my_orders)} order(s): "
            + ", ".join(o["order_id"] for o in my_orders),
            flush=True,
        )

        # Process assigned orders using multiprocessing + synchronized shared state
        result_queue = mp.Queue()
        lock = mp.Lock()
        completed_counter = mp.Value('i', 0)

        workers = []
        for order in my_orders:
            p = mp.Process(
                target=process_order_mp,
                args=(order, rank, result_queue, lock, completed_counter, args.min_delay, args.max_delay),
            )
            p.start()
            workers.append(p)

        for p in workers:
            p.join()

        completed = []
        while True:
            try:
                completed.append(result_queue.get_nowait())
            except queue.Empty:
                break

        if len(completed) < len(my_orders):
            done_order_ids = {entry["order_id"] for entry in completed}
            for missing_order in my_orders:
                if missing_order["order_id"] not in done_order_ids:
                    completed.append({
                        **missing_order,
                        "status": "FAILED",
                        "worker_rank": rank,
                        "processed_by": f"Worker-{rank}",
                        "processing_time_s": 0.0,
                        "error": "Child process exited before publishing result",
                    })

        print(
            f"  [Worker-{rank}] Multiprocessing completed: "
            f"{completed_counter.value} order(s) recorded via shared counter",
            flush=True,
        )

        # Send all completed results back to master
        comm.send(completed, dest=0, tag=20)


if __name__ == '__main__':
    main()
