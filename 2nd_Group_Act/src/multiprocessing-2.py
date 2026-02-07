from multiprocessing import Process, current_process
import time
import random

def compute_gwa_mp(grades):
    time.sleep(random.uniform(0.5, 2.0))

    gwa = sum(grades) / len(grades)
    print(f"[{current_process().name}] GWA calculated: {gwa:.2f}")

def main():
    all_grades = []

    num_students = int(input("Enter number of students: "))

    for s in range(num_students):
        print(f"\nStudent {s + 1}")
        num_subjects = int(input("  Number of subjects: "))

        grades = []
        for i in range(num_subjects):
            grade = float(input(f"  Grade {i + 1}: "))
            grades.append(grade)

        all_grades.append(grades)

    processes = []

    for i, grades in enumerate(all_grades):
        p = Process(
            target=compute_gwa_mp,
            args=(grades,),
            name=f"Process-{i + 1}"
        )
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("\nAll processes have finished execution.")

if __name__ == "__main__":
    main()