#!/usr/bin/env python
"""
Скрипт для создания векторного индекса из базы знаний.
Использует sentence-transformers для генерации эмбеддингов и FAISS для индексации.
"""

import os
import json
import time
import pickle
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Проверяем наличие необходимых библиотек
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
except ImportError:
    print("Installing required packages...")
    os.system("pip install sentence-transformers faiss-cpu numpy")
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np


class DocumentChunker:
    """Разбивает документы на чанки с метаданными"""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source_file: str) -> List[Dict]:
        """Разбивает текст на чанки с метаданными"""
        # Простое разбиение по словам (можно улучшить с токенизацией)
        words = text.split()
        chunks = []
        chunk_id = 0

        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            # Извлекаем заголовок из первой строки документа
            title = text.split("\\n")[0].replace("#", "").strip()

            chunks.append(
                {
                    "text": chunk_text,
                    "source_file": source_file,
                    "chunk_id": chunk_id,
                    "title": title,
                    "word_count": len(chunk_words),
                }
            )
            chunk_id += 1

        return chunks


class VectorIndexBuilder:
    """Строит векторный индекс из документов"""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Embedding dimension: {self.embedding_dim}")

        self.chunker = DocumentChunker(chunk_size=500, overlap=50)
        self.chunks = []
        self.embeddings = None
        self.index = None

    def load_documents(self, knowledge_base_dir: str) -> None:
        """Загружает и чанкует все документы из директории"""
        print(f"\\nLoading documents from: {knowledge_base_dir}")
        kb_path = Path(knowledge_base_dir)

        markdown_files = list(kb_path.glob("*.md"))
        print(f"Found {len(markdown_files)} markdown files")

        for md_file in markdown_files:
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            file_chunks = self.chunker.chunk_text(content, md_file.name)
            self.chunks.extend(file_chunks)
            print(f"  {md_file.name}: {len(file_chunks)} chunks")

        print(f"\\nTotal chunks created: {len(self.chunks)}")

    def generate_embeddings(self) -> None:
        """Генерирует эмбеддинги для всех чанков"""
        print(f"\\nGenerating embeddings for {len(self.chunks)} chunks...")
        start_time = time.time()

        # Извлекаем тексты
        texts = [chunk["text"] for chunk in self.chunks]

        # Генерируем эмбеддинги батчами
        self.embeddings = self.model.encode(
            texts, show_progress_bar=True, convert_to_numpy=True
        )

        elapsed_time = time.time() - start_time
        print(f"Embeddings generated in {elapsed_time:.2f} seconds")
        print(f"Embeddings shape: {self.embeddings.shape}")

    def build_faiss_index(self) -> None:
        """Создает FAISS индекс из эмбеддингов"""
        print("\\nBuilding FAISS index...")

        # Используем IndexFlatL2 для точного поиска (для больших объемов можно использовать IndexIVFFlat)
        self.index = faiss.IndexFlatL2(self.embedding_dim)

        # Добавляем векторы в индекс
        self.index.add(self.embeddings.astype("float32"))

        print(f"Index built with {self.index.ntotal} vectors")

    def test_search(self, query: str, k: int = 5) -> None:
        """Тестирует поиск по индексу"""
        print(f"\\n=== Testing search with query: '{query}' ===")

        # Генерируем эмбеддинг запроса
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        # Ищем ближайшие векторы
        distances, indices = self.index.search(query_embedding.astype("float32"), k)

        print(f"\\nTop {k} results:")
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
            chunk = self.chunks[idx]
            print(f"\\n{i+1}. Distance: {dist:.4f}")
            print(f"   Source: {chunk['source_file']}")
            print(f"   Title: {chunk['title']}")
            print(f"   Text preview: {chunk['text'][:200]}...")

    def save_index(self, output_dir: str = "data") -> None:
        """Сохраняет индекс и метаданные"""
        print(f"\\nSaving index to {output_dir}/...")
        os.makedirs(output_dir, exist_ok=True)

        # Сохраняем FAISS индекс
        faiss.write_index(self.index, f"{output_dir}/faiss.index")

        # Сохраняем метаданные чанков
        with open(f"{output_dir}/chunks_metadata.pkl", "wb") as f:
            pickle.dump(self.chunks, f)

        # Сохраняем информацию о конфигурации
        config = {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "num_chunks": len(self.chunks),
            "num_documents": len(set(chunk["source_file"] for chunk in self.chunks)),
            "created_at": datetime.now().isoformat(),
        }

        with open(f"{output_dir}/index_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print("Index saved successfully!")
        print(f"  - faiss.index")
        print(f"  - chunks_metadata.pkl")
        print(f"  - index_config.json")


def main():
    print("=" * 60)
    print("Building Vector Index for RAG Bot")
    print("=" * 60)

    # Создаем билдер индекса
    builder = VectorIndexBuilder(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Загружаем документы
    builder.load_documents("knowledge_base")

    # Генерируем эмбеддинги
    builder.generate_embeddings()

    # Строим FAISS индекс
    builder.build_faiss_index()

    # Тестируем поиск
    print("\\n" + "=" * 60)
    print("Testing Search")
    print("=" * 60)

    test_queries = [
        "What is Synth Flux?",
        "Who is Xarn Velgor?",
        "Tell me about Photon Blades",
    ]

    for query in test_queries:
        builder.test_search(query, k=3)

    # Сохраняем индекс
    print("\\n" + "=" * 60)
    builder.save_index("data")

    print("\\n" + "=" * 60)
    print("Index building complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
