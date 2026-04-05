import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Student Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")

# ------------------ FILE UPLOAD ------------------
st.sidebar.header("📂 Upload Data")

uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("student_grades.csv")

# ------------------ CLEANING ------------------
df.columns = df.columns.str.strip().str.lower()

# ------------------ DATA PREVIEW ------------------
with st.expander("📋 View Raw Data"):
    st.dataframe(df)

# ------------------ SIDEBAR FILTER ------------------
st.sidebar.header("🎯 Filters")
student = st.sidebar.selectbox("Select Student", df['name'].unique())
gender = st.sidebar.selectbox("Select Gender", df['gender'].unique())

filtered = df[(df['name'] == student) & (df['gender'] == gender)]

if filtered.empty:
    st.warning("No data for selected student & gender")
    st.stop()

# ------------------ KPI CARDS ------------------
st.subheader("📊 Key Performance")

col1, col2, col3 = st.columns(3)

total = int(filtered['total'].values[0])
percentage = float(filtered['average'].values[0])
grade = filtered['grade'].values[0]

col1.metric("📌 Total Marks", total)
col2.metric("📈 Percentage", f"{percentage}%")
col3.metric("🏆 Grade", grade)

# ------------------ STUDENT RANK ------------------
st.subheader("🏅 Student Rank")

df['rank'] = df['average'].rank(ascending=False)

student_rank = int(df[df['name'] == student]['rank'].values[0])

st.markdown(f"""
<h1 style='text-align: center; color: yellow; font-size: 60px;'>
    #{student_rank}
</h1>
<p style='text-align: center; font-size:20px; color: grey;'>
    {student} in class ranking
</p>
""", unsafe_allow_html=True)

# ------------------ GENDER COMPARISON ------------------
st.subheader("📊 Gender Comparison")

colA, colB = st.columns(2)

male_avg = df[df['gender'] == 'Boy']['average'].mean()
female_avg = df[df['gender'] == 'Girl']['average'].mean()

colA.metric("👦 Boys Avg", round(male_avg, 2))
colB.metric("👧 Girls Avg", round(female_avg, 2))

# ------------------ STUDENT VS CLASS AVG ------------------
st.subheader("📊 Student vs Class Average")

col1, col2 = st.columns(2)

student_avg = float(filtered['average'].values[0])
class_avg = df['average'].mean()

col1.metric("🎯 Selected Student Avg", round(student_avg, 2))
col2.metric("🏫 Class Average", round(class_avg, 2))

# ------------------ PERFORMANCE STATUS ------------------
st.subheader("📌 Performance Status")

if student_avg > class_avg:
    st.success("🎉 This student is ABOVE class average")
else:
    st.warning("⚠️ This student is BELOW class average")

# ------------------ SUBJECT COLUMNS ------------------
subjects = df.columns[1:4]   # auto-detect subjects

# ------------------ BAR CHART ------------------
st.subheader("📊 Subject-wise Marks")

student_marks = filtered[subjects].values.flatten()

fig1, ax1 = plt.subplots(figsize=(5,3))
sns.barplot(x=subjects, y=student_marks, ax=ax1)
ax1.set_xlabel("Subjects")
ax1.set_ylabel("Marks")
plt.tight_layout()
st.pyplot(fig1, use_container_width=False)

# ------------------ LINE CHART ------------------
st.subheader("📈 Performance")

fig2, ax2 = plt.subplots(figsize=(5,3))
sns.lineplot(x=subjects, y=student_marks, marker='o', ax=ax2)
ax2.set_xlabel("Subjects")
ax2.set_ylabel("Marks")
plt.tight_layout()
st.pyplot(fig2, use_container_width=False)

# ------------------ SUBJECT CONTRIBUTION PIE ------------------
st.subheader("📊 Subject Contribution")

fig, ax = plt.subplots(figsize=(4,4))

ax.pie(
    student_marks,
    labels=subjects,
    autopct='%1.1f%%',
    startangle=90
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

class_avg_subjects = df[subjects].mean()

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

# ------------------ TOPPER ------------------
st.subheader("🏆 Class Topper")

topper = df.loc[df['average'].idxmax()]

st.success(f"Topper: {topper['name']} with {topper['average']}%")

# ------------------ SUBJECT TOPPER ------------------
st.subheader("📚 Subject-wise Toppers")

for sub in subjects:
    topper = df.loc[df[sub].idxmax()]
    st.write(f"🏆 {sub}: {topper['name']} ({topper[sub]} marks)")

# ------------------ TOPPER BY GENDER ------------------
st.subheader("🏆 Topper by Gender")

col1, col2 = st.columns(2)

# 👦 Male topper
male_df = df[df['gender'] == 'Boy']
male_topper = male_df.loc[male_df['average'].idxmax()]

# 👧 Female topper
female_df = df[df['gender'] == 'Girl']
female_topper = female_df.loc[female_df['average'].idxmax()]

with col1:
    st.success(f"👦 Male Topper: {male_topper['name']} ({male_topper['average']}%)")

with col2:
    st.success(f"👧 Female Topper: {female_topper['name']} ({female_topper['average']}%)")

# ------------------ DISTRIBUTION ------------------
st.subheader("📉 Class Performance Distribution")

fig3, ax3 = plt.subplots(figsize=(5,3))
sns.histplot(df['average'], kde=True, ax=ax3)
plt.tight_layout()
st.pyplot(fig3, use_container_width=False)

# ------------------ GRADE COUNT ------------------
st.subheader("📊 Grade Distribution")

fig4, ax4 = plt.subplots(figsize=(5,3))
sns.countplot(x='grade', data=df, ax=ax4)
plt.tight_layout()
st.pyplot(fig4, use_container_width=False)

# ------------------ GENDER RATIO PIE ------------------
st.subheader("📊 Gender Ratio")

fig6, ax6 = plt.subplots(figsize=(4,4))

gender_counts = df['gender'].value_counts()

ax6.pie(
    gender_counts,
    labels=gender_counts.index,
    autopct='%1.1f%%',
    startangle=90
)

ax6.set_title("Distribution of Boys and Girls")
plt.tight_layout()
st.pyplot(fig6, use_container_width=False)

# ------------------ GENDER ANALYSIS ------------------
st.subheader("👦👧 Average Performance by Gender")

fig5, ax5 = plt.subplots(figsize=(5,3))

avg_marks = df.groupby('gender')['average'].mean().reset_index()

sns.barplot(x='gender', y='average', data=avg_marks, ax=ax5)

ax5.set_xlabel("Gender")
ax5.set_ylabel("Average Marks")
ax5.set_title("Average Performance of Boys vs Girls")

plt.tight_layout()
st.pyplot(fig5, use_container_width=False)
