# Running Instructions & Technical Documentation

## Overview

This document provides complete technical information, running instructions, and performance analysis guidance for the Sequential vs Parallel Algorithms project.

---

## Dataset Sizes

All benchmarks use the following standardized dataset sizes for consistent evaluation:

- **Small Dataset** → 1,000 elements
- **Medium Dataset** → 100,000 elements  
- **Large Dataset** → 1,000,000 elements

These sizes test algorithm performance across different workload scales and reveal the tradeoff between sequential and parallel execution overhead.

---

## Sorting Algorithms

### Sequential Merge Sort

```bash
# Run with default size (1,000 elements)
python sequential_sort.py

# Run with custom dataset size
python sequential_sort.py --size 100000

# Run with specific large dataset size
python sequential_sort.py --size 1000000

# Show full sorted output
python sequential_sort.py --size 50000 --show-output
```

**Features:**
- Tests random, already-sorted, and reverse-sorted datasets
- Displays execution time for each dataset type
- By default shows first 1,000 elements of output

---

### Parallel Merge Sort (Multiprocessing)

```bash
# Run with default size (1,000 elements)
python parallel_sort.py

# Run with custom size
python parallel_sort.py --size 100000

# Run with large dataset using more processes
python parallel_sort.py --size 1000000 --processes 8

# Test with different process configurations
python parallel_sort.py --size 500000 --processes 4
python parallel_sort.py --size 500000 --processes 8
```

**Features:**
- Uses multiprocessing for true parallelism
- Partitions data into chunks, each sorted by a worker process
- Automatically merges sorted chunks back together
- Shows partition and process information

---

## Searching Algorithms

### Sequential Linear Search

```bash
# Run with default size (1,000 elements)
python sequential_search.py

# Run with single custom size
python sequential_search.py --size 50000

# Run all three standard sizes (1K, 100K, 1M)
python sequential_search.py --all-sizes

# Quick test with small dataset
python sequential_search.py --size 10000
```

**Features:**
- Tests: target found, target not found, sorted data, reverse-sorted data
- Shows execution time for each test case
- Can run individual size or all standard sizes

---

### Parallel Linear Search (Multiprocessing)

```bash
# Run with default configuration (all sizes + correctness tests)
python parallel_search.py

# Run all three standard sizes only
python parallel_search.py --all-sizes

# Run with single custom size
python parallel_search.py --size 100000

# Run with more processes (for testing scalability)
python parallel_search.py --all-sizes --processes 8

# Skip correctness tests and run benchmarks only
python parallel_search.py --all-sizes --skip-correctness

# Combine options
python parallel_search.py --size 500000 --processes 6 --skip-correctness
```

**Features:**
- Includes correctness tests before benchmarking
- Tests across multiple data modes (random, sorted, reverse-sorted)
- Shows speedup comparisons between sequential and parallel
- Can adjust number of processes used

---

## Running Comparisons

### Compare Sequential vs Parallel for Same Dataset Size

```bash
# Small dataset
python sequential_sort.py --size 1000
python parallel_sort.py --size 1000

# Medium dataset
python sequential_sort.py --size 100000
python parallel_sort.py --size 100000

# Large dataset
python sequential_sort.py --size 1000000 --processes 8
python parallel_sort.py --size 1000000 --processes 8
```

### Search Comparison

```bash
# Sequential baseline
python sequential_search.py --size 100000

# Parallel with same size
python parallel_search.py --size 100000 --skip-correctness

# Full benchmark with all sizes
python parallel_search.py --all-sizes
```

---

## Performance Analysis Tips

### Observe Parallelism Overhead

```bash
# Small dataset shows overhead disadvantage
python parallel_sort.py --size 1000
python sequential_sort.py --size 1000

# Large dataset shows parallelism advantage
python parallel_sort.py --size 1000000 --processes 8
python sequential_sort.py --size 1000000
```

### Test Process Scaling

```bash
# Test with increasing process counts
python parallel_sort.py --size 1000000 --processes 2
python parallel_sort.py --size 1000000 --processes 4
python parallel_sort.py --size 1000000 --processes 8
```

### Special Cases

```bash
# Already-sorted data (best case for sequential)
python sequential_sort.py --size 1000000
python parallel_sort.py --size 1000000

# Reverse-sorted data (challenging for both)
python sequential_search.py --all-sizes
python parallel_search.py --all-sizes --skip-correctness
```

---

## Configuration Constants

You can modify default settings in each file:

### sequential_sort.py
- `DEFAULT_SIZE = 1000`
- `MAX_VALUE = 1_000_000`

### parallel_sort.py
- `DEFAULT_SIZE = 1000`
- `MAX_VALUE = 1_000_000`
- `DEFAULT_PROCESSES = 4`

### sequential_search.py
- `DEFAULT_SIZE = 1000`
- `MAX_VALUE = 1_000_000`

### parallel_search.py
- `DEFAULT_SIZE = 1000`
- `MAX_VALUE = 1_000_000`
- `DEFAULT_PROCESSES = 4`

---

## Expected Observations

### Sorting Performance
- **Small datasets (1K)**: Sequential faster due to lower overhead
- **Medium datasets (100K)**: Performance becomes comparable
- **Large datasets (1M)**: Parallel usually faster with proper process count

### Searching Performance
- Linear search overhead is minimal for small chunks
- Parallel search shows overhead that grows with process creation
- Process communication (via Queue) can be significant bottleneck

### Dataset Modes
- **Random**: Balanced performance characteristics
- **Already Sorted**: Sequential may perform better
- **Reverse Sorted**: Both face similar challenges

---

## Troubleshooting

### Getting "permission denied" errors
Ensure Python files have execution permissions:
```bash
chmod +x *.py  # On macOS/Linux
```

### Memory usage too high with 1M dataset
- Use smaller process count: `--processes 2`
- Test with medium dataset: `--size 100000`

### Results show no speedup for parallel
This is expected for small datasets due to process creation overhead. Try larger datasets.

---

## Project Architecture

### Project Structure

```
6th_Group_Act(FinTerm)/
├── Sorting/
│   ├── sequential_sort.py      # Sequential merge sort
│   └── parallel_sort.py         # Parallel merge sort (multiprocessing)
├── Searching/
│   ├── sequential_search.py     # Sequential linear search
│   └── parallel_search.py       # Parallel linear search (multiprocessing)
├── README.md                    # Individual reflections & overview
└── RUNNING_INSTRUCTIONS.md      # This file - Usage & technical details
```

---

## Algorithms Implemented

### Sorting

#### Sequential Merge Sort
- **Algorithm**: Recursive merge sort with O(n log n) time complexity
- **Implementation**: Divide-and-conquer approach
- **Stability**: Stable sort
- **Space Complexity**: O(n) for merging

#### Parallel Merge Sort (Multiprocessing)
- **Approach**: Partition-Sort-Merge (PSM)
  1. **Partition**: Divide data into chunks (default: 4 chunks)
  2. **Sort**: Each chunk sorted independently by a worker process
  3. **Merge**: Sorted chunks merged back into globally sorted output
- **Process Model**: `multiprocessing.Pool` with multiple workers
- **Overhead**: Process creation, context switching, data copying, inter-process coordination

### Searching

#### Sequential Linear Search
- **Algorithm**: Linear scan through data
- **Time Complexity**: O(n) worst case, O(1) best case
- **Space Complexity**: O(1)
- **Returns**: Index of first occurrence or -1 if not found

#### Parallel Linear Search (Multiprocessing)
- **Approach**: Partition-Search-Coordinate (PSC)
  1. **Partition**: Divide data into chunks (default: 4 chunks)
  2. **Search**: Each chunk searched independently by a worker process
  3. **Coordinate**: Global index calculated from local results
- **Process Model**: `multiprocessing.Process` with `Queue` for IPC
- **Overhead**: Process creation, Queue communication, result coordination

---

## Key Concepts: Sequential vs Parallel

### Sequential Execution Characteristics
- Single control flow, step-by-step execution
- No task partitioning or inter-process comnication overhead
- Deterministic behavior, consistent results
- Low memory overhead
- Limited by single CPU core performance
- Cannot scale with additional hardware

### Parallel Execution Characteristics
- Concurrent execution on multiple cores
- Data partitioned into independent chunks
- Scales with additional CPU cores (when overhead is managed)
- Inter-process communication overhead
- Context switching costs
- Result coordination complexity

---

## Performance Analysis Framework

### When Parallelism Provides Benefit
✅ **Large datasets** (typically 100K+ elements)  
✅ **High computational load** (complex algorithms)  
✅ **Multiple available CPU cores** (2+ cores)  
✅ **When: Workload >> Communication Overhead**  

Formula: `Benefit = (Sequential Time) - (Parallel Time + Overhead) > 0`

### When Sequential is Superior
✅ **Small datasets** (< 50K elements)  
✅ **Simple operations** with fast execution  
✅ **Memory-constrained** environments  
✅ **Single-core systems** or when core count is limited  
✅ **When: Overhead dominates computation time**  

### Critical Overhead Factors
1. **Process Creation Overhead**: 1-100ms per process
2. **Context Switching**: Recurring cost during execution
3. **Data Copying**: Multiprocessing requires copying data to/from processes
4. **Queue Communication**: Serialization/deserialization costs
5. **Result Merging**: Additional computational cost at end

### Performance Prediction
```
Sequential Time: T_seq = Time to process entire dataset sequentially
Parallel Time: T_par = (T_seq / P) + Overhead
  where P = number of processes

Speedup = T_seq / T_par

Conditions for beneficial parallelism:
  - Speedup > 1.05 (need >5% improvement to overcome overhead)
  - T_seq > 1000ms (adequate workload)
  - Overhead < 10% of T_seq (reasonable overhead ratio)
```

---

## Expected Results by Dataset Size

### Small Dataset (1,000 elements)
- **Sequential**: ~0.1-1ms
- **Parallel**: ~50-100ms (includes process creation)
- **Result**: Sequential is **10-100x faster**
- **Reason**: Overhead dominates computation
- **Learning**: Demonstrates cost of parallelism

### Medium Dataset (100,000 elements)  
- **Sequential**: ~10-50ms
- **Parallel**: ~30-80ms
- **Result**: Performance comparable, parallel slightly slower
- **Reason**: Overhead still significant relative to computation
- **Learning**: Breakeven point is around this size

### Large Dataset (1,000,000 elements)
- **Sequential**: ~100-500ms
- **Parallel**: ~50-150ms (with 4+ processes)
- **Result**: Parallel is **1.5-3x faster**
- **Reason**: Computation outweighs overhead
- **Learning**: Clear benefit from parallelism

---

## Special Cases Analysis

### Already Sorted Data
- **Sequential**: Faster due to low overhead
- **Parallel**: Still incurs same overhead but gains no sorting efficiency
- **Insight**: Parallel benefits require sufficient disorder/complexity

### Reverse Sorted Data
- **Sequential**: Maximum comparisons needed
- **Parallel**: Individual chunks reverse-sorted; merge still efficient
- **Insight**: Algorithm complexity less important than absolute workload

### Target Not Found (Search)
- **Sequential**: Must scan entire dataset
- **Parallel**: All processes must complete (full scan)
- **Insight**: Worst-case scenarios negate early termination benefits

---

## Configuration & Tuning

### Optimal Process Count
```
For Sorting:
  - Small dataset: 1 process (sequential)
  - Medium dataset: 2 processes
  - Large dataset: 4-8 processes (match CPU core count)

For Searching:
  - Small/Medium: 2-4 processes
  - Large: 4 processes (diminishing returns beyond this)

Rule of thumb: 
  num_processes = min(cpu_count(), len(data) // 10000)
```

### Memory Considerations
- Multiprocessing **copies** data to each process
- 1M element array: ~8MB per process copy
- 4 processes with 1M data: ~32MB+ usage
- Adjust chunk size if memory is limited

### Chunk Size Impact
- **Smaller chunks**: Better load balancing, more communication
- **Larger chunks**: Less communication, potential load imbalance
- **Current implementation**: `len(data) // num_processes`

---

## Correctness & Verification

### Sorting Verification
All implementations verify:
- Output is strictly sorted
- Output matches Python's built-in `sorted()`
- All input elements present in output
- No duplicates added or removed

### Searching Verification
Correctness tests include:
- Target at beginning, middle, end
- Target not found (returns -1)
- Single element lists
- Multiple occurrences (returns first index)
- Boundary conditions
- Chunk boundary search

---

## Requirements

- **Python**: 3.7 or higher
- **Standard Library Only**: Uses built-in `multiprocessing`, `time`, `random`, `argparse`
- **OS**: Windows, macOS, Linux (multiprocessing works on all platforms)
- **CPU**: Multi-core system recommended for performance demonstration

---

## Environment Variables (Optional)

```bash
# Control Python's multiprocessing start method (if needed)
PYTHONMULTIPROCESSSTART=spawn  # Force spawn method

# Disable buffering for real-time output
PYTHONUNBUFFERED=1
```
