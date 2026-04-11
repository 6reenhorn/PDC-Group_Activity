Provide written answers to the following questions:

### 1. How did you distribute orders among worker processes?
The master process (rank 0) is the sole authority for generating and distributing
orders. It uses a **round-robin algorithm** to divide orders as evenly as possible
across all available workers. Each order at index `i` is placed into the bucket for
worker `i % num_workers`, cycling through workers in sequence.

```python
buckets = [[] for _ in range(num_workers)]
for i, order in enumerate(orders):
    buckets[i % num_workers].append(order)
```

Once bucketing is done, the master sends each worker's bucket using MPI
point-to-point messaging (`comm.send`) with a tag of `10` to identify the message
type. Workers block on `comm.recv` until their payload arrives, then immediately
begin processing. This design keeps the master in full control of load distribution
while workers remain stateless and interchangeable.

---

### 2. What happens if there are more orders than workers?
Round-robin handles overflow automatically — extra orders simply wrap around and
stack onto workers that already have assignments. For example, with **7 orders**
and **3 workers**:

| Worker | Orders Assigned          | Count |
|--------|--------------------------|-------|
| Worker-1 | ORD-1000, ORD-1003, ORD-1006 | 3 |
| Worker-2 | ORD-1001, ORD-1004           | 2 |
| Worker-3 | ORD-1002, ORD-1005           | 2 |

No orders are dropped or lost. Workers with heavier buckets simply take longer to
finish because they process their orders sequentially within their MPI rank. In this
system, each MPI worker also spawns one `mp.Process` child per order, so multiple
orders within the same worker are processed **in parallel**, which significantly
reduces the impact of uneven bucket sizes. The worker with 3 orders does not
necessarily finish last — its three child processes all run concurrently.

---

### 3. How did processing delays affect the order completion?
Each order's processing time is drawn from `random.uniform(min_delay, max_delay)`
— by default between **0.3 and 1.5 seconds**. Because workers process their orders
in parallel child processes, and each child sleeps for a different random duration,
the **completion order is entirely non-deterministic** and almost never matches
the original submission order.

This is visible in the output: an order sent last may complete first, and the slowest
order becomes the bottleneck for its worker. The master uses a non-blocking
`comm.Iprobe()` polling loop to collect results as workers finish, rather than
waiting on them one by one in a fixed order. This means fast workers are
acknowledged immediately without the master stalling on a slow one. A configurable
`--recv-timeout` flag also protects the master from hanging indefinitely if a worker
crashes or never responds.

---

### 4. How did you implement shared memory, and where was it initialized?
Shared memory is implemented at the **worker level** using three components from
Python's `multiprocessing` module, all initialized inside the worker's MPI block
(rank > 0) before spawning child processes:

```python
result_queue = mp.Queue()          # collects completed order results
lock = mp.Lock()                   # mutual exclusion for counter writes
completed_counter = mp.Value('i', 0)  # shared integer across child processes
```

- `mp.Queue()` is a process-safe FIFO queue. Each child process calls
  `result_queue.put(result)` after finishing an order. The parent worker then
  drains the queue after all children have joined.

- `mp.Value('i', 0)` is a shared memory integer backed by a C-type. Every child
  process increments this counter after completing its order, giving a real-time
  count of how many orders have been processed so far.

- `mp.Lock()` guards the counter increment to prevent race conditions.

These are initialized **per MPI worker**, not globally, because each MPI process is
an independent OS process with its own memory space. Shared memory only needs
to exist within the scope of a single worker's child processes.

---

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?

---

### 6. How did you ensure consistent results when using multiple processes?

---
