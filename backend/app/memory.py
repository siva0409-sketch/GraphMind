from datetime import datetime, timezone
from uuid import uuid4
from .database import run_query

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def create_session(title: str):
    session_id = str(uuid4())
    timestamp = now_iso()
    run_query(
        "CREATE (s:Session {id: $id, title: $title, created_at: $created, updated_at: $updated})",
        {"id": session_id, "title": title, "created": timestamp, "updated": timestamp},
    )
    return {"id": session_id, "title": title}

def list_sessions():
    result = run_query(
        "MATCH (s:Session) RETURN s.id, s.title, s.created_at, s.updated_at ORDER BY s.updated_at DESC LIMIT 100"
    )
    return [
        {"id": r[0], "title": r[1], "created_at": r[2], "updated_at": r[3]}
        for r in result.result_set
    ]

def session_exists(session_id: str):
    return bool(run_query("MATCH (s:Session {id: $id}) RETURN s.id LIMIT 1", {"id": session_id}).result_set)

def save_message(session_id: str, role: str, content: str):
    timestamp, message_id = now_iso(), str(uuid4())
    run_query("""
        MATCH (s:Session {id: $session_id})
        CREATE (m:Message {id: $message_id, role: $role, content: $content, created_at: $timestamp})
        CREATE (s)-[:HAS_MESSAGE]->(m)
        SET s.updated_at = $timestamp
    """, {"session_id": session_id, "message_id": message_id, "role": role,
          "content": content, "timestamp": timestamp})

def get_messages(session_id: str, limit: int = 60):
    result = run_query("""
        MATCH (:Session {id: $session_id})-[:HAS_MESSAGE]->(m:Message)
        RETURN m.id, m.role, m.content, m.created_at
        ORDER BY m.created_at DESC LIMIT $limit
    """, {"session_id": session_id, "limit": limit})
    rows = [{"id": r[0], "role": r[1], "content": r[2], "created_at": r[3]} for r in result.result_set]
    return list(reversed(rows))
