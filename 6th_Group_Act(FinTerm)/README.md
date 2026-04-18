## Antonio's Reflection:
I first thought parallel algorithms would always be faster, but the results showed this is not true. Sequential code is simple and runs step by step, while parallel code splits the data, runs multiple processes, and combines the results, which adds extra work.
The tests showed that for 1,000 elements, parallel was about 80× slower, while for 1,000,000 elements, both were almost the same. The delay comes from starting processes and moving data between them.
In the search task, I first got the wrong result because I took the fastest output. I fixed it by checking all results and choosing the smallest index.

Parallel is not always faster because it adds extra setup time. It works better only for large tasks, while simple sequential code is often enough for small and medium data.
---
## Casia's Reflection:
I already learned something about sorting algorithms in theory but never truly appreciated the difference between sequential and parallel execution. Making the sequential version taught me  how the algorithm splits, sorts, and merges data recursively made the logic click. This activity did not just teach me sorting algorithms. It taught me how to think about efficiency, and that alone made it worth it. Testing special cases like already sorted and reverse sorted data also corrected a misconception I had. I thought that reverse sorted means that the output must be reversed but its actually the same output but the random integers that are generated are actually reversed also it is the worst case scenario based on that statement that i've read. This activity was actually meaningful and i learned something.

---
## Anino's Reflection
During the activity on sequential vs parallel algorithms, I realized that adding more processes does not always make a program faster. Even with a large dataset, the sequential linear search performed better because the overhead of creating multiple processes in Python took more time than the search itself. I also found the parallel version more complex to implement, especially when handling index offsets and cases where the target was not found. This experience taught me that choosing the right approach depends on understanding the problem and its constraints, not just assuming that parallelism is always better.

---
## Flores's Reflection
Working through both the linear search and merge sort implementations, the most important observation was that sequential code executes in a single, predictable flow, while parallel code must spend time organizing workers, dividing data, and collecting results before any speedup is realized. Because of this, parallel versions were slower for small datasets and only became useful for larger ones. The extra costs of creating processes, transferring data, and merging results limit the benefits, so parallelism is best suited for large, heavy tasks, while sequential code is better for smaller or simpler ones. One challenge encountered during implementation was managing the process pool and using proper guards, as incorrect handling could lead to errors or unexpected behavior.

---
## Espina's Reflection
This activity helped me understand that performance is not only about the algorithm itself, but also about execution overhead. At first, I expected the parallel versions to always win because they use multiple processes. After running the benchmarks on small, medium, and large datasets, I realized that parallelism only becomes useful when the workload is big enough to justify process creation and communication costs.

In the sorting task, I saw that both sequential and parallel merge sort produce correct outputs, but their runtime behavior depends heavily on dataset size. In the searching task, I also learned that correctness is just as important as speed, especially when handling chunk boundaries and returning the proper global index.

Overall, this project made me more careful in evaluating efficiency. Instead of assuming that "parallel = faster," I now understand that the better approach depends on the problem size, system resources, and the overhead involved.
