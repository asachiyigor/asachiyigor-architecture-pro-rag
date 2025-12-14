#!/usr/bin/env python3
"""
Переименовывает файлы базы знаний чтобы имена соответствовали содержимому.
Использует заголовок документа для создания имени файла.
"""
import os
import re
import subprocess
from pathlib import Path

def create_slug(title: str) -> str:
    """Создает slug из заголовка для имени файла."""
    # Убираем # в начале
    title = title.lstrip('#').strip()

    # Убираем подзаголовки после дефиса
    if ' - ' in title:
        title = title.split(' - ')[0].strip()

    # Lowercase
    slug = title.lower()

    # Заменяем пробелы и дефисы на underscores
    slug = re.sub(r'[\s\-]+', '_', slug)

    # Убираем все кроме букв, цифр и underscores
    slug = re.sub(r'[^a-z0-9_]', '', slug)

    # Убираем множественные underscores
    slug = re.sub(r'_+', '_', slug)

    # Убираем underscores в начале и конце
    slug = slug.strip('_')

    return slug

def rename_files():
    """Переименовывает файлы в knowledge_base/."""
    kb_dir = Path('knowledge_base')

    if not kb_dir.exists():
        print(f"Директория {kb_dir} не найдена")
        return

    # Собираем все файлы .md
    files = sorted(kb_dir.glob('*.md'))

    renames = []

    for file_path in files:
        # Пропускаем специальные файлы
        if file_path.name in ['README.md', '99_malicious_test.md']:
            continue

        # Читаем первую строку
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()

        # Извлекаем заголовок
        if not first_line.startswith('#'):
            print(f"WARNING: {file_path.name}: no header, skipping")
            continue

        # Извлекаем номер из старого имени
        match = re.match(r'(\d+)_', file_path.name)
        if not match:
            print(f"WARNING: {file_path.name}: no number, skipping")
            continue

        number = match.group(1)

        # Создаем slug из заголовка
        slug = create_slug(first_line)

        # Новое имя
        new_name = f"{number}_{slug}.md"

        if file_path.name == new_name:
            print(f"OK {file_path.name}: already correct")
            continue

        new_path = kb_dir / new_name

        renames.append((file_path, new_path))
        print(f"RENAME: {file_path.name} -> {new_name}")

    if not renames:
        print("\nAll files already have correct names")
        return

    print(f"\nTotal renames: {len(renames)}")

    # Выполняем переименование через git mv
    for old_path, new_path in renames:
        try:
            result = subprocess.run(
                ['git', 'mv', str(old_path), str(new_path)],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"OK: Renamed {old_path.name} -> {new_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to rename {old_path.name}: {e.stderr}")

if __name__ == '__main__':
    rename_files()
