#!/usr/bin/env python
"""
Скрипт для автоматического обновления векторного индекса.
Запускается по расписанию (cron/Task Scheduler).
"""

import os
import json
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/index_update.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def scan_for_new_documents(kb_dir: str, processed_files: set) -> list:
    """Сканирует директорию на наличие новых документов"""
    kb_path = Path(kb_dir)
    all_files = list(kb_path.glob("*.md"))
    new_files = [f for f in all_files if f.name not in processed_files]
    return new_files


def create_simple_embeddings(texts: list, dim: int = 384) -> np.ndarray:
    """Создает эмбеддинги для текстов"""
    embeddings = []
    for text in texts:
        np.random.seed(hash(text) % (2**32))
        embedding = np.random.randn(dim).astype("float32")
        embedding = embedding / np.linalg.norm(embedding)
        embeddings.append(embedding)
    return np.array(embeddings)


def chunk_text(text: str, source_file: str, chunk_size: int = 500) -> list:
    """Разбивает текст на чанки"""
    words = text.split()
    chunks = []
    chunk_id = 0

    for i in range(0, len(words), chunk_size):
        chunk_words = words[i: i + chunk_size]
        chunk_text = " ".join(chunk_words)
        title = text.split("\\n")[0].replace("#", "").strip()

        chunks.append({
            "text": chunk_text,
            "source_file": source_file,
            "chunk_id": chunk_id,
            "title": title,
            "word_count": len(chunk_words),
        })
        chunk_id += 1

    return chunks


def update_index():
    """Главная функция обновления индекса"""
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("Starting index update process")
    logger.info("=" * 60)

    try:
        # Загружаем текущий индекс
        embeddings_path = Path("data/embeddings.npy")
        metadata_path = Path("data/chunks_metadata.pkl")
        config_path = Path("data/index_config.json")

        if embeddings_path.exists():
            current_embeddings = np.load(embeddings_path)
            with open(metadata_path, "rb") as f:
                current_chunks = pickle.load(f)
            with open(config_path, "r") as f:
                config = json.load(f)

            processed_files = set(chunk["source_file"] for chunk in current_chunks)
            logger.info(f"Current index: {len(current_chunks)} chunks from {len(processed_files)} files")
        else:
            current_embeddings = np.array([]).reshape(0, 384)
            current_chunks = []
            processed_files = set()
            config = {}
            logger.info("No existing index found, creating new one")

        # Сканируем новые файлы
        new_files = scan_for_new_documents("knowledge_base", processed_files)

        if not new_files:
            logger.info("No new documents found. Index is up to date.")
            return

        logger.info(f"Found {len(new_files)} new documents:")
        for f in new_files:
            logger.info(f"  - {f.name}")

        # Обрабатываем новые документы
        new_chunks = []
        for file_path in new_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            file_chunks = chunk_text(content, file_path.name)
            new_chunks.extend(file_chunks)
            logger.info(f"Processed {file_path.name}: {len(file_chunks)} chunks")

        # Генерируем эмбеддинги для новых чанков
        logger.info(f"\\nGenerating embeddings for {len(new_chunks)} new chunks...")
        new_texts = [chunk["text"] for chunk in new_chunks]
        new_embeddings = create_simple_embeddings(new_texts)

        # Объединяем с существующими
        updated_embeddings = np.vstack([current_embeddings, new_embeddings])
        updated_chunks = current_chunks + new_chunks

        # Сохраняем обновленный индекс
        np.save(embeddings_path, updated_embeddings)
        with open(metadata_path, "wb") as f:
            pickle.dump(updated_chunks, f)

        # Обновляем конфигурацию
        config.update({
            "num_chunks": len(updated_chunks),
            "num_documents": len(set(chunk["source_file"] for chunk in updated_chunks)),
            "last_updated": datetime.now().isoformat(),
            "added_files": len(new_files),
            "added_chunks": len(new_chunks),
        })

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        elapsed_time = (datetime.now() - start_time).total_seconds()

        logger.info("\\n" + "=" * 60)
        logger.info("Index update completed successfully!")
        logger.info(f"Time elapsed: {elapsed_time:.2f} seconds")
        logger.info(f"New files added: {len(new_files)}")
        logger.info(f"New chunks added: {len(new_chunks)}")
        logger.info(f"Total chunks: {len(updated_chunks)}")
        logger.info(f"Total documents: {config['num_documents']}")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error during index update: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # Создаем директорию для логов если не существует
    os.makedirs("logs", exist_ok=True)
    update_index()
