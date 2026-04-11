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

