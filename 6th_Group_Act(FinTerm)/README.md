## Antonio's Reflection:

we first thought parallel algorithms would always be faster. The results showed this is not true.

Sequential code is simple and runs step by step. Parallel code splits data, runs multiple processes, and combines results. This adds extra work.

The results showed:
- 1,000 elements: parallel was about 80× slower  
- 1,000,000 elements: both were almost the same  

The delay comes from starting processes and moving data between them.

In the search task, we first got the wrong result because we took the fastest output. qw fixed it by checking all results and selecting the smallest index.

## Key Takeaways
- Parallel is not always faster  
- It adds extra setup time  
- It works better only for large tasks  
- Simple sequential code is often enough for small and medium data  

---
## Casia's Reflection:
I already learned something about sorting algorithms in theory but never truly appreciated the difference between sequential and parallel execution. Making the sequential version taught me  how the algorithm splits, sorts, and merges data recursively made the logic click. This activity did not just teach me sorting algorithms. It taught me how to think about efficiency, and that alone made it worth it. Testing special cases like already sorted and reverse sorted data also corrected a misconception I had. I thought that reverse sorted means that the output must be reversed but its actually the same output but the random integers that are generated are actually reversed also it is the worst case scenario based on that statement that i've read. This activity was actually meaningful and i learned something.
