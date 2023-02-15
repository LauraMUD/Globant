CREATE OR REPLACE VIEW employee_for_each_job_Q2021 
AS
SELECT departments.departments_name, 
       jobs.job_name, 
       CONCAT(hired_employees.idhired_employees,"-",hired_employees.employee_name) AS employees,
       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 1 THEN 1 ELSE 0 END) AS Q1,
       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 2 THEN 1 ELSE 0 END) AS Q2,
       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 3 THEN 1 ELSE 0 END) AS Q3,
       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 4 THEN 1 ELSE 0 END) AS Q4
FROM process_globant.`(hired_employees)` hired_employees
INNER JOIN process_globant.`(departments)` departments
ON hired_employees.departments_code = departments.iddepartments
INNER JOIN process_globant.`(jobs.)` jobs
ON hired_employees.job_code = jobs.idjobs
WHERE YEAR(hired_employees.hired_date) = 2021
GROUP BY departments.departments_name, jobs.job_name, employees
ORDER BY departments.departments_name, jobs.job_name;