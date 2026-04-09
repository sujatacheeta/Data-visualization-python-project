import pandas as pd
import random

students = [
"Umang","Harsh","Manish","Akash","Rishita","Aarav","Riya","Karan","Meenal","Rahul",
"Simran","Amit","Neha","Vijay","Pooja","Rohit","Anita","Deepak","Kiran","Tina",
"Arjun","Sakshi","Naman","Isha","Yash","Kriti","Rakesh","Divya","Mohit","Payal",
"Suresh","Anjali","Gaurav","Nisha","Tarun","Pallavi","Aman","Rekha","Sumit","Preeti",
"Ajay","Komal","Naveen","Shreya","Varun","Monika","Ashok","Kavita","Manoj","Ritu"
]

genders = ["Boy","Girl"]

def get_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

data = []

for student in students:
    gender = random.choice(genders)
    
    base = random.randint(60, 90)  # starting level
    
    for sem in range(1, 9):
        year = 2023 + (sem-1)//2
        
        # fluctuate marks
        marks = [base + random.randint(-10, 10) for _ in range(6)]
        marks = [max(40, min(100, m)) for m in marks]
        
        total = sum(marks)
        avg = round(total / 6, 2)
        grade = get_grade(avg)
        
        row = [student, gender, year, sem] + marks + [total, avg, grade]
        data.append(row)

columns = [
"Name","Gender","Year","Semester",
"Subject1","Subject2","Subject3",
"Subject4","Subject5","Subject6",
"Total","Average","Grade"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("student_semester_data.csv", index=False)

print("✅ Dataset generated: student_semester_data.csv")