import streamlit as st
import os
from dotenv import load_dotenv
from modules.database import Neo4jManager
from modules.loader import load_json_files
from modules.transformer import NER_RE_extract
#from modules.transformer import get_extraction_query # renamed from your previous code

load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="KG-RAG Explorer", page_icon="🕸️", layout="wide")

# --- Database Connection (Cached) ---
@st.cache_resource
def init_db():
    return Neo4jManager(
        os.getenv("NEO4J_URI"), 
        os.getenv("NEO4J_USERNAME"), 
        os.getenv("NEO4J_PASSWORD")
    )

db = init_db()

# --- UI Header ---
st.title("🕸️ Knowledge Graph RAG Explorer")
st.markdown("Query employee skills and project collaborations directly from the Graph.")

# --- Sidebar: Data Ingestion ---
with st.sidebar:
    st.header("Admin Controls")
    if st.button("🚀 Re-Ingest JSON Data"):
        with st.spinner("Processing files..."):
            pages = load_json_files("data")
            query = NER_RE_extract(pages)
            db.save_data(query, pages)
            st.success("Graph Refreshed!")

# --- Main UI Layout ---
tab1, tab2 = st.tabs(["🔍 Skill Search", "🤝 Collaboration Finder"])

with tab1:
    st.subheader("Find Employee Skills")
    emp_input = st.text_input("Enter Employee ID (e.g., E001)", key="emp_search")
    
    if st.button("Query Skills"):
        if emp_input:
            results = db.get_employee_skills(emp_input)
            if results:
                st.write(f"Results for **{emp_input}**:")
                st.table(results) # Displays as a clean dataframe
            else:
                st.warning("No skills found for this Employee ID.")
        else:
            st.error("Please enter an ID.")

with tab2:
    st.subheader("Project Collaboration Network")
    proj_input = st.text_input("Enter Project ID (e.g., P_PHOENIX)", key="proj_search")
    
    if st.button("Find Potential Collaborators"):
        if proj_input:
            collabs = db.find_collaborators(proj_input)
            if collabs:
                st.write(f"Employees with matching skills for **{proj_input}**:")
                st.json(collabs) # Good for debugging structured data
            else:
                st.info("No collaborators found with overlapping skills.")