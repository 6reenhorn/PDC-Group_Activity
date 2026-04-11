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

### 3. How did processing delays affect the order completion?

### 4. How did you implement shared memory, and where was it initialized?

### 5. What issues occurred when multiple workers wrote to shared memory simultaneously?

### 6. How did you ensure consistent results when using multiple processes?