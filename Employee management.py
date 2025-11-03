import json
from datetime import datetime
import os 
FILE_NAME = "employees.json"
def save_data():
    """Saves the current employee data to the JSON file."""
    with open(FILE_NAME, "w") as f:
        json.dump(employees, f, indent=4)
employees = {}
if os.path.exists(FILE_NAME):
    try:
        with open(FILE_NAME, "r") as f:
            employees = json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Warning: Could not decode JSON from {FILE_NAME}. Starting with empty data.")
        employees = {}
for emp_id, emp_data in employees.items():
    
    if "attendance" not in emp_data:
        emp_data["attendance"] = {}
    if isinstance(emp_data.get("attendance"), dict):
        for month, days_present_data in list(emp_data["attendance"].items()):
            
            if isinstance(days_present_data, (int, float)):
                emp_data["attendance"][month] = {
                    "days_present": days_present_data,
                    
                    "half_days": emp_data.get("half_days", {}).get(month, 0)
                }
    emp_data.pop("leaves", None)
    emp_data.pop("half_days", None)
def add_employee():
    """Adds a new employee record."""
    print("\n--- Add New Employee ---")
    emp_id = input("Enter Employee ID: ").strip()
    if emp_id in employees:
        print("❌ This ID already exists.\n")
        return
    name = input("Enter Name: ").strip()
    try:
        salary_input = input("Enter Monthly Salary: ")
        salary = float(salary_input)
        if salary <= 0:
            print("❌ Salary must be a positive number.\n")
            return
    except ValueError:
        print("❌ Invalid salary input.\n")
        return
    employees[emp_id] = {
        "name": name,
        "salary": salary,
        "attendance": {}
    }
    save_data()
    print("✅ Employee added successfully!\n")

def view_employees():
    """Displays a list of all employees."""
    print("\n--- Employee List ---")
    if not employees:
        print("No employees found.\n")
        return
    
    print("ID      | Name                    | Salary (Rs)")
    print("-" * 45)
    for emp_id, info in employees.items():
        
        print(f"{emp_id:<7} | {info['name']:<23} | {info['salary']:>10.2f}")
    print()

def delete_employee():
    """Deletes an employee record by ID."""
    emp_id = input("Enter Employee ID to delete: ").strip()
    if emp_id in employees:
        del employees[emp_id]
        save_data()
        print("✅ Employee deleted successfully!\n")
        
        print("Updated Employee List:")
        view_employees() 
        return
    else:
        print("❌ Employee ID not found.\n")

def update_employee():
    """Updates the name or salary of an existing employee."""
    emp_id = input("Enter Employee ID to update: ").strip()
    if emp_id in employees:
        print(f"Current details: Name='{employees[emp_id]['name']}', Salary='Rs{employees[emp_id]['salary']:.2f}'")
        name = input("New Name (press Enter to skip): ").strip()
        salary_input = input("New Salary (press Enter to skip): ").strip()
        
        updated = False
        if name:
            employees[emp_id]["name"] = name
            updated = True
        if salary_input:
            try:
                new_salary = float(salary_input)
                if new_salary <= 0:
                    print("❌ Salary must be a positive number. No changes made.")
                    return
                employees[emp_id]["salary"] = new_salary
                updated = True
            except ValueError:
                print("❌ Invalid salary input. No changes made.\n")
                return
        if updated:
            save_data()
            print("✅ Employee updated successfully!\n")
        else:
            print("No changes were made.\n")
    else:
        print("❌ Employee ID not found.\n")

def input_attendance():
    """Records attendance (Present or Half Day) for a specific date."""
    emp_id = input("Enter Employee ID: ").strip()
    if emp_id not in employees:
        print("❌ Employee ID not found.\n")
        return
    date_str = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        month = date_obj.strftime("%b") 
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.\n")
        return
    status = input("Enter attendance status (P for Present, H for Half Day): ").upper()
    if status not in ['P', 'H']:
        print("❌ Invalid input. Please enter 'P' or 'H'.\n")
        return
    emp_attendance = employees[emp_id]["attendance"]
    if month not in emp_attendance:
        emp_attendance[month] = {"days_present": 0, "half_days": 0}
    if status == 'P':
        emp_attendance[month]["days_present"] += 1
    elif status == 'H':
        emp_attendance[month]["half_days"] += 1
    save_data()
    print(f"✅ Attendance for {date_str} recorded successfully for {employees[emp_id]['name']}!\n")
def calculate_salary():
    """Calculates and displays the net salary for a given month."""
    emp_id = input("Enter Employee ID: ").strip()
    if emp_id not in employees:
        print("❌ Employee ID not found.\n")
        return
    month = input("Enter Month (e.g., Oct): ").strip().capitalize()
    emp = employees[emp_id]
    if month not in emp.get("attendance", {}):
        print(f"❌ No attendance record found for {month}.\n")
        return
    attendance = emp["attendance"][month]
    days_present = attendance["days_present"]
    half_days = attendance["half_days"]
    salary = emp["salary"]
    total_days = 30 
    total_present_days = days_present + half_days
    leaves = total_days - total_present_days
    if leaves < 0: leaves = 0 
    if total_present_days > total_days:
        print(f"⚠️ Warning: Total recorded days ({total_present_days}) exceeds standard month days ({total_days}).")
    daily_salary = salary / total_days
    deduction_leaves = daily_salary * leaves
    deduction_half_days = (daily_salary / 2) * half_days 
    net_salary = salary - deduction_leaves - deduction_half_days
    print(f"\n--- Salary Details for {emp['name']} ({month}) ---")
    print(f"Base Monthly Salary: Rs{salary:,.2f}")
    print(f"Days Present (Full): {days_present}")
    print(f"Half Days: {half_days}")
    print(f"Leaves (Auto-Calculated based on {total_days} days): {leaves}")
    print(f"Leaves Deduction: Rs{deduction_leaves:,.2f}")
    print(f"Half-Day Deduction: Rs{deduction_half_days:,.2f}")
    print(f"Net Salary Payable: Rs{net_salary:,.2f}\n")
def enter_attendance_and_salary():
    """Records attendance and immediately calculates and displays the new salary."""
    emp_id = input("Enter Employee ID: ").strip()
    if emp_id not in employees:
        print("❌ Employee ID not found.\n")
        return
    date_str = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        month = date_obj.strftime("%b")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.\n")
        return
    status = input("Enter attendance status (P for Present, H for Half Day): ").upper()
    if status not in ['P', 'H']:
        print("❌ Invalid input. Please enter 'P' or 'H'.")
        return
    emp_attendance = employees[emp_id]["attendance"]
    if month not in emp_attendance:
        emp_attendance[month] = {"days_present": 0, "half_days": 0}
    if status == 'P':
        emp_attendance[month]["days_present"] += 1
    elif status == 'H':
        emp_attendance[month]["half_days"] += 1
    save_data()
    print(f"✅ Attendance for {date_str} recorded successfully!")
    calculate_salary_display(emp_id, month) 
def calculate_salary_display(emp_id, month):
    """Helper function to calculate and display salary after attendance is entered."""
    emp = employees[emp_id]
    attendance = emp["attendance"][month]
    days_present = attendance["days_present"]
    half_days = attendance["half_days"]
    salary = emp["salary"]
    total_days = 30
    total_present_days = days_present + half_days
    leaves = total_days - total_present_days
    if leaves < 0: leaves = 0
    daily_salary = salary / total_days
    deduction_leaves = daily_salary * leaves
    deduction_half_days = (daily_salary / 2) * half_days
    net_salary = salary - deduction_leaves - deduction_half_days
    print(f"\n--- Current Salary Details for {emp['name']} ({month}) ---")
    print(f"Base Monthly Salary: Rs{salary:,.2f}")
    print(f"Days Present (Full): {days_present}")
    print(f"Half Days: {half_days}")
    print(f"Leaves (Auto-Calculated): {leaves}")
    print(f"Leaves Deduction: Rs{deduction_leaves:,.2f}")
    print(f"Half-Day Deduction: Rs{deduction_half_days:,.2f}")
    print(f"Net Salary Payable: Rs{net_salary:,.2f}\n")
def sales_target():
    """Allows HR to check sales target and apply a bonus."""
    emp_id = input("Enter Employee ID: ").strip()
    if emp_id not in employees:
        print("❌ Employee ID not found.\n")
        return
    try:
        target = float(input("Enter Sales Target: ").strip())
        achieved_sales = float(input("Enter Achieved Sales: ").strip())
        if target <= 0 or achieved_sales < 0:
            print("❌ Target must be positive and achieved sales must be non-negative.\n")
            return
    except ValueError:
        print("❌ Invalid input for sales target or achieved sales.\n")
        return
    employee = employees[emp_id]
    salary = employee['salary']
    if achieved_sales < target:
        print("Sales are less than the target. We will conduct a training session to enhance selling skills so you can perform better next time. See you at training!")
    else:
        bonus = 0.05 * salary
        employee['salary'] += bonus
        save_data()
        print(f"Congratulations! You have achieved the target successfully. A bonus of Rs{bonus:,.2f} has been added to your base monthly salary, which is now Rs{employee['salary']:,.2f}.")
    print()
def enter_attendance_for_employee():
    """Allows an employee to mark their own attendance."""
    emp_id = input("Enter your Employee ID: ").strip()
    if emp_id not in employees:
        print("❌ Employee ID not found.")
        return
    date_str = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        month = date_obj.strftime("%b")
    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        return
    status = input("Enter attendance status (P for Present, H for Half Day): ").upper()
    if status not in ['P', 'H']:
        print("❌ Invalid input. Please enter 'P' or 'H'.")
        return
    emp_attendance = employees[emp_id].get("attendance", {})
    if month not in emp_attendance:
        emp_attendance[month] = {"days_present": 0, "half_days": 0}
    if status == 'P':
        employees[emp_id]["attendance"][month]["days_present"] += 1
    elif status == 'H':
        employees[emp_id]["attendance"][month]["half_days"] += 1
    save_data()
    print(f"✅ Attendance for {date_str} recorded successfully!\n")
def main_menu():
    """The main menu for Human Resources."""
    while True:
        print("=== Employee Management System (HR) ===")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Delete Employee")
        print("4. Update Employee")
        print("5. Enter Attendance (Manual/Historical)")
        print("6. Calculate Salary")
        print("7. Enter Attendance and Calculate Salary")
        print("8. Check Sales Target & Apply Bonus")
        print("9. Exit")
        choice = input("Choose (1-9): ").strip()
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            delete_employee()
        elif choice == "4":
            update_employee()
        elif choice == "5":
            input_attendance()
        elif choice == "6":
            calculate_salary()
        elif choice == "7":
            enter_attendance_and_salary()
        elif choice == "8":
            sales_target()
        elif choice == "9":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, please try again.\n")
def this_menu():
    """The menu for general Employees (Attendance Only)."""
    while True:
        print("\n--- Employee Attendance Menu ---")
        print("1. Enter Attendance for a Date")
        print("2. Back to Login/Exit")
        choice = input("Choose (1-2): ").strip()
        if choice == "1":
            enter_attendance_for_employee()
        elif choice == "2":
            print("Logging out.\n")
            break
        else:
            print("❌ Invalid choice. Please try again.")
if __name__ == "__main__":
    
    print("Welcome to the Employee System.")
    this_list = ["Select from the list", "Human Resources", "Employee"]
    print(this_list)
    
    selection = input("Please select your department from the list: ").strip()

    if selection == "Human Resources":
        password = input("Enter HR Password: ")
        if password == "Huzaifa Kabir":
            print("\n✅ Welcome to the HR system.")
            main_menu()
        else:
            print("\n❌ Invalid password. Access denied.")
    elif selection == "Employee":
        Employee_id = input("Enter your Employee Id: ").strip()
        Passwordd = input("Enter your password: ").strip()
        if Employee_id in employees:
            print(f"\n✅ Welcome, {employees[Employee_id]['name']}.")
            this_menu()
        else:
            print("\n❌ Employee ID not found or invalid credentials.")
    else:
        print("\n❌ Access denied or invalid department selected.")
