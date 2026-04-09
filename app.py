import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")

# ------------------ FILE UPLOAD ------------------
st.sidebar.header("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("student_semester_data.csv")

# ------------------ CLEANING ------------------
df.columns = df.columns.str.strip().str.lower()

# ------------------ DATA PREVIEW ------------------
with st.expander("📋 View Raw Data"):
    st.dataframe(df)

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("🎯 Filters")
student = st.sidebar.selectbox("Select Student", df['name'].unique())
gender = st.sidebar.selectbox("Select Gender", df['gender'].unique())
year = st.sidebar.selectbox("Select Year", [2023, 2024, 2025, 2026])
semester = st.sidebar.selectbox("Select Semester", [1,2,3,4,5,6,7,8])

filtered_df = df[
    (df['name'] == student) &
    (df['gender'] == gender) &
    (df['year'] == year) &
    (df['semester'] == semester)
]
class_df = df[
    (df['year'] == year) &
    (df['semester'] == semester)
]

if filtered_df.empty:
    st.warning("No data for selected student & gender")
    st.stop()

                                            #STUDENT PERFORMANCE
st.markdown("""
<h1 style='text-align: center; color: yellow;'>
  🧮 Student Performance
</h1>
""", unsafe_allow_html=True)

# ------------------ KPI CARDS ------------------
st.subheader("🎯 Performance Overview")

col1, col2, col3 = st.columns(3)

total = int(filtered_df['total'].values[0])
percentage = float(filtered_df['average'].values[0])
grade = filtered_df['grade'].values[0]

col1.metric("✔️ Total Marks", total)
col2.metric("✔️ Percentage", f"{percentage}%")
col3.metric("✔️ Grade", grade)

# ------------------ STUDENT RANK (SEMESTER-WISE) ------------------
st.subheader("🏅 Student Rank")

rank_df = df[
    (df['year'] == year) &
    (df['semester'] == semester)
]

rank_df = rank_df[['name', 'average']]

rank_df['rank'] = rank_df['average'].rank(ascending=False)

student_rank = int(rank_df[rank_df['name'] == student]['rank'].values[0])

st.markdown(f"""
<h1 style='text-align: center; color: yellow; font-size: 60px;'>
    #{student_rank}
</h1>
<p style='text-align: center; font-size:20px; color: grey;'>
    {student} in class ranking
</p>
""", unsafe_allow_html=True)

# ------------------ STUDENT VS CLASS AVG ------------------
st.subheader("📊 Student vs Class Average")

col1, col2 = st.columns(2)

student_avg = float(filtered_df['average'].values[0])
class_avg = df['average'].mean()

col1.metric("🤓 Selected Student Avg", round(student_avg, 2))
col2.metric("🏫 Class Average", round(class_avg, 2))

# ------------------ PERFORMANCE STATUS ------------------
st.subheader("📌 Performance Status")

if student_avg > class_avg:
    st.success("🎉 This student is ABOVE class average")
else:
    st.warning("⚠️ This student is BELOW class average")

# ------------------ SUBJECT COLUMNS ------------------
subjects = df.columns[4:10]   # auto-detect subjects

# ------------------ BAR CHART ------------------
st.subheader("📊 Subject-wise Marks")

filtered = filtered_df.iloc[0]
student_marks = filtered[subjects].values

fig1, ax1 = plt.subplots(figsize=(5,3))
colors = ['#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#ff7f0e', '#17becf']
sns.barplot(
    x=list(subjects),
    y=list(student_marks),
    palette=colors,
    ax=ax1
)
#for i, bar in enumerate(ax1.patches):
#    bar.set_edgecolor('black')
#    bar.set_linewidth(0.5)

ax1.set_xlabel("Subjects")
ax1.set_ylabel("Marks")
ax1.set_ylim(0, 80)
plt.tight_layout()
st.pyplot(fig1, use_container_width=False)

# ------------------ LINE CHART ------------------
st.subheader("📈 Performance")

fig2, ax2 = plt.subplots(figsize=(5,3))
sns.lineplot(x=list(subjects), y=list(student_marks), marker='o',ax=ax2)
ax2.set_xlabel("Subjects")
ax2.set_ylabel("Marks")
#ax2.set_ylim(0, 100)
plt.tight_layout()
st.pyplot(fig2, use_container_width=False)

# ------------------ AREA CHART ------------------
st.subheader("📈 Performance Over Time (Area Chart)")

student_all = df[df['name'] == student].sort_values(by='semester')

figA, axA = plt.subplots(figsize=(6,4))

axA.fill_between(
    student_all['semester'],
    student_all['average'],
    color='#4CAF50',
    alpha=0.5
)

axA.plot(
    student_all['semester'],
    student_all['average'],
    color='#2E7D32',
    marker='o'
)

axA.set_xlabel("Semester")
axA.set_ylabel("Average Marks")
axA.set_title("Performance Across Semesters")
axA.set_ylim(0, 100)

plt.tight_layout()
st.pyplot(figA)

# ------------------ SEMESTER TREND ------------------
st.subheader("📈 Performance Over Time")

student_all = df[df['name'] == student]

fig, ax = plt.subplots(figsize=(6,4))

sns.lineplot(
    x=student_all['semester'],
    y=student_all['average'],
    marker='o',
    ax=ax
)

ax.set_xlabel("Semester")
ax.set_ylabel("Average Marks")
ax.set_title("Performance Across Semesters")

st.pyplot(fig)

# ------------------ SUBJECT CONTRIBUTION PIE ------------------
st.subheader("📊 Subject Contribution")

fig, ax = plt.subplots(figsize=(4,4))

ax.pie(
    student_marks,
    labels=subjects,
    autopct='%1.1f%%',
    startangle=90,
)

ax.set_title("Marks Contribution by Subject")

st.pyplot(fig, use_container_width=False)

# ------------------ WEAKEST/STRONGEST SUBJECT ------------------

with col1:
    st.subheader("⚠️ Weakest Subject")
    weak_subject = subjects[student_marks.argmin()]
    weak_marks = student_marks.min()
    st.warning(f"{weak_subject} ({weak_marks} marks)")

with col2:
    st.subheader("💪 Strongest Subject")
    strong_subject = subjects[student_marks.argmax()]
    strong_marks = student_marks.max()
    st.success(f"{strong_subject} ({strong_marks} marks)")

# ------------------ SUBJECT COMPARISON ------------------
st.subheader("📊 Subject Comparison (Student vs Class)")

fig, ax = plt.subplots(figsize=(6,4))

class_avg_subjects = class_df[subjects].mean()

x = range(len(subjects))

ax.bar(x, student_marks, width=0.4, label="Student", align='center')
ax.bar([i + 0.4 for i in x], class_avg_subjects, width=0.4, label="Class Avg")

ax.set_xticks([i + 0.2 for i in x])
ax.set_xticklabels(subjects)

ax.set_xlabel("Subjects")
ax.set_ylabel("Marks")
ax.set_title("Student vs Class Performance")
ax.legend()

st.pyplot(fig)

                                            #TOPPERS
st.markdown("""
<h1 style='text-align: center; color: yellow;'>
🏆 Top Performers
</h1>
""", unsafe_allow_html=True)

# ------------------ TOPPER ------------------
st.subheader("🏅 Class Topper")

class_df = df[(df['year'] == year) & (df['semester'] == semester)]
topper = class_df.loc[class_df['average'].idxmax()]

st.markdown(f"""
<div style="
    background: #1f2937;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 30px;
    font-weight: bold;
">
 Class Topper: {topper['name']} <br>
 {round(topper['average'],2)}%
</div>
""", unsafe_allow_html=True)

# ------------------ SUBJECT TOPPER ------------------
st.subheader("📚 Subject-wise Toppers")

cols = st.columns(3)

for i, subject in enumerate(subjects):
    top_student = class_df.loc[class_df[subject].idxmax()]
    
    cols[i % 3].markdown(f"""
    <div style="
        background: #1f2937;
        padding: 15px;
        border-radius: 10px;
        margin-bottom:10px;
        text-align:center;
        color:white;
    ">
     <b style="color:white" >{subject.upper()}</b><br>
    {top_student['name']}<br>

    <span style="color:#4CAF50">{top_student[subject]} marks</span>
    </div>
    """, unsafe_allow_html=True)

# ------------------ TOPPER BY GENDER ------------------
st.subheader("🤓 Topper by Gender")

col1, col2 = st.columns(2)

male_df = class_df[class_df['gender'] == 'Boy']
female_df = class_df[class_df['gender'] == 'Girl']

#with col1:
#    if not male_df.empty:
male_topper = male_df.loc[male_df['average'].idxmax()]
#        st.success(f"👦 Male Topper: {male_topper['name']} ({male_topper['average']}%)")
#    else:
#        st.warning("No male students in this selection")

#with col2:
#    if not female_df.empty:
female_topper = female_df.loc[female_df['average'].idxmax()]
#        st.success(f"👧 Female Topper: {female_topper['name']} ({female_topper['average']}%)")
#    else:
#        st.warning("No female students in this selection")


col1.markdown(f"""
<div style="
    background: #1f2937;
    padding: 20px;
    border-radius: 12px;
    text-align:center;
    color:white;
">
🚹 Male Topper<br>
<b>{male_topper['name']}</b><br>
{round(male_topper['average'],2)}%
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="
    background: #1f2937;
    padding: 20px;
    border-radius: 12px;
    text-align:center;
    color:white;
">
🚺 Female Topper<br>
<b>{female_topper['name']}</b><br>
{round(female_topper['average'],2)}%
</div>
""", unsafe_allow_html=True)

                                            #CLASS PERFORMANCE
st.markdown("""
<h1 style='text-align: center; color: yellow;'>
  🏫 Class Performance
</h1>
""", unsafe_allow_html=True)

# ------------------ DISTRIBUTION ------------------
st.subheader("📉 Class Performance Distribution")

fig3, ax3 = plt.subplots(figsize=(5,3))
sns.histplot(class_df['average'], bins=10, kde=True, ax=ax3)
plt.tight_layout()
st.pyplot(fig3, use_container_width=False)

# ------------------ GRADE COUNT ------------------
st.subheader("📊 Class Grade Distribution")

fig4, ax4 = plt.subplots(figsize=(5,3))
colors= ['#yellow']
sns.countplot(x='grade', data=class_df, ax=ax4, palette="coolwarm")
plt.tight_layout()
st.pyplot(fig4, use_container_width=False)

                                            #GENDER ANALYSIS
st.markdown("""
<h1 style='text-align: center; color: yellow;'>
  👧👦 Gender Analysis
</h1>
""", unsafe_allow_html=True)

# ------------------ GENDER RATIO PIE ------------------
st.subheader("📊 Gender Ratio")

gender_counts = class_df['gender'].value_counts()

fig6, ax6 = plt.subplots(figsize=(3,3))

ax6.pie(gender_counts, 
        labels=gender_counts.index, 
        autopct='%1.1f%%', 
        pctdistance=0.75,
        wedgeprops={'width':0.4}
)

ax6.set_title("Gender Ratio")
plt.tight_layout()
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.pyplot(fig6)

# ------------------ GENDER COMPARISON ------------------
st.subheader("📊 Gender Comparison")

avg_marks = class_df.groupby('gender')['average'].mean().reset_index()

colA, colB = st.columns(2)

boy_avg = avg_marks[avg_marks['gender']=='Boy']['average']
girl_avg = avg_marks[avg_marks['gender']=='Girl']['average']

colA.metric("👦 Boys Avg", round(float(boy_avg.values[0]), 2) if not boy_avg.empty else 0)
colB.metric("👧 Girls Avg", round(float(girl_avg.values[0]), 2) if not girl_avg.empty else 0)

# ------------------ GENDER ANALYSIS ------------------
st.subheader("👦👧 Average Performance by Gender")

fig5, ax5 = plt.subplots(figsize=(5,3))

#avg_marks = class_df.groupby('gender')['average'].mean()
#avg_marks = avg_marks.reindex(['Boy', 'Girl']).reset_index()

sns.barplot(x='gender', y='average', data=avg_marks, ax=ax5, palette="deep")

ax5.set_xlabel("Gender")
ax5.set_ylabel("Average Marks")
ax5.set_title("Average Performance of Boys vs Girls")
ax5.set_ylim(0, 100)

plt.tight_layout()
st.pyplot(fig5, use_container_width=False)