SELECT AnnualSalary, SystemDB.Compensation FROM JobStandards
JOIN SystemDB ON JobStandards.ProcessID=SystemDB.ProcessID
WHERE SystemDB.ProcessID=?