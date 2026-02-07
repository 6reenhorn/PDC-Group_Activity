|      Method      |     Execution Order    | GWA Output | Execution Time |
|------------------|------------------------|------------|----------------|
|  Multithreading  | Concurrent/Interleaved |    86.50   |     2.28s      |
|  Multiprocessing |        Parallel        |    86.50   |     2.58s      |

#### Discussion

Your group should answer the following questions in a README.md or separate
file in your repository:

### 1. Which approach demonstrates true parallelism in Python? Explain.
    - The multiprocessing version demonstrates true parallelism in Python because each process runs independently on separate CPU cores without being limited by the GIL(a lock that limits Python threads to one at a time), while multithreading only simulates parallelism through concurrency.

### 2. Compare execution times between multithreading and multiprocessing.
    - The execution times highlight the difference between multithreading and multiprocessing. In multiprocessing, only one process was used, completing in 2.31 seconds, so no parallel speedup occurred. In multithreading, four threads ran concurrently, finishing at different times (1.35–2.81 seconds), showing overlap but not true parallelism due to the GIL. Overall, multithreading provides concurrency, while multiprocessing enables true parallelism, though the benefit is seen only with multiple processes or heavier workloads.

### 3. Can Python handle true parallelism using threads? Why or why not?
    - No, Python cannot handle true parallelism using threads. This is because of the Global Interpreter Lock (GIL), which allows only one thread to execute Python bytecode at a time. Even if multiple threads exist, they take turns running instead of executing simultaneously on multiple CPU cores. As a result, Python threads provide concurrency but not true parallelism for CPU-bound tasks. True parallelism in Python is achieved using multiprocessing, where each process has its own GIL and can run on separate CPU cores.

### 4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?
    - If you input a large number of grades, such as 1000, multiprocessing will be faster than multithreading because each process runs on its own CPU core with a separate GIL, allowing true parallel execution, whereas multithreading is limited by the GIL and cannot run CPU-heavy calculations simultaneously.

### 5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?
    - For CPU-bound tasks (heavy calculations, large data processing), multiprocessing is better because it allows true parallelism across multiple CPU cores. For I/O-bound tasks (file reading/writing, network requests, waiting for input), multithreading is better because threads can run concurrently and utilize idle waiting time efficiently, even though they share the same GIL.

### 6. How did your group apply creative coding or algorithmic solutions in this lab?
    - In this lab, our group applied creative coding and algorithmic solutions by using both multithreading and multiprocessing to calculate GWA for multiple students or large sets of grades. We creatively divided the grades into smaller groups for threads, allowing concurrent execution, and used separate processes to achieve true parallelism for CPU-heavy calculations. Additionally, we implemented locks and queues to safely store results without data corruption, demonstrating algorithmic thinking in managing concurrency, synchronization, and efficient workload distribution.