import threading
import time
import random

results = []
lock = threading.Lock()

def compute_gwa(grades, thread_id):
    start_time = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} START")

    # Simulate different processing time
    time.sleep(random.uniform(1, 3))

    gwa = sum(grades) / len(grades)

    end_time = time.time()
    duration = end_time - start_time

    print(f"[{time.strftime('%H:%M:%S')}] Thread {thread_id} END - GWA: {gwa:.2f} (Time: {duration:.2f}s)")

    # Safely store results
    with lock:
        results.append((thread_id, duration))

grades_list = []

num_grades = int(input("Enter number of grades: "))

for i in range(num_grades):
    grade = float(input(f"Enter grade {i+1}: "))
    grades_list.append(grade)

threads = []

# Divide grades into groups of 2
group_size = 2
groups = [grades_list[i:i+group_size] for i in range(0, len(grades_list), group_size)]

for i, group in enumerate(groups):
    t = threading.Thread(target=compute_gwa, args=(group, i+1))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# To find the fastest thread
fastest = min(results, key=lambda x: x[1])
print(f"\nFastest thread: Thread {fastest[0]} ({fastest[1]:.2f}s)")
print("All threads completed.")