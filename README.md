# Globant
## **Description**
This repository shows the procedure suggested by Globant "Proposal for coding challenge" as a test to evaluate the capabilities of a data engineer candidate.


The procedure is a dockerization of the REST APIs proposed by the challenge as well as a file to display a descriptive analysis and a file in python that is not a REST API

- In the folder called *"Process Globant"* are the files and the procedures of the challenges:
  + Challenge 1 files:
    - Challenge1_R1.py and Challenge1_R1.ipynb Procedures point 1
    - Challenge1_R2.py and Challenge1_R2.ipynb Procedures point 2
  + Challenge 2 files:
    - Challenge2_R1.py and Challenge2_R1.ipynb Procedures part1
    - Departments_Metrics.pbix Report in Power BI for procedure part1
    - Report_Challenge2.pdf static report from Power BI
    
  
- For the dockerization of the app, Alpine linux was used as image

## **Difficulties**

- In the dockerization of the procedure, it was quite difficult for me to put together the image and get the packages I needed to install correctly. The numpy, pandas and psutil python libraries gave me quite a bit of work when creating the Docker image
- When designing the application in Flask, it was difficult for me to know what I wanted to return specifically since the app focuses more on the interaction with tables in SQL databases. There are errors that I still don't know how to solve within the Flask app
- I have never worked with AVRO and in fact it is the first time I hear it so I decided to skip this part of challenge
- By carelessness I damaged the first repository that I created for this challenge, below is the link where you can see all the failed submissions <https://github.com/LauraMUD/Process_Globant>
- I was not able to migrate the application from local to Azure cloud, but I made an architecture diagram as a proposal of how to start, taking into account that within each procedure there are several details to review

## **Possible migration diagram to Azure cloud**

![alt text](https://github.com/LauraMUD/Globant/blob/master/app_architecture.drawio.png?raw=true)
