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

