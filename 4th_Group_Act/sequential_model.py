import time

def pre_process():
    """Shared prep that must happen before cooking (critical section)."""
    print("[PRE-PROCESS] Chopping vegetables, measuring rice & water, seasoning chicken...")
    time.sleep(1)  # simulates 5 min prep (scaled: 1s = 5 min)
    print("[PRE-PROCESS] Done. Starting to cook...\n")

def cook_rice():
    print("[Thread 1 - Rice Cooker]  STEP 1: Loading rice and water into cooker...")
    time.sleep(0.4)  # ~2 min
    print("[Thread 1 - Rice Cooker]  STEP 2: Cooking rice...")
    time.sleep(5.0)  # ~25 min
    print("[Thread 1 - Rice Cooker]  STEP 3: Auto-shutoff, switching to warm mode...")
    time.sleep(0.6)  # ~3 min
    print("[Thread 1 - Rice Cooker]  ✓ Rice is ready! (30 min)\n")

def cook_chicken():
    print("[Thread 2 - Burner A]     STEP 1: Heating oil in pan...")
    time.sleep(0.6)  # ~3 min
    print("[Thread 2 - Burner A]     STEP 2: Frying chicken – Side A...")
    time.sleep(2.4)  # ~12 min
    print("[Thread 2 - Burner A]     STEP 3: Flipping chicken – Side B...")
    time.sleep(2.4)  # ~12 min
    print("[Thread 2 - Burner A]     STEP 4: Draining and resting on rack...")
    time.sleep(0.6)  # ~3 min
    print("[Thread 2 - Burner A]     ✓ Fried chicken is ready! (30 min)\n")

def cook_soup():
    print("[Thread 3 - Burner B]     STEP 1: Boiling water...")
    time.sleep(1.6)  # ~8 min
    print("[Thread 3 - Burner B]     STEP 2: Adding pre-chopped ingredients...")
    time.sleep(0.4)  # ~2 min
    print("[Thread 3 - Burner B]     STEP 3: Simmering soup...")
    time.sleep(5.0)  # ~25 min
    print("[Thread 3 - Burner B]     STEP 4: Tasting and adjusting seasoning...")
    time.sleep(1.0)  # ~5 min
    print("[Thread 3 - Burner B]     ✓ Soup is ready! (40 min)\n")

def main():
    print("=" * 55)
    print("       SEQUENTIAL COOKING — One dish at a time")
    print("=" * 55)

    start = time.time()

    pre_process()
    cook_rice()
    cook_chicken()
    cook_soup()

    end = time.time()
    elapsed = end - start

    print("=" * 55)
    print(f"  ✓ Dinner is served! (Sequential)")
    print(f"  Total time: {elapsed:.2f}s  (simulates ~100 min)")
    print("=" * 55)

    return elapsed

if __name__ == "__main__":
    main()