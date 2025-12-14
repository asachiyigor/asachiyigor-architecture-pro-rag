#!/usr/bin/env python
"""
Упрощенный скрипт для создания векторного индекса.
Создает mock индекс для тестирования без загрузки больших моделей.
"""

import os
import json
import pickle
from pathlib import Path
from datetime import datetime
import numpy as np


class SimpleDocumentChunker:
    """Разбивает документы на чанки"""

    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source_file: str) -> list:
        """Разбивает текст на чанки, сохраняя структуру"""
        # Для небольших документов просто возвращаем весь текст как один чанк
        # Это сохранит форматирование и структуру

        title = text.split("\n")[0].replace("#", "").strip()

        chunks = [{
            "text": text,  # Сохраняем весь текст со всеми переносами строк
            "source_file": source_file,
            "chunk_id": 0,
            "title": title,
            "word_count": len(text.split()),
        }]

        return chunks


def create_simple_embeddings(texts: list, dim: int = 384) -> np.ndarray:
    """Создает простые эмбеддинги на основе хэшей текста"""
    embeddings = []
    for text in texts:
        # Простой детерминированный метод создания векторов
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(dim).astype("float32")
        # Нормализация
        embedding = embedding / np.linalg.norm(embedding)
        embeddings.append(embedding)
    return np.array(embeddings)


def main():
    print("=" * 60)
    print("Building Simple Vector Index for RAG Bot")
    print("=" * 60)

    # Создаем директорию для данных
    os.makedirs("data", exist_ok=True)

    # Загружаем документы
    chunker = SimpleDocumentChunker(chunk_size=500, overlap=50)
    chunks = []

    print("\\nLoading documents from knowledge_base/...")
    kb_path = Path("knowledge_base")
    markdown_files = list(kb_path.glob("*.md"))
    print(f"Found {len(markdown_files)} markdown files")

    for md_file in markdown_files:
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        file_chunks = chunker.chunk_text(content, md_file.name)
        chunks.extend(file_chunks)
        print(f"  {md_file.name}: {len(file_chunks)} chunks")

    print(f"\\nTotal chunks: {len(chunks)}")

    # Создаем эмбеддинги
    print("\\nGenerating embeddings...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = create_simple_embeddings(texts, dim=384)
    print(f"Embeddings shape: {embeddings.shape}")

    # Создаем простой индекс (для FAISS потребуется импорт, используем numpy)
    print("\\nSaving data...")

    # Сохраняем эмбеддинги
    np.save("data/embeddings.npy", embeddings)

    # Сохраняем метаданные
    with open("data/chunks_metadata.pkl", "wb") as f:
        pickle.dump(chunks, f)

    # Сохраняем конфигурацию
    config = {
        "model_name": "simple-hash-embeddings",
        "embedding_dim": 384,
        "num_chunks": len(chunks),
        "num_documents": len(markdown_files),
        "created_at": datetime.now().isoformat(),
    }

    with open("data/index_config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("\\n" + "=" * 60)
    print("Index created successfully!")
    print(f"  - embeddings.npy ({embeddings.shape})")
    print(f"  - chunks_metadata.pkl ({len(chunks)} chunks)")
    print(f"  - index_config.json")
    print("=" * 60)

    # Тест поиска
    print("\\nTesting simple search...")
    query = "What is Synth Flux?"
    query_embedding = create_simple_embeddings([query], dim=384)[0]

    # Вычисляем косинусное сходство
    similarities = np.dot(embeddings, query_embedding)
    top_k_indices = np.argsort(similarities)[::-1][:3]

    print(f"\\nQuery: '{query}'")
    print("\\nTop 3 results:")
    for i, idx in enumerate(top_k_indices):
        chunk = chunks[idx]
        print(f"\\n{i+1}. Score: {similarities[idx]:.4f}")
        print(f"   Source: {chunk['source_file']}")
        print(f"   Text: {chunk['text'][:150]}...")


if __name__ == "__main__":
    main()
