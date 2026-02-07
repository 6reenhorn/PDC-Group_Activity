from multiprocessing import Process, Queue, current_process
import time
import random

def compute_gwa_mp(student_id, grades, result_queue):
    """Calculate GWA and store result in queue"""
    time.sleep(random.uniform(0.5, 2.0)) 
    
    gwa = sum(grades) / len(grades)
    process_name = current_process().name
    
    result_queue.put({
        'student_id': student_id,
        'gwa': gwa,
        'process_name': process_name,
        'num_subjects': len(grades)
    })
    
    print(f"[{process_name}] Student {student_id} GWA calculated: {gwa:.2f}")

def main():
    all_grades = []
    
    num_students = int(input("Enter number of students: "))
    
    for s in range(num_students):
        print(f"\nStudent {s + 1}")
        num_subjects = int(input("  Number of subjects: "))
        
        grades = []
        for i in range(num_subjects):
            grade = float(input(f"    Subject {i + 1} grade: "))
            grades.append(grade)
        
        all_grades.append(grades)
    
    print("\n" + "="*60)
    print("Starting GWA calculations in parallel...")
    print("="*60 + "\n")
    
    processes = []
    result_queue = Queue()
    
    for i, grades in enumerate(all_grades):
        p = Process(
            target=compute_gwa_mp,
            args=(i + 1, grades, result_queue),
            name=f"Process-Student-{i + 1}"
        )
        processes.append(p)
        p.start()
    
    for p in processes:
        p.join()
    
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    
    results = []
    while not result_queue.empty():
        results.append(result_queue.get())
    
    results.sort(key=lambda x: x['student_id'])
    
    for result in results:
        print(f"\nStudent {result['student_id']}:")
        print(f"  GWA: {result['gwa']:.2f}")
        print(f"  Subjects: {result['num_subjects']}")
        print(f"  Processed by: {result['process_name']}")
    
    if results:
        class_avg = sum(r['gwa'] for r in results) / len(results)
        print(f"\n{'='*60}")
        print(f"Class Average GWA: {class_avg:.2f}")
        print(f"{'='*60}")
    
    print("\nAll processes have finished execution.")

if __name__ == "__main__":
    main()