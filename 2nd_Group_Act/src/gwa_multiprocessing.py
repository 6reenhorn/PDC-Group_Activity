from multiprocessing import Process, Queue
import time
import random

def compute_gwa_mp(grades, process_id, result_queue):
    start_time = time.time()
    
    print(f"[{time.strftime('%H:%M:%S')}] Process-{process_id} START - Grades: {grades}")
    
    time.sleep(random.uniform(1, 3))
    
    gwa = sum(grades) / len(grades)
    duration = time.time() - start_time
    
    print(f"[{time.strftime('%H:%M:%S')}] Process-{process_id} END - GWA: {gwa:.2f} (Time: {duration:.2f}s)")
    
    result_queue.put((process_id, gwa, duration))

def main():
    grades_list = []
    num_students = int(input("Enter number of students: "))
    
    for i in range(num_students):
        print(f"\nStudent {i+1}:")
        num_grades = int(input("  How many grades? "))
        grades = []
        for j in range(num_grades):
            grade = float(input(f"    Grade {j+1}: "))
            grades.append(grade)
        grades_list.append(grades)
    
    print("\nStarting processes...\n")
    
    processes = []
    result_queue = Queue()
    overall_start = time.time()
    
    for i, grades in enumerate(grades_list):
        p = Process(target=compute_gwa_mp, args=(grades, i+1, result_queue))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    overall_end = time.time()
    
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    print("\n" + "="*50)
    print("RESULTS")
    print("="*50)
    
    results.sort(key=lambda x: x[0])
    for process_id, gwa, duration in results:
        print(f"Student {process_id}: GWA = {gwa:.2f} (Time: {duration:.2f}s)")
    
    if results:
        fastest = min(results, key=lambda x: x[2])
        print(f"\nFastest process: Process-{fastest[0]} ({fastest[2]:.2f}s)")
    
    print(f"Total execution time: {overall_end - overall_start:.2f}s")
    print("\nAll processes completed.")

if __name__ == "__main__":
    main()