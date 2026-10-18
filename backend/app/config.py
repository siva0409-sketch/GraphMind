import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

FALKORDB_URL = os.getenv("FALKORDB_URL", "").strip() or None
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "localhost")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", "6379"))
FALKORDB_GRAPH = os.getenv("FALKORDB_GRAPH", "graphmind")
FALKORDB_USERNAME = os.getenv("FALKORDB_USERNAME", "").strip() or None
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", "").strip() or None

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
