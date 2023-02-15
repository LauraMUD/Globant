{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, request,jsonify\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import mysql.connector\n",
    "from sqlalchemy import create_engine, text"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "app = Flask(__name__)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "\n",
    "# Connect to the MySQL database\n",
    "connection = create_engine(\"mysql+mysqldb://globantuser:pruebatecnica123@localhost/process_globant\")\n",
    "conn = connection.connect()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "employee_for_each_job_Q2021=\"\"\"\n",
    "CREATE OR REPLACE VIEW employee_for_each_job_Q2021 \n",
    "AS\n",
    "SELECT departments.departments_name, \n",
    "       jobs.job_name, \n",
    "       CONCAT(hired_employees.idhired_employees,\"-\",hired_employees.employee_name) AS employees,\n",
    "       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 1 THEN 1 ELSE 0 END) AS Q1,\n",
    "       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 2 THEN 1 ELSE 0 END) AS Q2,\n",
    "       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 3 THEN 1 ELSE 0 END) AS Q3,\n",
    "       SUM(CASE WHEN QUARTER(hired_employees.hired_date) = 4 THEN 1 ELSE 0 END) AS Q4\n",
    "FROM process_globant.`(hired_employees)` hired_employees\n",
    "INNER JOIN process_globant.`(departments)` departments\n",
    "ON hired_employees.departments_code = departments.iddepartments\n",
    "INNER JOIN process_globant.`(jobs.)` jobs\n",
    "ON hired_employees.job_code = jobs.idjobs\n",
    "WHERE YEAR(hired_employees.hired_date) = 2021\n",
    "GROUP BY departments.departments_name, jobs.job_name, employees\n",
    "ORDER BY departments.departments_name, jobs.job_name\"\"\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "departments_wmore_employees_2021=\"\"\"\n",
    "CREATE OR REPLACE VIEW departments_wmore_employees_2021 \n",
    "AS\n",
    "SELECT departments.iddepartments, \n",
    "     departments.departments_name, \n",
    "        COUNT(CONCAT(hired_employees.idhired_employees,\"-\",hired_employees.employee_name)) AS number_of_employees_hired\n",
    "FROM process_globant.`(departments)` departments\n",
    "JOIN process_globant.`(hired_employees)` hired_employees\n",
    "ON departments.iddepartments = hired_employees.departments_code\n",
    "WHERE hired_employees.hired_date BETWEEN '2021-01-01' AND '2021-12-31'\n",
    "GROUP BY departments.iddepartments, departments.departments_name\n",
    "HAVING COUNT(CONCAT(hired_employees.idhired_employees,\"-\",hired_employees.employee_name)) > (SELECT AVG(num_employees)\n",
    "                         FROM (SELECT COUNT(CONCAT(idhired_employees,\"-\",employee_name)) AS num_employees\n",
    "                           FROM process_globant.`(hired_employees)`\n",
    "                           WHERE hired_date BETWEEN '2021-01-01' AND '2021-12-31'\n",
    "                           GROUP BY departments_code) as avg_employees_per_department)\n",
    "ORDER BY number_of_employees_hired DESC;\"\"\"\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_view(query_view):\n",
    "    query = text(f\"{query_view}\")\n",
    "    result=conn.execute(query)\n",
    "    \n",
    "    \n",
    "    return print(\"View succesfully created \",result)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# API endpoint to receive new data for the transactions table and insert it into the database\n",
    "\n",
    "\n",
    "@app.route(\"/\", methods=['POST','GET'])\n",
    "def ping():\n",
    "    return jsonify({\"response\": \"Holi\"})\n",
    "\n",
    "@app.route(\"/employees_job\")\n",
    "def employees_job():\n",
    "    create_view(employee_for_each_job_Q2021)\n",
    "\n",
    "    \n",
    "    conn.close()\n",
    "    #return \"Show results\"\n",
    "    return jsonify({\"response\": \"View for employees jobs succesfully created\"})\n",
    "    \n",
    "\n",
    "@app.route(\"/employees_dept\")\n",
    "def employees_dept():\n",
    "    create_view(departments_wmore_employees_2021)\n",
    "    \n",
    "    return jsonify({\"response\": \"View for employees departments succesfully created\"})\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "if __name__==\"__main__\" :\n",
    "    #app.run(debug=True)\n",
    "    #df_dept=load_data(path_list[0])\n",
    "    #df_dept.columns =['iddepartments', 'departments_name']\n",
    "    #insert_data(df_dept,connection, table_list[0])\n",
    "    #app.debug=True\n",
    "    \n",
    "    #For Docker\n",
    "    #app.run(host=\"0.0.0.0\",port=4000)\n",
    "    # Only in my local host\n",
    "    app.run(host=\"0.0.0.0\",port=4000,debug=False)\n",
    "    "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.1"
  },
  "orig_nbformat": 4,
  "vscode": {
   "interpreter": {
    "hash": "5238573367df39f7286bb46f9ff5f08f63a01a80960060ce41e3c79b190280fa"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
