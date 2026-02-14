from concurrent.futures import ThreadPoolExecutor
import threading

# Employee data
employees = [
    ("Alice", 25000),
    ("Bob", 32000),
    ("Charlie", 28000),
    ("Diana", 40000),
    ("Edward", 35000)
]

# ============================================================================
# DEDUCTION FUNCTIONS (Independent Tasks)
# ============================================================================

def compute_sss(salary):
    """
    Compute SSS deduction (4.5%)
   
    Args:
        salary: Employee's gross salary
   
    Returns:
        SSS deduction amount
    """
    deduction = salary * 0.045
    thread_name = threading.current_thread().name
    print(f"  [{thread_name}] Computing SSS: ₱{deduction:,.2f}")
    return deduction

def compute_philhealth(salary):
    """
    Compute PhilHealth deduction (2.5%)
   
    Args:
        salary: Employee's gross salary
   
    Returns:
        PhilHealth deduction amount
    """
    deduction = salary * 0.025
    thread_name = threading.current_thread().name
    print(f"  [{thread_name}] Computing PhilHealth: ₱{deduction:,.2f}")
    return deduction
