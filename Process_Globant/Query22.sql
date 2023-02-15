CREATE OR REPLACE VIEW departments_wmore_employees_2021 
AS
SELECT departments.iddepartments, 
     departments.departments_name, 
        COUNT(CONCAT(hired_employees.idhired_employees,"-",hired_employees.employee_name)) AS number_of_employees_hired
FROM process_globant.`(departments)` departments
JOIN process_globant.`(hired_employees)` hired_employees
ON departments.iddepartments = hired_employees.departments_code
WHERE hired_employees.hired_date BETWEEN '2021-01-01' AND '2021-12-31'
GROUP BY departments.iddepartments, departments.departments_name
HAVING COUNT(CONCAT(hired_employees.idhired_employees,"-",hired_employees.employee_name)) > (SELECT AVG(num_employees)
                         FROM (SELECT COUNT(CONCAT(idhired_employees,"-",employee_name)) AS num_employees
                           FROM process_globant.`(hired_employees)`
                           WHERE hired_date BETWEEN '2021-01-01' AND '2021-12-31'
                           GROUP BY departments_code) as avg_employees_per_department)
ORDER BY number_of_employees_hired DESC;