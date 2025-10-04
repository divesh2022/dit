import pyodbc
import pandas as pd
import streamlit as st

# Database connection
def get_connection():
    try:
        connection_string = (
            "DRIVER={SQL Server};"
            "SERVER=localhost\\SQLEXPRESS;"
            "DATABASE=smss;"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        st.error(f"❌ Connection failed: {e}")
        return None

# Query executor
def run_query(query):
    try:
        conn = get_connection()
        if conn is None:
            return pd.DataFrame()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if not data:
            st.warning("Query returned no rows.")
            return pd.DataFrame()
        columns = [col[0] for col in cursor.description]
        if len(data[0]) != len(columns):
            st.error(f"Mismatch: {len(data[0])} columns in data vs {len(columns)} column headers.")
            return pd.DataFrame()
        conn.close()
        return pd.DataFrame(data, columns=columns)
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()


# Streamlit UI
st.set_page_config(page_title="CSE Branch Viewer", layout="wide")
st.title("📊 CSE Branch Database Viewer")

tables = [
    "Student", "Faculty", "FacultySubjects", "FacultyEducation", "FacultyResearchArea",
    "HOD", "HODCommunication", "Course", "Assignment", "CourseSchedule", "StudentSchedule",
    "Attendance", "Grade", "Submission", "Message", "Parent", "TeachingMaterial",
    "StudentAssessment", "Test", "TestResult", "Lecture", "CourseCompletion",
    "DiscussionBoard", "NotificationPreference", "AssignmentAITrainingData"
]

selected_table = st.selectbox("Select a table to view:", tables)

# Query builder with corrected column names
if selected_table == "Student":
    query = "SELECT * FROM Student WHERE branch = 'CSE';"
elif selected_table == "Faculty":
    query = "SELECT * FROM Faculty WHERE department = 'CSE';"
elif selected_table == "HOD":
    query = "SELECT * FROM HOD WHERE department = 'CSE';"
elif selected_table == "Course":
    query = "SELECT * FROM Course WHERE department = 'CSE';"
elif selected_table == "CourseSchedule":
    query = """
        SELECT * FROM CourseSchedule 
        WHERE course_id IN (SELECT course_id FROM Course WHERE department = 'CSE');
    """
elif selected_table == "StudentSchedule":
    query = """
        SELECT * FROM StudentSchedule 
        WHERE student_id IN (SELECT student_id FROM Student WHERE branch = 'CSE');
    """
elif selected_table == "Assignment":
    query = """
        SELECT * FROM Assignment 
        WHERE course_id IN (SELECT course_id FROM Course WHERE department = 'CSE');
    """
elif selected_table == "Submission":
    query = """
        SELECT * FROM Submission 
        WHERE student_id IN (SELECT student_id FROM Student WHERE branch = 'CSE');
    """
elif selected_table == "Grade":
    query = """
        SELECT * FROM Grade 
        WHERE student_id IN (SELECT student_id FROM Student WHERE branch = 'CSE');
    """
elif selected_table == "Test":
    query = """
        SELECT * FROM Test 
        WHERE course_id IN (SELECT course_id FROM Course WHERE department = 'CSE');
    """
elif selected_table == "TestResult":
    query = """
        SELECT * FROM TestResult 
        WHERE student_id IN (SELECT student_id FROM Student WHERE branch = 'CSE');
    """
elif selected_table == "Lecture":
    query = """
        SELECT * FROM Lecture 
        WHERE course_id IN (SELECT course_id FROM Course WHERE department = 'CSE');
    """
elif selected_table == "CourseCompletion":
    query = """
        SELECT * FROM CourseCompletion 
        WHERE student_id IN (SELECT student_id FROM Student WHERE branch = 'CSE');
    """
elif selected_table == "DiscussionBoard":
    query = """
        SELECT * FROM DiscussionBoard 
        WHERE course_id IN (SELECT course_id FROM Course WHERE department = 'CSE');
    """
elif selected_table == "TeachingMaterial":
    query = """
        SELECT * FROM TeachingMaterial 
        WHERE course_id IN (SELECT course_id FROM Course WHERE department = 'CSE');
    """
elif selected_table == "AssignmentAITrainingData":
    query = """
        SELECT * FROM AssignmentAITrainingData 
        WHERE student_id IN (SELECT student_id FROM Student WHERE branch = 'CSE');
    """
else:
    query = f"SELECT * FROM {selected_table};"

# Display results
df = run_query(query)
if not df.empty:
    st.subheader(f"Showing data from: {selected_table}")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data found or query failed.")
