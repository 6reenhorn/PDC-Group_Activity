import time
import threading




measuring_cup_lock = threading.Lock()
tongs_lock         = threading.Lock()
ladle_lock         = threading.Lock()




def pre_process():
    """Shared prep that must happen BEFORE threads spawn (critical section)."""
    print("[PRE-PROCESS] Chopping vegetables, measuring rice & water, seasoning chicken...")
    time.sleep(1)  # simulates ~5 min prep (scaled: 1s = 5 min)
    print("[PRE-PROCESS] Done. Spawning cooking threads...\n")




def cook_rice():
    print("[Thread 1 - Rice Cooker]  STEP 1: Acquiring measuring cup lock...")
    with measuring_cup_lock:
        print("[Thread 1 - Rice Cooker]  STEP 1: Loading rice and water into cooker...")
        time.sleep(0.4)  # ~2 min
    # lock released — measuring cup now free for other threads
    print("[Thread 1 - Rice Cooker]  STEP 2: Cooking rice...")
    time.sleep(5.0)  # ~25 min
    print("[Thread 1 - Rice Cooker]  STEP 3: Auto-shutoff, switching to warm mode...")
    time.sleep(0.6)  # ~3 min
    print("[Thread 1 - Rice Cooker]  ✓ Rice is ready! (30 min)")




def cook_chicken():
    print("[Thread 2 - Burner A]     STEP 1: Heating oil in pan...")
    time.sleep(0.6)  # ~3 min
    print("[Thread 2 - Burner A]     STEP 2: Frying chicken – Side A...")
    time.sleep(2.4)  # ~12 min
    print("[Thread 2 - Burner A]     STEP 3: Flipping chicken – Side B...")
    with tongs_lock:
        print("[Thread 2 - Burner A]     STEP 3: Acquired tongs lock, flipping...")
        time.sleep(2.4)  # ~12 min
    print("[Thread 2 - Burner A]     STEP 4: Draining and resting on rack...")
    time.sleep(0.6)  # ~3 min
    print("[Thread 2 - Burner A]     ✓ Fried chicken is ready! (30 min)")
