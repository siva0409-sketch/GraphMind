# GraphMind — FalkorDB Agent with Session Memory

A starter hackathon project: FastAPI + FalkorDB + OpenAI-compatible chat generation + React UI.

## Run with Docker
1. Copy `.env.example` to `.env`.
2. Optionally add your `OPENAI_API_KEY` to `.env`.
3. Run `docker compose up --build`.
4. Open http://localhost:5173. API docs: http://localhost:8000/docs.

## Without Docker
Run FalkorDB locally, then:
- Backend: `cd backend`, create/activate a Python virtual environment, `pip install -r requirements.txt`, then `uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend`, run `npm install`, then `npm run dev`

## What is included
- Persistent session messages stored in FalkorDB
- Knowledge entities and relationships stored in FalkorDB
- Graph fact retrieval to ground answers
- OpenAI API integration when `OPENAI_API_KEY` is set
- Graph-only fallback if no API key is configured
- React chat UI, session list, add-entity form, add-relationship form, and graph-evidence panel

The graph starts empty intentionally. Add your own authorized information in the UI or via the API. This starter does not bundle a fake dataset.

## Example API calls
```bash
curl -X POST http://localhost:8000/api/knowledge/entities -H "Content-Type: application/json" -d '{"name":"Driver Drowsiness Detection","entity_type":"Project","description":"A computer vision project"}'
curl -X POST http://localhost:8000/api/knowledge/entities -H "Content-Type: application/json" -d '{"name":"Python","entity_type":"Technology","description":"Programming language"}'
curl -X POST http://localhost:8000/api/knowledge/relationships -H "Content-Type: application/json" -d '{"source":"Driver Drowsiness Detection","relation":"USES","target":"Python"}'
```

Then ask: `Which technology does Driver Drowsiness Detection use?`

## Notes
- A session ID identifies one conversation. Its messages persist across page reloads and backend restarts.
- This starter implements persistent session history, not automatic cross-session user-profile memory.
- Add authentication, authorization, rate limits, and privacy controls before exposing it publicly.
