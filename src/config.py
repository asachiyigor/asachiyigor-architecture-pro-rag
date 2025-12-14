"""
Configuration settings for RAG Bot
"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
KB_DIR = PROJECT_ROOT / "knowledge_base"
LOGS_DIR = PROJECT_ROOT / "logs"

# Model settings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gpt-3.5-turbo"  # или другая модель

# Index settings
FAISS_INDEX_PATH = DATA_DIR / "faiss.index"
CHUNKS_METADATA_PATH = DATA_DIR / "chunks_metadata.pkl"
INDEX_CONFIG_PATH = DATA_DIR / "index_config.json"

# Search settings
TOP_K_RESULTS = 5
SIMILARITY_THRESHOLD = 0.7

# API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Chunking settings
CHUNK_SIZE = 500  # words
CHUNK_OVERLAP = 50  # words
