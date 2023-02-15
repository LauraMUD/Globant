#Project libraries

from flask import Flask, request,jsonify
import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Connect to the MySQL database
connection = create_engine("mysql+mysqldb://globantuser:pruebatecnica123@localhost/process_globant")
conn = connection.connect()


#View for the first metric
employee_for_each_job_Q2021="""
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
ORDER BY departments.departments_name, jobs.job_name"""

#View for the second metric
departments_wmore_employees_2021="""
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
ORDER BY number_of_employees_hired DESC;"""


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#     functions for create views in MySQL database
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def create_view(query_view):
    query = text(f"{query_view}")
    result=conn.execute(query)
    
    
    return print("View succesfully created ",result)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# API endpoint to receive new data for the transactions table and insert it into the database

#test

@app.route("/", methods=['POST','GET'])
def ping():
    return jsonify({"response": "Holi"})

@app.route("/employees_job")
def employees_job():
    create_view(employee_for_each_job_Q2021)

    
    conn.close()
    #return "Show results"
    return jsonify({"response": "View for employees jobs succesfully created"})
    

@app.route("/employees_dept")
def employees_dept():
    create_view(departments_wmore_employees_2021)
    
    return jsonify({"response": "View for employees departments succesfully created"})

if __name__=="__main__" :    
    #For Docker
    app.run(host="0.0.0.0",port=4000,debug=False)