import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import uuid
import hashlib
from datetime import datetime
import json
import os
 
# JSON file paths
STUDENTS_FILE = 'students.json'
USERS_FILE = 'users.json'
LOGS_FILE = 'logs.json'
 
# ----- Data Management Functions -----
def load_data(file_path):
    """Load data from JSON file, return empty dict if file doesn't exist"""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}
 
def save_data(data, file_path):
    """Save data to JSON file"""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
 
def load_students():
    """Load student data"""
    return load_data(STUDENTS_FILE)
 
def save_students(students):
    """Save student data"""
    save_data(students, STUDENTS_FILE)
 
def load_users():
    """Load user data"""
    return load_data(USERS_FILE)
 
def save_users(users):
    """Save user data"""
    save_data(users, USERS_FILE)
 
def load_logs():
    """Load activity logs"""
    return load_data(LOGS_FILE)
 
def save_logs(logs):
    """Save activity logs"""
    save_data(logs, LOGS_FILE)
 
# ----- Password Management -----
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()
 
# ----- Initialize Data -----
def initialize_data():
    """Initialize data files with default values if they don't exist"""
    # Initialize students data
    if not os.path.exists(STUDENTS_FILE):
        default_students = [
            {"id": "S001", "name": "Alice Johnson", "age": 20, "course": "Computer Science",
             "math": 85, "science": 92, "history": 78, "english": 88,
             "parent_name": "John Johnson", "parent_phone": "123-456-7890"},
            {"id": "S002", "name": "Bob Smith", "age": 21, "course": "Mechanical",
             "math": 72, "science": 68, "history": 85, "english": 79,
             "parent_name": "Mary Smith", "parent_phone": "234-567-8901"},
            {"id": "S003", "name": "Charlie Brown", "age": 22, "course": "Electrical",
             "math": 91, "science": 94, "history": 89, "english": 93,
             "parent_name": "Tom Brown", "parent_phone": "345-678-9012"},
            {"id": "S004", "name": "Diana Prince", "age": 20, "course": "Civil",
             "math": 65, "science": 70, "history": 75, "english": 68,
             "parent_name": "Bruce Prince", "parent_phone": "456-789-0123"},
            {"id": "S005", "name": "Ethan Hunt", "age": 23, "course": "Computer Science",
             "math": 78, "science": 82, "history": 77, "english": 85,
             "parent_name": "Ethan Hunt Sr.", "parent_phone": "567-890-1234"}
        ]
        save_students(default_students)
   
    # Initialize users data
    if not os.path.exists(USERS_FILE):
        default_users = {
            # Teachers
            "T001": {"name": "Sarah Jones", "password": hash_password("teacher123"), "type": "teacher"},
            "T002": {"name": "Michael Brown", "password": hash_password("teacher456"), "type": "teacher"},
           
            # Students
            "S001": {"name": "Alice Johnson", "password": hash_password("alice123"), "type": "student"},
            "S002": {"name": "Bob Smith", "password": hash_password("bob123"), "type": "student"},
            "S003": {"name": "Charlie Brown", "password": hash_password("charlie123"), "type": "student"},
            "S004": {"name": "Diana Prince", "password": hash_password("diana123"), "type": "student"},
            "S005": {"name": "Ethan Hunt", "password": hash_password("ethan123"), "type": "student"}
        }
        save_users(default_users)
   
    # Initialize logs data
    if not os.path.exists(LOGS_FILE):
        save_logs([])
 
# ----- Helper Functions -----
def log_activity(user_id, activity):
    """Log user activity with timestamp"""
    logs = load_logs()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.append({
        "timestamp": timestamp,
        "user_id": user_id,
        "activity": activity
    })
    save_logs(logs)
 
def calculate_gpa(student):
    """Calculate GPA and percentage from marks"""
    subjects = ['math', 'science', 'history', 'english']
    total_marks = sum(student[subject] for subject in subjects)
    percentage = total_marks / (len(subjects) * 100) * 100
   
    # 4.0 GPA scale conversion
    if percentage >= 90:
        gpa = 4.0
    elif percentage >= 80:
        gpa = 3.0 + (percentage - 80) / 10
    elif percentage >= 70:
        gpa = 2.0 + (percentage - 70) / 10
    elif percentage >= 60:
        gpa = 1.0 + (percentage - 60) / 10
    else:
        gpa = 0.0 + percentage / 60
       
    return round(gpa, 2), round(percentage, 2)
 
def get_grade(percentage):
    """Convert percentage to letter grade"""
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"
 
# ----- Page Functions -----
def class_report():
    st.title("📊 Class Performance Report")
   
    students = load_students()
    students_with_gpa = []
    for student in students:
        gpa, percentage = calculate_gpa(student)
        grade = get_grade(percentage)
        students_with_gpa.append({
            **student,
            "gpa": gpa,
            "percentage": percentage,
            "grade": grade
        })
   
    df = pd.DataFrame(students_with_gpa)
   
    # Show general statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Class Average GPA", f"{df['gpa'].mean():.2f}")
    with col3:
        st.metric("Pass Rate", f"{(df['percentage'] >= 60).mean() * 100:.1f}%")
   
    # Top 3 students
    st.subheader("🏆 Top Performing Students")
    top_students = df.sort_values(by="percentage", ascending=False).head(3)
    st.table(top_students[["id", "name", "percentage", "gpa", "grade"]])
   
    # Grade distribution
    st.subheader("📈 Grade Distribution")
    grade_counts = df['grade'].value_counts().sort_index(ascending=False)
   
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.barh(grade_counts.index, grade_counts.values, color=['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336'])
    ax.set_xlabel('Number of Students')
    ax.set_ylabel('Grade')
    ax.set_title('Grade Distribution')
   
    # Add count labels to bars
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, f"{width}",
                ha='left', va='center')
   
    st.pyplot(fig)
   
    # Subject-wise performance
    st.subheader("📊 Subject Performance Analysis")
    subject = st.selectbox("Select Subject", ["math", "science", "history", "english"])
   
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sorted_df = df.sort_values(by=subject, ascending=False)
    bars = ax2.bar(sorted_df["name"], sorted_df[subject], color='skyblue')
    ax2.set_ylabel("Marks", fontsize=12)
    ax2.set_xlabel("Students", fontsize=12)
    ax2.set_title(f"{subject.capitalize()} Marks", fontsize=14)
    plt.axhline(y=sorted_df[subject].mean(), color='r', linestyle='-', label=f'Average: {sorted_df[subject].mean():.1f}')
    plt.legend()
   
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height}',
                ha='center', va='bottom', fontsize=10)
   
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()
    st.pyplot(fig2)
   
    # Full student data
    with st.expander("View Full Student Data"):
        st.dataframe(df.sort_values(by="percentage", ascending=False), use_container_width=True)
 
def manage_marks():
    st.title("✏️ Manage Student Marks")
   
    students = load_students()
    # Create a DataFrame for marks editing
    df = pd.DataFrame(students)
    subjects = ["math", "science", "history", "english"]
    marks_df = df[["id", "name"] + subjects]
   
    st.write("Edit marks directly in the table below:")
    edited_df = st.data_editor(
        marks_df,
        num_rows="fixed",
        use_container_width=True,
        column_config={
            "id": st.column_config.TextColumn("Student ID", disabled=True),
            "name": st.column_config.TextColumn("Student Name", disabled=True),
            "math": st.column_config.NumberColumn("Mathematics", min_value=0, max_value=100),
            "science": st.column_config.NumberColumn("Science", min_value=0, max_value=100),
            "history": st.column_config.NumberColumn("History", min_value=0, max_value=100),
            "english": st.column_config.NumberColumn("English", min_value=0, max_value=100),
        },
        hide_index=True
    )
   
    if st.button("Save Marks Changes", type="primary"):
        updated_students = students.copy()
        for _, row in edited_df.iterrows():
            student_id = row['id']
            for student in updated_students:
                if student['id'] == student_id:
                    for subject in subjects:
                        if student[subject] != row[subject]:
                            student[subject] = row[subject]
                            log_activity(
                                st.session_state.current_user,
                                f"Updated {subject} mark for {student['name']} (ID: {student_id}) to {row[subject]}"
                            )
        save_students(updated_students)
        st.success("Marks updated successfully!")
   
    # Show current GPA and grades based on marks
    st.subheader("Current Performance Metrics")
   
    perf_data = []
    for student in students:
        gpa, percentage = calculate_gpa(student)
        grade = get_grade(percentage)
        perf_data.append({
            "id": student["id"],
            "name": student["name"],
            "percentage": percentage,
            "gpa": gpa,
            "grade": grade
        })
   
    perf_df = pd.DataFrame(perf_data)
    st.dataframe(
        perf_df,
        use_container_width=True,
        column_config={
            "id": st.column_config.TextColumn("Student ID"),
            "name": st.column_config.TextColumn("Student Name"),
            "percentage": st.column_config.ProgressColumn("Percentage", format="%d%%", min_value=0, max_value=100),
            "gpa": st.column_config.NumberColumn("GPA (4.0 Scale)", format="%.2f"),
            "grade": st.column_config.TextColumn("Letter Grade"),
        },
        hide_index=True
    )
 
def manage_students():
    st.title("👨‍🎓 Manage Students")
   
    tab1, tab2, tab3 = st.tabs(["Student Details", "Add New Student", "Remove Student"])
    students = load_students()
    users = load_users()
   
    with tab1:
        st.subheader("✏️ Student Bio Data")
        if len(students) > 0:
            df = pd.DataFrame(students)
            student_details = df[["id", "name", "age", "course", "parent_name", "parent_phone"]]
            updated_details = st.data_editor(
                student_details,
                num_rows="fixed",
                use_container_width=True,
                column_config={
                    "id": st.column_config.TextColumn("Student ID", disabled=True),
                    "name": st.column_config.TextColumn("Full Name"),
                    "age": st.column_config.NumberColumn("Age", min_value=15, max_value=100),
                    "course": st.column_config.TextColumn("Course/Major"),
                    "parent_name": st.column_config.TextColumn("Parent's Name"),
                    "parent_phone": st.column_config.TextColumn("Parent's Contact"),
                },
                hide_index=True
            )
 
            if st.button("Save Student Details", type="primary"):
                updated_students = students.copy()
                updated_users = users.copy()
               
                for _, row in updated_details.iterrows():
                    student_id = row['id']
                    for student in updated_students:
                        if student['id'] == student_id:
                            student['name'] = row['name']
                            student['age'] = row['age']
                            student['course'] = row['course']
                            student['parent_name'] = row['parent_name']
                            student['parent_phone'] = row['parent_phone']
                           
                            # Update corresponding user entry if it exists
                            if student_id in updated_users:
                                updated_users[student_id]["name"] = row['name']
                           
                            log_activity(
                                st.session_state.current_user,
                                f"Updated details for student {row['name']} (ID: {student_id})"
                            )
               
                save_students(updated_students)
                save_users(updated_users)
                st.success("Student details updated successfully!")
   
    with tab2:
        st.subheader("➕ Add New Student")
        with st.form(key="add_student_form"):
            col1, col2 = st.columns(2)
            with col1:
                student_id = st.text_input("Student ID", placeholder="e.g., S006")
                name = st.text_input("Full Name", placeholder="e.g., John Doe")
                age = st.number_input("Age", min_value=15, max_value=100, value=18)
                course = st.text_input("Course/Major", placeholder="e.g., Computer Science")
            with col2:
                parent_name = st.text_input("Parent's Name", placeholder="e.g., Jane Doe")
                parent_phone = st.text_input("Parent's Phone", placeholder="e.g., 123-456-7890")
                password = st.text_input("Initial Password", type="password",
                                       help="Password for student login")
                confirm_password = st.text_input("Confirm Password", type="password")
               
            submit_button = st.form_submit_button("Add Student", type="primary")
           
            if submit_button:
                if not student_id or not name or not course or not parent_name or not parent_phone or not password:
                    st.error("Please fill all the required fields!")
                elif password != confirm_password:
                    st.error("Passwords do not match!")
                elif student_id in [s["id"] for s in students]:
                    st.error(f"Student ID {student_id} already exists!")
                else:
                    # Add student to students list
                    updated_students = students.copy()
                    updated_students.append({
                        "id": student_id,
                        "name": name,
                        "age": age,
                        "course": course,
                        "math": 0,
                        "science": 0,
                        "history": 0,
                        "english": 0,
                        "parent_name": parent_name,
                        "parent_phone": parent_phone
                    })
                   
                    # Add student to users for login
                    updated_users = users.copy()
                    updated_users[student_id] = {
                        "name": name,
                        "password": hash_password(password),
                        "type": "student"
                    }
                   
                    save_students(updated_students)
                    save_users(updated_users)
                   
                    log_activity(
                        st.session_state.current_user,
                        f"Added new student {name} (ID: {student_id})"
                    )
                    st.success(f"Student {name} added successfully!")
   
    with tab3:
        st.subheader("➖ Remove Student")
        if len(students) > 0:
            student_list = [f"{s['id']} - {s['name']}" for s in students]
            selected_student = st.selectbox("Select Student to Remove", student_list)
            selected_id = selected_student.split(" - ")[0] if selected_student else None
           
            if selected_id and st.button("Remove Student", type="primary"):
                # Find student name before removal
                student_name = next((s['name'] for s in students if s['id'] == selected_id), "")
               
                # Remove from students list
                updated_students = [s for s in students if s["id"] != selected_id]
               
                # Remove from users if exists
                updated_users = users.copy()
                if selected_id in updated_users:
                    del updated_users[selected_id]
               
                save_students(updated_students)
                save_users(updated_users)
               
                log_activity(
                    st.session_state.current_user,
                    f"Removed student {student_name} (ID: {selected_id})"
                )
                st.success(f"Student {student_name} (ID: {selected_id}) removed successfully!")
        else:
            st.info("No students to remove.")
 
def account_settings():
    st.title("🔒 Account Settings")
   
    user_id = st.session_state.current_user
    users = load_users()
    user_data = users.get(user_id, {})
   
    st.subheader("Change Password")
    with st.form(key="change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
       
        submit_button = st.form_submit_button("Change Password", type="primary")
       
        if submit_button:
            if not current_password or not new_password or not confirm_password:
                st.error("Please fill all the fields!")
            elif hash_password(current_password) != user_data.get("password"):
                st.error("Current password is incorrect!")
            elif new_password != confirm_password:
                st.error("New passwords do not match!")
            elif len(new_password) < 6:
                st.error("Password should be at least 6 characters long!")
            else:
                updated_users = users.copy()
                updated_users[user_id]["password"] = hash_password(new_password)
                save_users(updated_users)
                log_activity(user_id, "Changed password")
                st.success("Password changed successfully!")
   
    st.subheader("Recent Activities")
    logs = load_logs()
    user_logs = [log for log in logs if log["user_id"] == user_id]
   
    if user_logs:
        logs_df = pd.DataFrame(user_logs[-10:])  # Show only the 10 most recent logs
        st.dataframe(logs_df, use_container_width=True, hide_index=True)
    else:
        st.info("No recent activities.")
 
def student_dashboard(student_id):
    students = load_students()
    student = next((s for s in students if s["id"] == student_id), None)
   
    if not student:
        st.error("Student data not found!")
        return
   
    st.title(f"📚 Welcome, {student['name']}!")
 
    # Sidebar for Change Password  
    st.sidebar.header("🔑 Change Password")
    with st.sidebar.form(key="password_change_form"):
        current_pwd = st.text_input("Current Password", type="password")
        new_pwd = st.text_input("New Password", type="password")
        confirm_pwd = st.text_input("Confirm New Password", type="password")
        submit = st.form_submit_button("Change Password")
 
        if submit:
            users = load_users()
            if not current_pwd or not new_pwd or not confirm_pwd:
                st.sidebar.error("Please fill all fields.")
            elif hash_password(current_pwd) != users[student_id]["password"]:
                st.sidebar.error("Incorrect current password.")
            elif new_pwd != confirm_pwd:
                st.sidebar.error("New passwords do not match.")
            else:
                updated_users = users.copy()
                updated_users[student_id]["password"] = hash_password(new_pwd)
                save_users(updated_users)
                log_activity(student_id, "Changed password")
                st.sidebar.success("Password changed successfully!")
 
    # GPA, Percentage, Grade
    gpa, percentage = calculate_gpa(student)
    grade = get_grade(percentage)
 
    st.subheader("📈 Academic Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("GPA", f"{gpa}/4.0")
    col2.metric("Percentage", f"{percentage}%")
    col3.metric("Grade", grade)
 
    # Performance Graph
    st.subheader("📊 Subject-wise Marks")
    subjects = ['math', 'science', 'history', 'english']
    subject_names = ['Mathematics', 'Science', 'History', 'English']
    marks = [student[subject] for subject in subjects]
 
    fig, ax = plt.subplots()
    ax.bar(subject_names, marks, color='skyblue')
    ax.set_ylabel('Marks')
    ax.set_ylim(0, 100)
    ax.set_title('Performance in Subjects')
    for i, v in enumerate(marks):
        ax.text(i, v + 2, str(v), ha='center', fontweight='bold')
    st.pyplot(fig)
 
    # Full Student Details
    st.subheader("👤 Student Details")
    details = {
        "Student ID": student["id"],
        "Name": student["name"],
        "Age": student["age"],
        "Course": student["course"],
        "Parent's Name": student["parent_name"],
        "Parent's Contact": student["parent_phone"]
    }
    st.table(pd.DataFrame(details.items(), columns=["Field", "Value"]))
 
    # Top 3 Students
    st.subheader("🏆 Top 3 Students")
    students_sorted = sorted(students,
                             key=lambda s: sum([s['math'], s['science'], s['history'], s['english']]),
                             reverse=True)
    top_3 = students_sorted[:3]
    df_top3 = pd.DataFrame([{
        "Rank": idx + 1,
        "Name": s["name"],
        "GPA": calculate_gpa(s)[0]
    } for idx, s in enumerate(top_3)])
    st.table(df_top3)
 
    # Student's Rank
    student_total = sum([student[subj] for subj in subjects])
    rank = 1
    for s in students_sorted:
        s_total = sum([s[subj] for subj in subjects])
        if s_total > student_total:
            rank += 1
    st.success(f"Your Class Rank: #{rank}")
 
# ----- Main App -----
def main():
    st.set_page_config(
        page_title="Student Tracking System",
        page_icon="🎓",
        layout="wide"
    )
   
    # Initialize data files
    initialize_data()
   
    # Check login status
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
   
    # Login screen
    if not st.session_state.logged_in:
        col1, col2 = st.columns([1, 1])
       
        with col1:
            st.title("🎓 STUDENT TRACKING SYSTEM")
            st.subheader("Login to continue")
           
            with st.form("login_form"):
                user_id = st.text_input("User ID", placeholder="Enter your ID")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
               
                if submitted:
                    users = load_users()
                    if not user_id or not password:
                        st.error("Please fill in all fields!")
                    elif user_id in users:
                        user = users[user_id]
                        if user["password"] == hash_password(password):
                            st.session_state.logged_in = True
                            st.session_state.current_user = user_id
                            log_activity(user_id, "Logged in")
                            st.balloons()
                            st.success(f"Login successful as {user['type'].capitalize()}!")
                            st.markdown(
                                """
                                <script>
                                    setTimeout(function() {
                                        window.location.reload();
                                    }, 1500);
                                </script>
                                """,
                                unsafe_allow_html=True
                            )
                        else:
                            st.error("Invalid password!")
                    else:
                        st.error("User ID not found!")
       
        with col2:
            st.image("https://via.placeholder.com/400x300.png?text=Student+Tracking+System", width=400)
            st.info("""
            👨‍🎓 For students: Use your student ID and password
           
            👩‍🏫 For teachers: Use your teacher ID and password
           
            Demo Accounts:
            - Teacher: T001 / teacher123
            - Student: S001 / alice123
            """)
   
    # Authenticated screens
    else:
        user_id = st.session_state.current_user
        users = load_users()
        user_data = users.get(user_id, {})
        user_type = user_data.get("type")
        user_name = user_data.get("name", "User")
       
        # Teacher Dashboard
        if user_type == "teacher":
            st.sidebar.title(f"Welcome, {user_name}")
            st.sidebar.write(f"ID: {user_id}")
           
            # Navigation
            page = st.sidebar.radio(
                "Navigation",
                ["Class Report", "Manage Marks", "Manage Students", "Account Settings"]
            )
           
            if page == "Class Report":
                class_report()
            elif page == "Manage Marks":    
                manage_marks()
            elif page == "Manage Students":
                manage_students()
            elif page == "Account Settings":
                account_settings()
               
            # Logout button
            if st.sidebar.button("Logout", type="primary"):
                log_activity(user_id, "Logged out")
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.experimental_rerun()
       
        # Student Dashboard
        elif user_type == "student":
            student_dashboard(user_id)
           
            # Logout button
            if st.sidebar.button("Logout", type="primary"):
                log_activity(user_id, "Logged out")
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.experimental_rerun()
       
        # Unknown user type
        else:
            st.error("Invalid user type!")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.experimental_rerun()
 
if __name__ == "__main__":
    main()
 