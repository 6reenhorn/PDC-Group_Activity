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

# DEDUCTION FUNCTIONS (Independent Tasks)
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

def compute_pagibig(salary):
    """
    Compute Pag-IBIG deduction (2%)
   
    Args:
        salary: Employee's gross salary
   
    Returns:
        Pag-IBIG deduction amount
    """
    deduction = salary * 0.02
    thread_name = threading.current_thread().name
    print(f"  [{thread_name}] Computing Pag-IBIG: ₱{deduction:,.2f}")
    return deduction

def compute_tax(salary):
    """
    Compute Withholding Tax (10%)
   
    Args:
        salary: Employee's gross salary
   
    Returns:
        Withholding tax amount
    """
    deduction = salary * 0.10
    thread_name = threading.current_thread().name
    print(f"  [{thread_name}] Computing Withholding Tax: ₱{deduction:,.2f}")
    return deduction

# TASK PARALLELISM IMPLEMENTATION
def process_employee_task_parallelism(employee_name, salary):
    """
    Process a single employee's deductions using Task Parallelism.
   
    Different deduction tasks (SSS, PhilHealth, Pag-IBIG, Tax) are executed
    concurrently using ThreadPoolExecutor. All tasks operate on the same
    salary value.
   
    Args:
        employee_name: Name of the employee
        salary: Gross salary of the employee
    """
    print(f"\n{'='*70}")
    print(f"TASK PARALLELISM - PROCESSING EMPLOYEE: {employee_name.upper()}")
    print(f"{'='*70}")
    print(f"Gross Salary: ₱{salary:,.2f}")
    print(f"\nExecuting deduction tasks concurrently...\n")
   
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit each deduction task and get Future objects
        future_sss = executor.submit(compute_sss, salary)
        future_philhealth = executor.submit(compute_philhealth, salary)
        future_pagibig = executor.submit(compute_pagibig, salary)
        future_tax = executor.submit(compute_tax, salary)
       
        sss = future_sss.result()
        philhealth = future_philhealth.result()
        pagibig = future_pagibig.result()
        tax = future_tax.result()
   
    total_deduction = sss + philhealth + pagibig + tax
    net_salary = salary - total_deduction
   
    print(f"\n{'-'*70}")
    print(f"DEDUCTION BREAKDOWN")
    print(f"{'-'*70}")
    print(f"SSS (4.5%):              ₱{sss:>12,.2f}")
    print(f"PhilHealth (2.5%):       ₱{philhealth:>12,.2f}")
    print(f"Pag-IBIG (2%):           ₱{pagibig:>12,.2f}")
    print(f"Withholding Tax (10%):   ₱{tax:>12,.2f}")
    print(f"{'-'*70}")
    print(f"Total Deduction:         ₱{total_deduction:>12,.2f}")
    print(f"Net Salary:              ₱{net_salary:>12,.2f}")
    print(f"{'='*70}\n")
   
    return {
        'name': employee_name,
        'gross_salary': salary,
        'sss': sss,
        'philhealth': philhealth,
        'pagibig': pagibig,
        'tax': tax,
        'total_deduction': total_deduction,
        'net_salary': net_salary
    }

# MAIN EXECUTION
def main():
    """Main execution function for Task Parallelism demonstration"""
   
    print("\n" + "="*70)
    print("PART A - TASK PARALLELISM DEMONSTRATION")
    print("Using ThreadPoolExecutor")
    print("="*70)
   
    # Process ALL employees using Task Parallelism
    all_results = []
   
    for employee_name, salary in employees:
        result = process_employee_task_parallelism(employee_name, salary)
        all_results.append(result)
   
    # Display summary for all employees
    print("\n" + "="*70)
    print("SUMMARY - ALL EMPLOYEES")
    print("="*70)
   
    total_gross = sum(r['gross_salary'] for r in all_results)
    total_deductions = sum(r['total_deduction'] for r in all_results)
    total_net = sum(r['net_salary'] for r in all_results)
   
    print(f"Total Employees Processed: {len(all_results)}")
    print(f"Total Gross Salary:        ₱{total_gross:>12,.2f}")
    print(f"Total Deductions:          ₱{total_deductions:>12,.2f}")
    print(f"Total Net Salary:          ₱{total_net:>12,.2f}")
   
    print("="*70)

if __name__ == "__main__":
    main()
