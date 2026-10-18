from falkordb import FalkorDB
from .config import (
    FALKORDB_URL,
    FALKORDB_HOST,
    FALKORDB_PORT,
    FALKORDB_GRAPH,
    FALKORDB_USERNAME,
    FALKORDB_PASSWORD,
)

_db = None
_graph = None

def get_graph():
    global _db, _graph
    if _graph is None:
        if FALKORDB_URL:
            _db = FalkorDB.from_url(FALKORDB_URL)
        else:
            kwargs = {}
            if FALKORDB_PASSWORD:
                kwargs["password"] = FALKORDB_PASSWORD
            if FALKORDB_USERNAME:
                kwargs["username"] = FALKORDB_USERNAME
            _db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT, **kwargs)
        _graph = _db.select_graph(FALKORDB_GRAPH)
    return _graph

def run_query(query: str, params: dict | None = None):
    graph = get_graph()
    return graph.query(query, params=params) if params else graph.query(query)

def init_graph():
    for statement in (
        "CREATE INDEX FOR (e:Entity) ON (e.name)",
        "CREATE INDEX FOR (s:Session) ON (s.id)",
        "CREATE INDEX FOR (m:Message) ON (m.id)",
    ):
        try:
            run_query(statement)
        except Exception as exc:
            print(f"Index note: {exc}")
