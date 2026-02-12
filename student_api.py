import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd
from datetime import datetime

# API Configuration
API_BASE_URL = st.secrets.get("API_URL", "http://localhost:8000/api/students/")

# Page Configuration
st.set_page_config(
    page_title="Student Management System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .student-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'refresh' not in st.session_state:
    st.session_state.refresh = 0

def get_all_students():
    """Fetch all students from API"""
    try:
        response = requests.get(API_BASE_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            st.error(f"Error fetching students: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return []

def get_student(student_id):
    """Fetch single student by ID"""
    try:
        response = requests.get(f"{API_BASE_URL}{student_id}/")
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {})
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def create_student(name, age, profile_image=None):
    """Create new student"""
    try:
        if profile_image:
            files = {'profile_image': profile_image}
            data = {'name': name, 'age': age}
            response = requests.post(API_BASE_URL, data=data, files=files)
        else:
            data = {'name': name, 'age': age}
            response = requests.post(API_BASE_URL, json=data)
        
        if response.status_code == 201:
            st.success("✅ Student created successfully!")
            st.session_state.refresh += 1
            return True
        else:
            error_data = response.json()
            st.error(f"Error: {error_data.get('message', 'Unknown error')}")
            if 'errors' in error_data:
                for field, errors in error_data['errors'].items():
                    st.error(f"{field}: {', '.join(errors)}")
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

def update_student(student_id, name, age):
    """Update student information"""
    try:
        data = {'name': name, 'age': age}
        response = requests.put(f"{API_BASE_URL}{student_id}/", json=data)
        
        if response.status_code == 200:
            st.success("✅ Student updated successfully!")
            st.session_state.refresh += 1
            return True
        else:
            error_data = response.json()
            st.error(f"Error: {error_data.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

def delete_student(student_id):
    """Delete student"""
    try:
        response = requests.delete(f"{API_BASE_URL}{student_id}/")
        
        if response.status_code == 200:
            st.success("✅ Student deleted successfully!")
            st.session_state.refresh += 1
            return True
        else:
            error_data = response.json()
            st.error(f"Error: {error_data.get('message', 'Unknown error')}")
            return False
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

# Main App
def main():
    st.markdown('<h1 class="main-header">🎓 Student Management System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Navigation")
        page = st.radio(
            "Select Operation",
            ["View All Students", "Add New Student", "Update Student", "Delete Student", "Student Details"]
        )
        
        st.markdown("---")
        st.info("💡 **API Endpoint:**\n" + API_BASE_URL)
        
        if st.button("🔄 Refresh Data"):
            st.session_state.refresh += 1
            st.rerun()
    
    # Main Content
    if page == "View All Students":
        view_all_students()
    elif page == "Add New Student":
        add_student_form()
    elif page == "Update Student":
        update_student_form()
    elif page == "Delete Student":
        delete_student_form()
    elif page == "Student Details":
        student_details()

def view_all_students():
    """Display all students in a table"""
    st.header("📊 All Students")
    
    students = get_all_students()
    
    if students:
        # Display statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Students", len(students))
        with col2:
            avg_age = sum(s['age'] for s in students) / len(students)
            st.metric("Average Age", f"{avg_age:.1f}")
        with col3:
            with_images = sum(1 for s in students if s.get('profile_image'))
            st.metric("With Profile Images", with_images)
        
        st.markdown("---")
        
        # Create DataFrame
        df_data = []
        for student in students:
            df_data.append({
                'ID': student['id'],
                'Name': student['name'],
                'Age': student['age'],
                'Has Image': '✅' if student.get('profile_image') else '❌',
                'Created': datetime.fromisoformat(student['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
            })
        
        df = pd.DataFrame(df_data)
        
        # Display table
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Export option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="students.csv",
            mime="text/csv"
        )
        
    else:
        st.info("No students found. Add some students to get started!")

def add_student_form():
    """Form to add new student"""
    st.header("➕ Add New Student")
    
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Student Name *", placeholder="Enter full name")
            age = st.number_input("Age *", min_value=5, max_value=100, value=18)
        
        with col2:
            profile_image = st.file_uploader(
                "Profile Image (Optional)",
                type=['jpg', 'jpeg', 'png'],
                help="Upload a profile picture"
            )
            
            if profile_image:
                st.image(profile_image, caption="Preview", width=200)
        
        submitted = st.form_submit_button("✨ Create Student", use_container_width=True)
        
        if submitted:
            if not name or not name.strip():
                st.error("❌ Name is required!")
            else:
                with st.spinner("Creating student..."):
                    create_student(name.strip(), age, profile_image)

def update_student_form():
    """Form to update existing student"""
    st.header("✏️ Update Student")
    
    students = get_all_students()
    
    if not students:
        st.warning("No students available to update.")
        return
    
    # Create selection dropdown
    student_options = {f"{s['id']} - {s['name']}": s['id'] for s in students}
    
    selected = st.selectbox(
        "Select Student to Update",
        options=list(student_options.keys())
    )
    
    if selected:
        student_id = student_options[selected]
        student = get_student(student_id)
        
        if student:
            with st.form("update_student_form"):
                st.info(f"**Current Details:** {student['name']}, Age: {student['age']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("New Name", value=student['name'])
                
                with col2:
                    new_age = st.number_input(
                        "New Age",
                        min_value=5,
                        max_value=100,
                        value=student['age']
                    )
                
                submitted = st.form_submit_button("💾 Update Student", use_container_width=True)
                
                if submitted:
                    if not new_name or not new_name.strip():
                        st.error("❌ Name cannot be empty!")
                    else:
                        with st.spinner("Updating student..."):
                            update_student(student_id, new_name.strip(), new_age)

def delete_student_form():
    """Form to delete student"""
    st.header("🗑️ Delete Student")
    
    students = get_all_students()
    
    if not students:
        st.warning("No students available to delete.")
        return
    
    # Create selection dropdown
    student_options = {f"{s['id']} - {s['name']} (Age: {s['age']})": s['id'] for s in students}
    
    selected = st.selectbox(
        "Select Student to Delete",
        options=list(student_options.keys())
    )
    
    if selected:
        student_id = student_options[selected]
        student = get_student(student_id)
        
        if student:
            st.warning(f"⚠️ You are about to delete: **{student['name']}**")
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True):
                    with st.spinner("Deleting student..."):
                        delete_student(student_id)
            
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    st.info("Deletion cancelled.")

def student_details():
    """Show detailed view of a single student"""
    st.header("🔍 Student Details")
    
    students = get_all_students()
    
    if not students:
        st.warning("No students available.")
        return
    
    # Create selection dropdown
    student_options = {f"{s['id']} - {s['name']}": s['id'] for s in students}
    
    selected = st.selectbox(
        "Select Student",
        options=list(student_options.keys())
    )
    
    if selected:
        student_id = student_options[selected]
        student = get_student(student_id)
        
        if student:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                if student.get('profile_image'):
                    st.image(student['profile_image'], caption="Profile Image", width=250)
                else:
                    st.info("No profile image available")
            
            with col2:
                st.subheader(f"📝 {student['name']}")
                
                st.markdown(f"""
                **ID:** {student['id']}  
                **Age:** {student['age']} years  
                **Created:** {datetime.fromisoformat(student['created_at'].replace('Z', '+00:00')).strftime('%B %d, %Y at %H:%M')}  
                **Last Updated:** {datetime.fromisoformat(student['updated_at'].replace('Z', '+00:00')).strftime('%B %d, %Y at %H:%M')}  
                """)
                
                st.markdown("---")
                
                # Quick actions
                st.subheader("⚡ Quick Actions")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    if st.button("✏️ Edit This Student", use_container_width=True):
                        st.session_state.page = "Update Student"
                        st.rerun()
                
                with col_b:
                    if st.button("🗑️ Delete This Student", use_container_width=True, type="primary"):
                        if st.session_state.get('confirm_delete') == student_id:
                            delete_student(student_id)
                            st.session_state.confirm_delete = None
                        else:
                            st.session_state.confirm_delete = student_id
                            st.warning("⚠️ Click again to confirm deletion")

if __name__ == "__main__":
    main()
