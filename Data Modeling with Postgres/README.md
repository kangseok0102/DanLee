## Purpose
This project is designed for a startup **Sparkify** to analyze songs and user activity data on their new music streaming app

## Project Description
Since **analytics team** has no idea on writing appropriate queries on the collected data, a data engineer is supposed to create database and ETL pipeline which could read JSON metadata
on the songs in their app and transfer data from local files into fact and dimension tables

## Files

1. **sql_queries.py**: contains the sql queries and table details

2. **create_tables.py**: connects to sparkify database and executes the sql queries to create and drop tables

3. **etl.ipynb**: enables an engineer to test and process a single file by fllowing instructions in Jupyter Notebook  

4. **etl.py**: reads **song** and **log** files to transfer data based on the table requirements
    
    - **Fact Table**: songplay
    - **Demension Table**: user, songs, artists, time

5. **test.ipynb**: shows few rows of each table to see if database and queries perform well 


## Diagram

![Fact and Dimensional Tables Connection](C:\Users\Dan Lee\Desktop\Diagram.jpg)


## ETL Process

1. Run create_tables.py file to establish connection with **Sparkify** database and create tables according to the sql queries in sql_queries.py

2. Run etl.py file to extract and transfer JSON metadata to fact and dimension tables







