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

No orders are dropped or lost. A worker with more assigned orders has more local
work to manage, but in our implementation each worker spawns one `mp.Process`
child per order, so those assigned orders execute concurrently within that worker.
Because of this, uneven bucket sizes do not always map directly to completion time:
a worker with 3 orders can still finish close to, or even before, a worker with 2
orders depending on random delays and OS scheduling.

---

### 3. How did processing delays affect the order completion?
Each order's processing time is drawn from `random.uniform(min_delay, max_delay)`
— by default between **0.3 and 1.5 seconds**. Because workers process their orders
in parallel child processes, and each child sleeps for a different random duration,
the **completion order can be non-deterministic** and often does not match
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
Process coordination is implemented at the **worker level** using three components from
Python's `multiprocessing` module, all initialized inside the worker's MPI block
(rank > 0) before spawning child processes:

```python
result_queue = mp.Queue()          # collects completed order results
lock = mp.Lock()                   # mutual exclusion for counter writes
completed_counter = mp.Value('i', 0)  # shared integer across child processes
```

- `mp.Queue()` is a process-safe IPC queue (message passing between processes),
  not a shared-memory array/list. Each child process calls
  `result_queue.put(result)` after finishing an order. The parent worker then
  drains the queue after all children have joined.

- `mp.Value('i', 0)` is a shared-memory integer backed by a C-type. Every child
  process increments this counter after completing its order, giving a real-time
  count of how many orders have been processed so far.

- `mp.Lock()` guards the counter increment to prevent race conditions.

These are initialized **per MPI worker**, not globally, because each MPI process is
an independent OS process with its own memory space. The shared-memory part
(`mp.Value` + `mp.Lock`) only exists within one worker and its child processes,
while cross-process result transfer uses `mp.Queue`.

---

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?

In our design, there are two levels of concurrency, and each level has different
write-conflict behavior:

1. **Between MPI workers (rank-to-rank):**
  There is **no direct shared memory conflict** between Worker-1, Worker-2, and
  Worker-3 because each MPI rank is its own OS process with an isolated memory
  space. A variable in one rank is invisible to another rank unless explicitly sent
  through MPI.

2. **Inside one MPI worker (child process-to-child process):**
  Multiple child processes do write concurrently to worker-local shared structures.
  This is where race conditions can occur if synchronization is missing.

The main issue we had to prevent was a **lost update** on the shared completion
counter. Incrementing a shared value is not atomic at the Python logic level
(`read -> add -> write`), so two children finishing at nearly the same time could
overwrite each other and produce an incorrect count.

To prevent this, we wrapped the counter increment with a lock:

```python
with lock:
   completed_counter.value += 1
```

For result collection, we used `mp.Queue()` instead of a plain list because it is
process-safe and designed for concurrent producer writes. Without a safe queue,
simultaneous writes could corrupt state or require additional manual locking.

Another practical issue in highly concurrent runs is **interleaved console output**
(log lines appearing mixed or out of order). This does not corrupt data, but it can
make logs harder to read. We reduced this confusion by ensuring each processed
result is still stored as a complete dictionary in the queue and later consolidated
by the parent worker before sending to the master.

In short, simultaneous writes were safe because we used the right primitives for
each write pattern: `Lock` for the shared counter and `Queue` for concurrent result
publishing.

---

### 6. How did you ensure consistent results when using multiple processes?

The system uses a **layered approach** to guarantee correctness at every level:

**Within each worker — `mp.Lock()` for atomic counter updates:**
```python
with lock:
    completed_counter.value += 1
```
The `with lock:` block ensures only one child process at a time can enter the
critical section. All others block at the lock boundary until it is released. This
makes the increment effectively atomic and eliminates lost updates.

**Within each worker — `p.join()` before reading results:**
```python
for p in workers:
    p.join()
```
The parent worker waits for every child process to fully exit before draining the
result queue. This guarantees that all `result_queue.put()` calls have completed
before any `result_queue.get()` is attempted — no partial reads.

**Across MPI processes — non-blocking `Iprobe()` collection with timeout:**
```python
if comm.Iprobe(source=worker_rank, tag=20):
    worker_results = comm.recv(source=worker_rank, tag=20)
```
The master polls each worker non-blocking rather than doing a blocking `recv` in
fixed order. This prevents one slow worker from stalling the collection of results
from all others. If a worker never responds within `--recv-timeout` seconds, the
master records those orders as `TIMEOUT` and continues — the final list is always
complete even under failure conditions.

**Result integrity — missing order detection in workers:**
If a child process crashes before putting its result in the queue, the worker detects
the gap by comparing received result IDs against the original order list, and inserts
a `FAILED` record so the master always receives exactly as many records as orders
were assigned. Nothing is silently dropped.

Together, these four mechanisms — mutual exclusion, join barriers, non-blocking
collection, and gap detection — ensure the final output is always **complete,
consistent, and accurate** regardless of timing, process speed, or partial failures.

---
