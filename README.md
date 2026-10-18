# GraphMind — FalkorDB Agent with Session Memory

A full-stack AI knowledge agent: FastAPI + FalkorDB + Google Gemini (`gemini-3.8-flash`) + React UI.

## Run with Docker (Local)
1. Copy `.env.example` to `.env`.
2. Add your `GEMINI_API_KEY` to `.env`.
3. Run `docker compose up --build`.
4. Open http://localhost:5173. API docs: http://localhost:8000/docs.

## Without Docker (Local)
Run FalkorDB locally on port 6379, then:
- Backend: `cd backend`, `pip install -r requirements.txt`, then `uvicorn app.main:app --reload --port 8000`
- Frontend: `cd frontend`, `npm install`, then `npm run dev`

---

## Deploy to Render

### 1. Database (FalkorDB)
Because Render free web services are ephemeral, use a hosted FalkorDB instance:
- Create a free instance at **[FalkorDB Cloud](https://app.falkordb.cloud/)** (Free Tier available).
- Copy the connection URL or Host, Port, and Password.

### 2. Deploy via Render Blueprint (Recommended)
1. Push your repository to GitHub.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New +** > **Blueprint**.
3. Connect your `GraphMind` repository (`render.yaml` will be detected automatically).
4. Fill in the required environment variables:
   - `GEMINI_API_KEY`: Your Gemini API key.
   - `FALKORDB_URL` (or `FALKORDB_HOST`, `FALKORDB_PORT`, `FALKORDB_PASSWORD`): From your FalkorDB Cloud database.
5. Click **Apply**. Both backend and frontend will be built and deployed automatically!

---

## What is included
- Persistent session messages stored in FalkorDB
- Knowledge entities and relationships stored in FalkorDB
- Graph fact retrieval to ground answers
- Gemini API integration with `gemini-3.8-flash`
- React chat UI, session list, add-entity form, add-relationship form, and graph-evidence panel

## Example API calls
```bash
curl -X POST http://localhost:8000/api/knowledge/entities -H "Content-Type: application/json" -d '{"name":"Driver Drowsiness Detection","entity_type":"Project","description":"A computer vision project"}'
curl -X POST http://localhost:8000/api/knowledge/entities -H "Content-Type: application/json" -d '{"name":"Python","entity_type":"Technology","description":"Programming language"}'
curl -X POST http://localhost:8000/api/knowledge/relationships -H "Content-Type: application/json" -d '{"source":"Driver Drowsiness Detection","relation":"USES","target":"Python"}'
```

Then ask: `Which technology does Driver Drowsiness Detection use?`
