#Project libraries

from flask import Flask, request,jsonify
import pandas as pd
import numpy as np
import mysql.connector
from sqlalchemy import create_engine, text

app = Flask(__name__)

#Parameters for functions
path_list=['./departments.csv','./jobs.csv','./hired_employees.csv']
table_list=['process_globant.`(departments)`','process_globant.`(jobs.)`','process_globant.`(hired_employees)`']

# Connect to the MySQL database
connection = create_engine("mysql+mysqldb://globantuser:pruebatecnica123@localhost/process_globant")
conn = connection.connect()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#     functions for, load data validations for each table, table control and insertion data
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def load_data(file_path):
    """Load the data into a pandas dataframe."""
    df = pd.read_csv(file_path, delimiter=',', header=None)
    return df

def validate_data_job_dept(df):
    """Validate the data in the dataframe."""
    # Check for missing values
    missing_values = df.isnull().sum()
    if missing_values.sum() > 0:
        print("Missing values:")
        print(missing_values)
        return False

    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print("Duplicate rows:")
        print(duplicates)
        return False
    
    # Covert data types in each column
    #df['departments_name'] = df['departments_name'].astype(pd.StringDtype())
    #df['job_name'] = df['job_name'].astype(pd.StringDtype())
    #df['employee_name'] = df['employee_name'].astype(pd.StringDtype())
    #df['hired_date'] = pd.to_datetime(df['hired_date'])
    return True

def validate_data_he(df):
    """Validate the data in the dataframe."""

    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print("Duplicate rows:")
        print(duplicates)
        return False

    return True

def drop_table(table_name):
    drop_table_sql = text(f"DROP TABLE IF EXISTS {table_name}")
    conn.execute(drop_table_sql)

def insert_data(df, connector, table_name):
    #
    if len(df)< 1000:
        return df.to_sql(name="({})".format(table_name), con=connector, if_exists="append", index=False, chunksize = 1000, method='multi')
    else: 
        return print("Warning data entered",df.to_sql(name="({})".format(table_name), con=connector, if_exists="append", index=False, chunksize = 1000, method='multi')) 
    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Read Dataframe by table
df_dept=load_data(path_list[0])
df_dept.columns =['iddepartments', 'departments_name']
df_job=load_data(path_list[1])
df_job.columns =['idjobs', 'job_name']
df_he=load_data(path_list[2])
df_he.columns =['idhired_employees', 'employee_name','hired_date','departments_code','job_code']

# API endpoint to receive new data for the transactions table and insert it into the database

#test
@app.route("/", methods=['POST','GET'])
def ping():
    return jsonify({"response": "Holi"})

@app.route("/drop_table_departments")
def drop_table_departments():

    drop_table(table_list[0])
    conn.close()
    return jsonify({"response": "Table departments dropped successfully"})

@app.route("/drop_table_jobs")
def drop_table_jobs():

    drop_table(table_list[1])
    conn.close()
    return jsonify({"response": "Table jobs dropped successfully"})

@app.route("/drop_table_hiredemployees")
def drop_table_hiredemployees():

    drop_table(table_list[2])
    conn.close()
    return jsonify({"response": "Table hired employees dropped successfully"})


@app.route("/write_data_departments")
def write_data_departments():
    
    if validate_data_job_dept(df_dept):
        insert_data(df_dept,connection,table_list[0])
    else:
        "No valid Data for departments"
    conn.close()
    return "Data inserted successfully", 201

@app.route("/write_data_jobs")
def write_data_jobs():
    
    if validate_data_job_dept(df_job):
        insert_data(df_job,connection,table_list[1])
    else:
        "No valid Data for jobs"
    conn.close()
    return "Data inserted successfully", 201

@app.route("/write_data_hiredemployees")
def write_data_hiredemployees():

    if validate_data_he(df_he):
        insert_data(df_he,connection,table_list[2])
    else:
        "No valid Data for hired employees"
    conn.close()
    return "Data inserted successfully", 201

if __name__=="__main__" :
    #app.run(debug=True)
    #df_dept=load_data(path_list[0])
    #df_dept.columns =['iddepartments', 'departments_name']
    #insert_data(df_dept,connection, table_list[0])
    #app.debug=True
    
    #For Docker
    #app.run(host="0.0.0.0",port=4000)
    # Only in my local host
    app.run(host="0.0.0.0",port=4000,debug=False)