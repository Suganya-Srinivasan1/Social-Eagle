import streamlit as st

# 1. INITIALIZE DATABASE (Session State)
# Streamlit reruns the script on every click, so we need st.session_state 
# to keep our data from disappearing.
if "tasks" not in st.session_state:
    st.session_state.tasks = []

st.set_page_config(page_title="Streamlit Todo", page_icon="📝")

st.title("📝 Simple Streamlit Todo")

# 2. INPUT AREA (Sidebar)
st.sidebar.header("Manage Tasks")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_task_title = st.text_input("Task Title")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submit = st.form_submit_button("Add Task")

    if submit and new_task_title:
        # Create a dictionary for the new task
        task_obj = {
            "title": new_task_title,
            "priority": priority,
            "completed": False
        }
        # Save to our "database"
        st.session_state.tasks.append(task_obj)
        st.toast(f"Added: {new_task_title}")

# 3. DISPLAY AREA
st.subheader("Your Tasks")

if not st.session_state.tasks:
    st.info("Your list is empty. Add a task in the sidebar!")
else:
    # We use enumerate so we have an index for deleting/updating
    for index, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([0.1, 3, 1])
        
        with col1:
            # Checkbox to mark as completed
            is_done = st.checkbox("", value=task["completed"], key=f"check_{index}")
            st.session_state.tasks[index]["completed"] = is_done
            
        with col2:
            # Cross out text if completed
            if is_done:
                st.write(f"~~{task['title']}~~")
            else:
                st.write(f"**{task['title']}** ({task['priority']})")
                
        with col3:
            if st.button("🗑️", key=f"del_{index}"):
                st.session_state.tasks.pop(index)
                st.rerun()

# 4. STATS (Optional)
if st.session_state.tasks:
    st.divider()
    done_count = sum(1 for t in st.session_state.tasks if t["completed"])
    total = len(st.session_state.tasks)
    st.progress(done_count / total)
    st.write(f"Completed {done_count} of {total} tasks")
