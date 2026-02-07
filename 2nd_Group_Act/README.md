|      Method      | Execution Order | GWA Output | Execution Time |
|------------------|-----------------|------------|----------------|
|  Multithreading  |
|  Multiprocessing |

#### Discussion

Your group should answer the following questions in a README.md or separate
file in your repository:

### 1. Which approach demonstrates true parallelism in Python? Explain.
    -The multiprocessing version demonstrates true parallelism in Python because each process runs independently on separate CPU cores without being limited by the GIL(a lock that limits Python threads to one at a time), while multithreading only simulates parallelism through concurrency.

### 2. Compare execution times between multithreading and multiprocessing.
    -

### 3. Can Python handle true parallelism using threads? Why or why not?
    -No, Python cannot handle true parallelism using threads. This is because of the Global Interpreter Lock (GIL), which allows only one thread to execute Python bytecode at a time. Even if multiple threads exist, they take turns running instead of executing simultaneously on multiple CPU cores. As a result, Python threads provide concurrency but not true parallelism for CPU-bound tasks. True parallelism in Python is achieved using multiprocessing, where each process has its own GIL and can run on separate CPU cores.

### 4. What happens if you input a large number of grades (e.g., 1000)? Which method is faster and why?

### 5. Which method is better for CPU-bound tasks and which for I/O-bound tasks?

### 6. How did your group apply creative coding or algorithmic solutions in this lab?