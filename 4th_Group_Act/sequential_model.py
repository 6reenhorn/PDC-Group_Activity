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

