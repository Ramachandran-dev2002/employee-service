from pathlib import Path
import sys

script_dir = Path(__file__).resolve().parent
sys.path[:] = [entry for entry in sys.path if Path(entry or ".").resolve() != script_dir]
import pandas as pd
import numpy as np

csv_path = script_dir / "employees.csv"
csv_path.write_text(
	"id,name,department,salary,city\n"
	"1,Arun,Sales,30000,Chennai\n"
	"2,Priya,HR,45000,Chennai\n"
	"3,Rahul,IT,60000,Bangalore\n"
	"4,Divya,IT,75000,Chennai\n"
	"5,Karthik,Finance,90000,Mumbai\n"
	"6,Meena,Sales,52000,Bangalore\n"
	"7,Suresh,IT,68000,Chennai\n"
	"8,Anitha,HR,48000,Mumbai\n",
	encoding="utf-8",
)
df = pd.read_csv(csv_path)

print("First five employees:")
print(df.head())
print("DataFrame information:")
df.info()
print("Numeric summary:")
print(df.describe())
print("head() shows the first five rows.")
print("info() shows column names, data types, and non-null counts.")
print("describe() summarizes numeric columns with statistics such as mean and quartiles.")

print("Names:")
print(df["name"])
print("Names and salaries:")
print(df[["name", "salary"]])

chennai_names = df.loc[df["city"] == "Chennai", "name"]
print("Chennai: " + ", ".join(chennai_names))
print("iloc slice (rows 0–2, columns 1–2):")
print(df.iloc[0:3, 1:3])

high_salary = df[df["salary"] > 50000]
it_employees = df[df["department"] == "IT"]
print(f"Salary above 50000: {len(high_salary)} employees")
print("IT department: " + ", ".join(it_employees["name"]))
print(f"IT department count: {len(it_employees)} employees")

values = np.arange(24).reshape(2, 3, 4)
print("Shape of each slice along axis 0:")
for slice_ in values:
	print(slice_.shape)
