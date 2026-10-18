import re
from .database import run_query

def upsert_entity(name: str, entity_type: str, description: str):
    run_query("""
        MERGE (e:Entity {name: $name})
        SET e.entity_type = $entity_type, e.description = $description
    """, {"name": name, "entity_type": entity_type, "description": description})
    return {"name": name, "entity_type": entity_type, "description": description}

def add_relationship(source: str, relation: str, target: str):
    run_query("""
        MERGE (a:Entity {name: $source})
        ON CREATE SET a.entity_type = 'Concept', a.description = ''
        MERGE (b:Entity {name: $target})
        ON CREATE SET b.entity_type = 'Concept', b.description = ''
        MERGE (a)-[r:RELATED_TO {relation: $relation}]->(b)
    """, {"source": source, "target": target, "relation": relation.upper()})
    return {"source": source, "relation": relation.upper(), "target": target}

def search_knowledge(query: str, limit: int = 10):
    q = query.strip().lower()
    if not q:
        return []
    result = run_query("""
        MATCH (e:Entity)
        WHERE toLower(e.name) CONTAINS $q
           OR toLower(coalesce(e.description, '')) CONTAINS $q
           OR toLower(coalesce(e.entity_type, '')) CONTAINS $q
        OPTIONAL MATCH (e)-[r:RELATED_TO]->(target:Entity)
        RETURN e.name, e.entity_type, e.description,
               collect({relation: r.relation, target: target.name}) AS outgoing
        LIMIT $limit
    """, {"q": q, "limit": limit})
    found = []
    for row in result.result_set:
        outgoing = [x for x in (row[3] or []) if x and x.get("target")]
        found.append({"name": row[0], "entity_type": row[1], "description": row[2] or "",
                      "relationships": outgoing})
    return found

def get_relevant_knowledge(message: str, limit: int = 12):
    stop = {"which","what","when","where","have","does","with","that","this","from",
            "your","about","could","would","should","tell","please","project","technology",
            "using","used","were","they","them","agent","graph","memory"}
    terms = [w.lower() for w in re.findall(r"[A-Za-z0-9_-]{3,}", message) if w.lower() not in stop][:6]
    found, seen = [], set()
    for term in terms:
        for entity in search_knowledge(term, limit=5):
            if entity["name"] not in seen:
                found.append(entity)
                seen.add(entity["name"])
            if len(found) >= limit:
                return found
    return found
