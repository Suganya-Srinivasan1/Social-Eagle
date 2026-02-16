import os
from modules.loader import load_json_files
#from modules.transformer import transform_to_graph_data
from modules.transformer import NER_RE_extract
from modules.database import get_employee_skills
from modules.database import find_collaboratorss
from modules.database import save_pages
from neo4j import GraphDatabase
from modules.database import Neo4jManager
from dotenv import load_dotenv

load_dotenv()

#directory_path = r"C:\Users\Hp\My_AI_works\kg-rag\data"
directory_path = "data"

def main():
    # 1. Load
    print("--- Loading PDF ---")
    pages = load_json_files(directory_path)

    # 2. Extract/Transform
    print("--- Extracting Data ---")
    transform = NER_RE_extract()

    #graph_ready_data = transform_to_graph_data(pages)

    # 3. Store
    print("--- Connecting to Neo4j ---")
    db = Neo4jManager(os.getenv("NEO4J_URI"), os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    save_pages(transform)
    
    # 4. Retrieve
    print("--- Querying Graph ---")
    query = "E001" # EmpID hardcoded
    results = get_employee_skills(query)
    
    for res in results:
        print(f"\nFound in Page {res['id']}: {res['text'][:100]}...")
    
    print("--- Querying Graph ---")
    query = "P_PHOENIX" # ProjectID hardcoded
    results = find_collaborators(query)
    close()

if __name__ == "__main__":
    main()