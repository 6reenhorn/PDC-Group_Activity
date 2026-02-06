from multiprocessing import Process

def compute_gwa_mp(grades):
    gwa = sum(grades) / len(grades)
    print(f"[Process] Calculated GWA: {gwa}")

grades_list = [85, 90, 78, 92] # Replace with user input

processes = []
for grade in grades_list:
    p = Process(target=compute_gwa_mp, args=([grade],))
    processes.append(p)
    p.start()

for p in processes:
    p.join()