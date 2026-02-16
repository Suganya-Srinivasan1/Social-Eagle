from neo4j import GraphDatabase

class Neo4jManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def save_pages(self, transform):
        with driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")  # Clear old data
            try:
                session.run(transform, batch=transform)
                print(f"Successfully ingested {len(transform)} records into Neo4j.")
            except Exception as e:
                print(f"Inversion failed: {e}")
            finally:
                driver.close()

# Example Usage:
# all_data = [{'employee_id': 'E001', 'skill_id': 'S001', ...}, ...]
# ingest_data_to_neo4j(all_data)

    #Find a Specific Employee's Skills
    def get_employee_skills(query):
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
        # execute_query is the recommended modern API
            records, summary, keys = driver.execute_query(
            """
            MATCH (e:Employee {id: $eid})-[:HAS_SKILL]->(s:Skill)
            RETURN s.id AS skill, e.id AS employee
            """,
            eid=query,
            database_="neo4j",
        )
        
        # Convert records to a list of dictionaries for your RAG prompt
        return [record.data() for record in records]

# Usage
# results = get_employee_skills("E001")
# print(results)

    #Who else has the same skills?
    def find_collaborators(query):
        query = """
        MATCH (p:Project {id: $pid})<-[:WORKS_ON]-(e:Employee)-[:HAS_SKILL]->(s:Skill)
        MATCH (other:Employee)-[:HAS_SKILL]->(s)
        WHERE other <> e
        RETURN DISTINCT other.id AS potential_help, s.id AS shared_skill
        """
        with GraphDatabase.driver(URI, auth=AUTH) as driver:
           records, _, _ = driver.execute_query(query, pid=project_id)
        return [record.data() for record in records]