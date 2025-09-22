import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📚 Student Marks Analyzer & Grade Calculator")

uploaded_file = st.file_uploader("Upload CSV file with student marks", type=["csv"])

def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 75:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 40:
        return "C"
    else:
        return "F"

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Calculate total and average
    subjects = df.columns[1:]  # Assuming first column is Name
    df["Total"] = df[subjects].sum(axis=1)
    df["Average"] = df["Total"] / len(subjects)
    df["Grade"] = df["Average"].apply(calculate_grade)

    st.subheader("📊 Calculated Results")
    st.dataframe(df)

    # Top 5 students chart
    st.subheader("🏆 Top 5 Performers")
    top_students = df.sort_values(by="Average", ascending=False).head(5)
    fig, ax = plt.subplots()
    ax.bar(top_students["Name"], top_students["Average"])
    ax.set_ylabel("Average Marks")
    ax.set_title("Top 5 Students")
    st.pyplot(fig)

    # Grade distribution chart
    st.subheader("📈 Grade Distribution")
    grade_counts = df["Grade"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%')
    ax2.set_title("Grade Distribution")
    st.pyplot(fig2)

else:
    st.info("Please upload a CSV file to analyze marks.")
