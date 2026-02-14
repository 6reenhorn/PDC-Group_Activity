Analysis Questions

### 1. Differentiate Task and Data Parallelism. Identify which part of the lab demonstrates each and justify the workload division.
- Task Parallelism and Data Parallelism differ in what runs concurrently: Task Parallelism executes different operations on the same data, while Data Parallelism applies the same operation to different data. Part A demonstrates Task Parallelism by computing four different deductions (SSS, PhilHealth, Pag-IBIG, Tax) concurrently on a single employee's salary, dividing the workload by task type where each thread handles one deduction calculation. Part B demonstrates Data Parallelism by applying the complete payroll computation function to all five employees simultaneously, dividing the workload by data where each process handles one employee's entire calculation independently.

### 2. Explain how concurrent.futures managed execution, including submit(), map(), and Future objects. Discuss the purpose of with when creating an Executor.
- The concurrent.futures module manages execution through Executors that schedule and run tasks concurrently, where submit() schedules individual tasks and immediately returns a Future object representing the eventual result that can be retrieved using result(), while map() applies a function to multiple items in parallel and returns results in order. Future objects act as placeholders for results that may not be available yet, allowing the program to continue executing while waiting for task completion. The with statement ensures proper resource management by automatically shutting down the executor and cleaning up threads or processes when the block completes, preventing resource leaks even if errors occur.

### 3. Analyze ThreadPoolExecutor execution in relation to the GIL and CPU cores. Did true parallelism occur?

### 4. Explain why ProcessPoolExecutor enables true parallelism, including memory space separation and GIL behavior.

### 5. Evaluate scalability if the system increases from 5 to 10,000 employees. Which approach scales better and why?

### 6. Provide a real-world payroll system example. Indicate where Task Parallelism and Data Parallelism would be applied, and which executor you would use.