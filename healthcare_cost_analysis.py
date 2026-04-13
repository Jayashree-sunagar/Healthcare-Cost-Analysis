import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector 

conn = mysql.connector.connect(
    host="localhost",
    user="root",          
    password="pooja27",
    database="healthcare_cost"
)
cursor = conn.cursor()
print("mysql connected succesfully")

cursor.execute("CREATE DATABASE IF NOT EXISTS healthcare_cost")
print("Database created")

cursor.execute("""
CREATE TABLE IF NOT EXISTS HealthcareData (
    ID INT PRIMARY KEY,
    Age INT,
    Sex VARCHAR(10),
    BMI FLOAT,
    Children INT,
    Smoker VARCHAR(10),
    Region VARCHAR(50),
    Charges FLOAT
)
""")

conn.commit()
print("Table created")

df = pd.read_csv('medical_cost.csv')

df["ID"] = range(1, len(df) + 1)

for index, row in df.iterrows():
    cursor.execute("""
    INSERT INTO HealthcareData 
    (ID, Age, Sex, BMI, Children, Smoker, Region, Charges)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """,
    (int(row.ID), int(row.age), row.sex, float(row.bmi),
     int(row.children), row.smoker, row.region, float(row.charges)))

conn.commit()
print("CSV data inserted into MySQL!")



print(df.head())
print(df.info())
print(df.describe())

print(df.isnull().sum())

#Data Exploration
#count of age and sex acoording to patients distribution
print(df['age'].value_counts())
print(df['sex'].value_counts())

#BMI distribution
print(df['bmi'].describe())

#children
print(df['children'].value_counts())    

#smokers distribution
print(df['smoker'].value_counts())  

print(df.groupby("region")["charges"].mean())

#data analysis
print("average cahrges by age ")
print(df.groupby("age")["charges"].mean())

print("average by gender")
print(df.groupby("sex")["charges"].mean())  

print("average by smokers distribution")
print(df.groupby("smoker")["charges"].mean())   

print("average based on number of children")
print(df.groupby("children")["charges"].mean()) 

print("highest charge :", max(df['charges'] ))
print("lowest charge : ",min(df['charges'] ))    

#visualization by ploting the graphs

df['sex'].value_counts().plot(kind='bar')
plt.title("Gender distribution")
plt.xlabel("sex")
plt.ylabel("count")     
plt.show()

sns.countplot(x="children", data=df)
plt.title("Children Distribution")
plt.show()

sns.boxplot(x="region",y="charges",data=df)
plt.title("region and charges")
plt.show()




