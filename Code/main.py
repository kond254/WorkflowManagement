from db import Databank

db= Databank()

x=2251799813788528
candidates = db.select_new_employees(x)
db.join_new_employee_data(candidates)


newEmployeeCount = db.check_Count_new_employees(x)
numberOfpositions = db.check_number_of_positions(x)
print(newEmployeeCount)
print(numberOfpositions)
if newEmployeeCount == numberOfpositions:
    print("a")
else:
    print("b")
    
newEmployeeCount = db.check_Count_new_employees(x)
Salary = db.check_annual_salary(x)
print(newEmployeeCount)
print(Salary)
CalculatedSalarySum = newEmployeeCount*Salary[0]*Salary[1]
print(CalculatedSalarySum)
if CalculatedSalarySum == 107.68:
    print("True")
else:
    print("False")