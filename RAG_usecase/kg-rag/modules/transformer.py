def NER_RE_extract():
    # Cypher query for bulk ingestion
    # This creates nodes for Employee, Skill, and Project, then links them
    cypher_query = """
    UNWIND $batch AS row
    // 1. Create/Update Nodes
    MERGE (e:Employee {id: row.employee_id})
    MERGE (s:Skill {id: row.skill_id})
    MERGE (p:Project {id: row.project_id})
    
    // 2. Create Relationships with properties
    MERGE (e)-[rs:HAS_SKILL]->(s)
    SET rs.years_exp = toInteger(row.years_exp)
    
    MERGE (e)-[rw:WORKS_ON]->(p)
    SET rw.is_lead = toBoolean(row.is_lead)
    """
    return cypher_query
transform = NER_RE_extract()
