from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import get_graph, init_graph
from .memory import create_session, list_sessions, session_exists, save_message, get_messages
from .knowledge import upsert_entity, add_relationship, search_knowledge
from .agent import generate_answer
from .schemas import SessionCreate, ChatRequest, EntityCreate, RelationshipCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_graph()
    init_graph()
    yield

app = FastAPI(title="GraphMind API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    try:
        get_graph().query("RETURN 1")
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"FalkorDB unavailable: {exc}")

@app.post("/api/sessions")
def new_session(payload: SessionCreate):
    return create_session(payload.title)

@app.get("/api/sessions")
def sessions():
    return list_sessions()

@app.get("/api/sessions/{session_id}/messages")
def messages(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return get_messages(session_id)

@app.post("/api/chat")
def chat(payload: ChatRequest):
    session_id = payload.session_id
    if not session_id:
        session_id = create_session(payload.message[:48] or "New conversation")["id"]
    elif not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found. Create a new session first.")
    save_message(session_id, "user", payload.message)
    history = get_messages(session_id, limit=60)
    try:
        result = generate_answer(payload.message, history[:-1])
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent generation failed: {type(exc).__name__}: {exc}")
    save_message(session_id, "assistant", result["answer"])
    return {"session_id": session_id, **result}

@app.post("/api/knowledge/entities")
def create_entity(payload: EntityCreate):
    return upsert_entity(payload.name, payload.entity_type, payload.description)

@app.post("/api/knowledge/relationships")
def create_relation(payload: RelationshipCreate):
    return add_relationship(payload.source, payload.relation, payload.target)

@app.get("/api/knowledge/search")
def knowledge_search(q: str, limit: int = 10):
    if limit < 1 or limit > 50:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 50")
    return search_knowledge(q, limit)

# Serve built frontend if dist directory exists
frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")
