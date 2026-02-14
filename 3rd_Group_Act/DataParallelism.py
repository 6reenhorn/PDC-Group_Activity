from concurrent.futures import ProcessPoolExecutor
from typing import Dict, Any

# Define deduction rates
DEDUCTION_RATES = {
    "sss": 0.045,           # 4.5%
    "philhealth": 0.025,    # 2.5%
    "pagibig": 0.02,        # 2%
    "withholding_tax": 0.10 # 10%
}

def compute_employee_payroll(employee: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute complete payroll for a single employee.
    This function applies the same operation to a single employee's data.
    """
    name = employee["name"]
    gross_salary = employee["gross_salary"]
    
    # Calculate deductions
    sss = gross_salary * DEDUCTION_RATES["sss"]
    philhealth = gross_salary * DEDUCTION_RATES["philhealth"]
    pagibig = gross_salary * DEDUCTION_RATES["pagibig"]
    withholding_tax = gross_salary * DEDUCTION_RATES["withholding_tax"]
    
    # Calculate totals
    total_deduction = sss + philhealth + pagibig + withholding_tax
    net_salary = gross_salary - total_deduction
    
    # Return result as dictionary
    return {
        "name": name,
        "gross_salary": gross_salary,
        "sss": sss,
        "philhealth": philhealth,
        "pagibig": pagibig,
        "withholding_tax": withholding_tax,
        "total_deduction": total_deduction,
        "net_salary": net_salary
    }


def display_payroll_results(results):
    """Display payroll results in formatted output."""
    print("DATA PARALLELISM - PROCESSING ALL EMPLOYEES")
    print(f"Number of Employees: {len(results)}\n")
    print("Applying payroll computation to all employees in parallel...\n")
    print("PAYROLL COMPUTATION RESULTS")
    print("-" * 70 + "\n")
    
    total_gross = 0
    total_net = 0
    total_deductions = 0
    
    for result in results:
        print(f"Employee: {result['name']}")
        print(f"  Gross Salary:          ₱ {result['gross_salary']:>12,.2f}")
        print(f"  SSS (4.5%):            ₱ {result['sss']:>12,.2f}")
        print(f"  PhilHealth (2.5%):     ₱ {result['philhealth']:>12,.2f}")
        print(f"  Pag-IBIG (2%):         ₱ {result['pagibig']:>12,.2f}")
        print(f"  Withholding Tax (10%): ₱ {result['withholding_tax']:>12,.2f}")
        print(f"  Total Deduction:       ₱ {result['total_deduction']:>12,.2f}")
        print(f"  Net Salary:            ₱ {result['net_salary']:>12,.2f}")
        print()
        
        # Accumulate totals
        total_gross += result['gross_salary']
        total_net += result['net_salary']
        total_deductions += result['total_deduction']
    
    # Display summary statistics
    print("-" * 70)
    print("SUMMARY STATISTICS")
    print("-" * 70)
    print(f"Total Gross Salary:     ₱ {total_gross:>12,.2f}")
    print(f"Total Deductions:       ₱ {total_deductions:>12,.2f}")
    print(f"Total Net Salary:       ₱ {total_net:>12,.2f}")


def main():
    """Main function demonstrating data parallelism with ProcessPoolExecutor."""
    
    # Sample employee data
    employees = [
        {"name": "Alice", "gross_salary": 25000},
        {"name": "Bob", "gross_salary": 32000},
        {"name": "Charlie", "gross_salary": 28000},
        {"name": "Diana", "gross_salary": 35000},
        {"name": "Eve", "gross_salary": 30000}
    ]
    
    # Use ProcessPoolExecutor for parallel processing
    # executor.map() applies compute_employee_payroll to each employee
    # This demonstrates data parallelism: same function, different data
    with ProcessPoolExecutor(max_workers=5) as executor:
        # map() returns results in the same order as input
        results = list(executor.map(compute_employee_payroll, employees))
    
    # Display the results
    display_payroll_results(results)


if __name__ == "__main__":
    main()
