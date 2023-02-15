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
    "path_list=['./departments.csv','./jobs.csv','./hired_employees.csv']\n",
    "table_list=['process_globant.`(departments)`','process_globant.`(jobs.)`','process_globant.`(hired_employees)`']\n",
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
    "def load_data(file_path):\n",
    "    \"\"\"Load the data into a pandas dataframe.\"\"\"\n",
    "    df = pd.read_csv(file_path, delimiter=',', header=None)\n",
    "    return df\n",
    "\n",
    "def validate_data_job_dept(df):\n",
    "    \"\"\"Validate the data in the dataframe.\"\"\"\n",
    "    # Check for missing values\n",
    "    missing_values = df.isNone().sum()\n",
    "    if missing_values.sum() > 0:\n",
    "        print(\"Missing values:\")\n",
    "        print(missing_values)\n",
    "        return False\n",
    "\n",
    "    # Check for duplicates\n",
    "    duplicates = df.duplicated().sum()\n",
    "    if duplicates > 0:\n",
    "        print(\"Duplicate rows:\")\n",
    "        print(duplicates)\n",
    "        return False\n",
    "    \n",
    "    # Covert data types in each column\n",
    "    #df['departments_name'] = df['departments_name'].astype(pd.StringDtype())\n",
    "    #df['job_name'] = df['job_name'].astype(pd.StringDtype())\n",
    "    #df['employee_name'] = df['employee_name'].astype(pd.StringDtype())\n",
    "    #df['hired_date'] = pd.to_datetime(df['hired_date'])\n",
    "    return True\n",
    "\n",
    "def validate_data_he(df):\n",
    "    \"\"\"Validate the data in the dataframe.\"\"\"\n",
    "\n",
    "    # Check for duplicates\n",
    "    duplicates = df.duplicated().sum()\n",
    "    if duplicates > 0:\n",
    "        print(\"Duplicate rows:\")\n",
    "        print(duplicates)\n",
    "        return False\n",
    "\n",
    "    return True\n",
    "\n",
    "def drop_table(table_name):\n",
    "    drop_table_sql = text(f\"DROP TABLE IF EXISTS {table_name}\")\n",
    "    conn.execute(drop_table_sql)\n",
    "\n",
    "def insert_data(df, connector, table_name):\n",
    "    #\n",
    "    if len(df)< 1000:\n",
    "        return df.to_sql(name=\"({})\".format(table_name), con=connector, if_exists=\"append\", index=False, chunksize = 1000, method='multi')\n",
    "    else: \n",
    "        return print(\"Warning data entered\",df.to_sql(name=\"({})\".format(table_name), con=connector, if_exists=\"append\", index=False, chunksize = 1000, method='multi')) "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "#Read Dataframe by table\n",
    "df_dept=load_data(path_list[0])\n",
    "df_dept.columns =['iddepartments', 'departments_name']\n",
    "df_job=load_data(path_list[1])\n",
    "df_job.columns =['idjobs', 'job_name']\n",
    "df_he=load_data(path_list[2])\n",
    "df_he.columns =['idhired_employees', 'employee_name','hired_date','departments_code','job_code']"
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
    "@app.route(\"/drop_table_departments\")\n",
    "def drop_table_departments():\n",
    "\n",
    "    drop_table(table_list[0])\n",
    "    conn.close()\n",
    "    return \"Table departments dropped successfully\", 201\n",
    "\n",
    "@app.route(\"/drop_table_jobs\")\n",
    "def drop_table_jobs():\n",
    "\n",
    "    drop_table(table_list[1])\n",
    "    conn.close()\n",
    "    return \"Table jobs dropped successfully\", 201\n",
    "\n",
    "@app.route(\"/drop_table_hiredemployees\")\n",
    "def drop_table_hiredemployees():\n",
    "\n",
    "    drop_table(table_list[2])\n",
    "    conn.close()\n",
    "    return \"Table hiredemployees dropped successfully\", 201\n",
    "\n",
    "@app.route(\"/write_data_departments\")\n",
    "def write_data_departments():\n",
    "    \n",
    "    if validate_data_job_dept(df_dept):\n",
    "        insert_data(df_dept,connection,table_list[0])\n",
    "    else:\n",
    "        \"No valid Data for departments\"\n",
    "    conn.close()\n",
    "    return \"Data inserted successfully\", 201\n",
    "\n",
    "@app.route(\"/write_data_jobs\")\n",
    "def write_data_jobs():\n",
    "    \n",
    "    if validate_data_job_dept(df_job):\n",
    "        insert_data(df_job,connection,table_list[1])\n",
    "    else:\n",
    "        \"No valid Data for jobs\"\n",
    "    conn.close()\n",
    "    return \"Data inserted successfully\", 201\n",
    "\n",
    "@app.route(\"/write_data_hiredemployees\")\n",
    "def write_data_hiredemployees():\n",
    "\n",
    "    if validate_data_he(df_he):\n",
    "        insert_data(df_he,connection,table_list[2])\n",
    "    else:\n",
    "        \"No valid Data for hired employees\"\n",
    "    conn.close()\n",
    "    return \"Data inserted successfully\", 201\n"
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
