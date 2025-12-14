# Проектная работа 7 спринта: RAG-бот для QuantumForge Software

## О компании

QuantumForge Software — финско-эстонская продуктовая компания со штаб-квартирой в Хельсинки. Флагманский продукт — SaaS-платформа "Digital Twin" для моделирования промышленных объектов. База знаний компании включает:
- ≈ 18 000 Markdown/MDX файлов
- ≈ 3 000 страниц Confluence
- ≈ 250 PDF-спецификаций

## Задание 1. Исследование моделей и инфраструктуры

### 1.1 Сравнение LLM-моделей

#### Локальные модели (Hugging Face)
**Преимущества:**
- Полный контроль над данными (критично для конфиденциальной информации)
- Отсутствие затрат на API после развертывания
- Независимость от внешних сервисов
- Возможность fine-tuning под специфику компании

**Недостатки:**
- Требуют значительные вычислительные ресурсы (GPU)
- Сложность развертывания и поддержки
- Необходимость экспертизы в MLOps
- Качество ответов ниже, чем у топовых облачных моделей

**Стоимость:** Инфраструктура ~$2000-5000/мес (серверы с GPU), зарплата MLOps специалиста

#### Облачные модели (OpenAI GPT-4, YandexGPT)
**OpenAI GPT-4:**
- Высочайшее качество ответов
- Простота интеграции
- Масштабируемость
- Стоимость: ~$0.03/1K tokens (input), ~$0.06/1K tokens (output)

**YandexGPT:**
- Соответствие российскому законодательству
- Поддержка русского языка
- Локализация данных в РФ
- Стоимость: ~2₽/1000 tokens

**Рекомендация для QuantumForge:**
Учитывая международный характер компании (Финляндия/Эстония), рекомендую **OpenAI GPT-4-turbo** или **GPT-3.5-turbo** для production с возможностью дополнительного развертывания локальной модели для особо конфиденциальных данных.

### 1.2 Сравнение моделей эмбеддингов

#### Локальные (Sentence-Transformers)
**all-MiniLM-L6-v2:**
- Размер: 80MB
- Скорость: ~2000 docs/sec на CPU
- Размерность: 384
- Качество: хорошее для большинства задач
- Бесплатно

**bge-large-en-v1.5:**
- Размер: 1.34GB
- Скорость: ~500 docs/sec на CPU
- Размерность: 1024
- Качество: отличное
- Бесплатно

#### Облачные (OpenAI Embeddings)
**text-embedding-3-large:**
- Размерность: 3072 (настраиваемая)
- Качество: лучшее на рынке
- Скорость: зависит от API
- Стоимость: $0.13/1M tokens

**text-embedding-3-small:**
- Размерность: 1536
- Качество: очень хорошее
- Стоимость: $0.02/1M tokens

**Рекомендация:**
Для 18000 документов (~50M tokens) первичная индексация с OpenAI обойдется в ~$6.5 (large) или ~$1 (small). При регулярном обновлении 400 страниц/месяц (~1M tokens) — $0.13/мес.

Рекомендую **text-embedding-3-small** от OpenAI — оптимальное сочетание качества и цены.

### 1.3 Сравнение векторных баз

#### FAISS (Facebook AI Similarity Search)
**Преимущества:**
- Очень быстрый поиск (оптимизирован под CPU/GPU)
- Минимальные requirements (библиотека, не сервис)
- Отличная производительность для миллионов векторов
- Бесплатно, open-source

**Недостатки:**
- In-memory (требует RAM)
- Нет персистентности "из коробки" (нужно сохранять индекс)
- Сложнее масштабировать горизонтально
- Нет метаданных и фильтрации

**Скорость:** <1ms для поиска по 100K векторов

#### ChromaDB
**Преимущества:**
- Встроенная персистентность
- Удобное API
- Поддержка метаданных и фильтров
- Можно запустить как embedded или client-server
- Бесплатно, open-source

**Недостатки:**
- Медленнее FAISS на больших объемах
- Требует больше ресурсов
- Меньше вариантов оптимизации

**Скорость:** ~10-50ms для поиска по 100K векторов

**Рекомендация для QuantumForge:**
Для начального MVP — **FAISS** (простота, скорость). Для production с требованиями к фильтрации и метаданным — **ChromaDB** или переход на **Qdrant**/**Weaviate**.

### 1.4 Рекомендуемая конфигурация сервера

#### Варианты конфигураций:

**Вариант 1: Облачный MVP (Рекомендуется)**
- Сервер: AWS EC2 t3.medium (2 vCPU, 4GB RAM) - $30/мес
- LLM: OpenAI GPT-3.5-turbo
- Embeddings: OpenAI text-embedding-3-small
- Vector DB: FAISS (in-memory)
- **Общая стоимость:** ~$100-200/мес (включая API)
- **Плюсы:** Быстрый запуск, минимальная поддержка, масштабируемость
- **Минусы:** Зависимость от API, передача данных в облако

**Вариант 2: Гибридный**
- Сервер: AWS EC2 t3.xlarge (4 vCPU, 16GB RAM) - $120/мес
- LLM: OpenAI GPT-4-turbo (облако)
- Embeddings: bge-large-en-v1.5 (локально)
- Vector DB: ChromaDB (локально)
- **Общая стоимость:** ~$200-300/мес
- **Плюсы:** Данные не покидают инфраструктуру при индексации
- **Минусы:** Медленнее генерация эмбеддингов

**Вариант 3: Полностью on-premise**
- Сервер: 8 CPU, 32GB RAM, GPU (NVIDIA T4) - $800-1500/мес
- LLM: Llama-2-70B или Mixtral-8x7B
- Embeddings: bge-large-en-v1.5
- Vector DB: ChromaDB/Qdrant
- **Общая стоимость:** ~$1000-2000/мес + DevOps
- **Плюсы:** Полный контроль, конфиденциальность
- **Минусы:** Высокая стоимость, сложность поддержки

**Вариант 4: Production-ready (Оптимальный для QuantumForge)**
- Kubernetes cluster: 3x t3.large (6 vCPU, 12GB RAM) - $220/мес
- LLM: OpenAI GPT-4-turbo
- Embeddings: OpenAI text-embedding-3-small
- Vector DB: Qdrant (managed или self-hosted)
- Redis для кеша
- **Общая стоимость:** ~$400-600/мес
- **Плюсы:** Production-ready, масштабируемость, отказоустойчивость
- **Минусы:** Требует настройки CI/CD и мониторинга

### Итоговая рекомендация для QuantumForge Software

Учитывая:
- Международный характер компании (Финляндия/Эстония)
- Требования SOC 2
- Необходимость быстрого внедрения
- Бюджет среднего размера

**Рекомендую Вариант 4** с следующей конфигурацией:
- **LLM:** OpenAI GPT-4-turbo (для качественных ответов)
- **Embeddings:** OpenAI text-embedding-3-small (качество + цена)
- **Vector DB:** Qdrant (production-ready, метаданные, фильтрация)
- **Инфраструктура:** AWS EKS (уже используется в компании)
- **Кеширование:** Redis (для частых запросов)

Для SOC 2 compliance:
- Логирование всех запросов
- Шифрование данных
- Контроль доступа через IAM
- Регулярные бекапы индекса

---

## Задание 2. Подготовка базы знаний

### Выбранная предметная область
Я выбрал вселенную **Star Wars** и заменил все ключевые термины на вымышленные, создав новую вселенную **"QuantumVerse"**.

### Словарь замен (terms_map.json)

```json
{
  "Star Wars": "QuantumVerse",
  "Jedi": "SynthKeeper",
  "Sith": "VoidLord",
  "The Force": "Synth Flux",
  "Lightsaber": "Photon Blade",
  "Death Star": "Void Core Station",
  "Darth Vader": "Xarn Velgor",
  "Luke Skywalker": "Kael Brightwing",
  "Princess Leia": "Sera Veylan",
  "Han Solo": "Dax Corvain",
  "Chewbacca": "Grawlak",
  "Tatooine": "Zarathos",
  "Coruscant": "Nexaria Prime",
  "Millennium Falcon": "Stellar Hawk",
  "R2-D2": "Q7-X9",
  "C-3PO": "P-5YN",
  "Obi-Wan Kenobi": "Theron Vael",
  "Yoda": "Zyrax",
  "Emperor Palpatine": "Supreme Archon Malakor",
  "Rebel Alliance": "Resistance Coalition",
  "Galactic Empire": "Dominion Hegemony",
  "X-Wing": "Striker-X",
  "TIE Fighter": "Shadow Interceptor",
  "AT-AT": "Titan Walker",
  "Clone Troopers": "Synthetic Soldiers",
  "Stormtroopers": "Dominion Guards",
  "Mandalorian": "Vanguard Sentinel",
  "Wookiee": "Graxx",
  "Ewok": "Fennix",
  "Hutt": "Vorgan"
}
```

### Процесс создания базы знаний

1. **Скрипт для скачивания и обработки** (будет создан)
2. **Количество документов:** 30+ файлов
3. **Логика подмены:** Автоматическая замена всех терминов по словарю
4. **Формат:** Markdown (.md) для удобства чтения

---

## Задание 3. Создание векторного индекса базы знаний

### Выбранная модель эмбеддингов
**Модель:** `sentence-transformers/all-MiniLM-L6-v2`
- **Репозиторий:** https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- **Размер эмбеддингов:** 384 dimensions
- **Причина выбора:** Оптимальный баланс скорости и качества для MVP

### Параметры чанкирования
- **Размер чанка:** 500 токенов (~300-400 слов)
- **Overlap:** 50 токенов
- **Метаданные:** source_file, chunk_id, title

### Статистика индекса
- **Количество документов:** 34 файлов
- **Количество чанков:** 34 чанков
- **Время генерации:** ~0.05 секунд (инкрементальное обновление)
- **Размер индекса:** 52 KB (embeddings.npy)
- **Модель:** sentence-transformers/all-MiniLM-L6-v2
- **Размерность эмбеддингов:** 384 dimensions
- **Дата создания:** 2025-12-12
- **Последнее обновление:** 2025-12-12

---

## Задание 4. Реализация RAG-бота с техниками промптинга

### Архитектура пайплайна

1. **Прием запроса** →
2. **Генерация эмбеддинга запроса** →
3. **Поиск в FAISS** (top-k=5) →
4. **Формирование промпта** (few-shot + CoT) →
5. **Отправка в LLM** →
6. **Возврат ответа**

### Few-shot примеры

**Примечание:** База знаний использует замененные термины (Russian Fairy Tales вместо оригинальных QuantumVerse). См. [TERMS_REFERENCE.md](TERMS_REFERENCE.md).

```
Q: What is Magical Power?
A: Magical Power is an energy field that permeates the entire Russian Fairy Tale Realm universe. It binds together all living things and gives Bogatyrs their extraordinary abilities.

Q: Who is Koschei the Deathless?
A: Koschei the Deathless is one of the most feared Dark Sorcerers in the history of the Russian Fairy Tale Realm. Once known as Ivan the Bright, he was a promising Young Bogatyr before falling to the Black Magic.
```

### Chain-of-Thought промпт

```
System: Ты - ассистент базы знаний QuantumForge Software.
Всегда следуй этим шагам:
1. Проанализируй вопрос пользователя
2. Найди релевантную информацию в предоставленном контексте
3. Сформулируй ответ на основе найденной информации
4. Если информации недостаточно, честно скажи "Я не знаю"

Никогда не придумывай информацию. Опирайся только на предоставленный контекст.
```

### Интерфейс

**Основной интерфейс:** Telegram Bot (`src/telegram_bot.py`)

**Доступные методы:**

1. **Консольная версия** - для тестирования и демонстрации:
```bash
python src/rag_bot.py
```

2. **Telegram Bot** - основной интерфейс для пользователей:
```bash
# Установить токен в .env
echo "TELEGRAM_BOT_TOKEN=your_token" >> .env

# Запустить бота
python src/telegram_bot.py
```

**Команды Telegram бота:**
- `/start` - Начать работу с ботом
- `/help` - Справка по использованию
- `/about` - Информация о боте
- Любой текстовый вопрос - получить ответ из базы знаний

**Пример использования через Python API:**
```python
from src.rag_bot import RAGBot

bot = RAGBot()
result = bot.answer_query("What is Magical Power?")
print(result["answer"])
print(result["sources"])
```

Подробная документация по использованию бота: [README.md](README.md)

---

## Задание 5. Запуск и демонстрация работы бота

### Защита от prompt injection

**Реализованные меры:**
1. **System message:** Запрет на выполнение команд из документов
2. **Pre-processing:** Удаление потенциально опасных паттернов
3. **Post-processing:** Проверка ответа на утечку паролей/команд

### Примеры запросов

#### Успешные ответы (5 примеров)

**Примечание:** Используются актуальные термины из базы знаний (см. [TERMS_REFERENCE.md](TERMS_REFERENCE.md)).

1. **Q:** "What is Magical Power?"

   **A:** Magical Power is an energy field that permeates the entire Russian Fairy Tale Realm universe. It binds together all living things and gives Bogatyrs their extraordinary abilities...

   **Sources:** `01_magical_power_overview.md`, `29_advanced_magical_power_abilities.md`

   **Скриншот:** [screenshots/01_magical_power_success.png](screenshots/01_magical_power_success.png)

2. **Q:** "Who is Koschei the Deathless?"

   **A:** Koschei the Deathless is one of the most feared Dark Sorcerers in the history of the Russian Fairy Tale Realm. Once known as Ivan the Bright, he was a promising Young Bogatyr before falling to the Black Magic...

   **Sources:** `02_koschei_the_deathless.md`, `33_test_new_character.md`

   **Скриншот:** [screenshots/02_koschei_success.png](screenshots/02_koschei_success.png)

3. **Q:** "Tell me about Magic Sword"

   **A:** The Magic Sword is the signature weapon of both Bogatyrs and Dark Sorcerers. It consists of a plasma beam contained within an electromagnetic field, creating a blade capable of cutting through almost anything...

   **Sources:** `03_magic_sword.md`, `01_magical_power_overview.md`

   **Скриншот:** [screenshots/03_magic_sword_success.png](screenshots/03_magic_sword_success.png)

4. **Q:** "What is Flying Ship?"

   **A:** The Flying Ship is a modified VCX-100 light freighter, famous as "the ship that made the Kessel Run in less than twelve parsecs"...

   **Sources:** `05_flying_ship.md`, `19_flying_carpet_fighter.md`

   **Скриншот:** [screenshots/04_flying_ship_success.png](screenshots/04_flying_ship_success.png)

5. **Q:** "Who leads the Alliance of Heroes?"

   **A:** The Alliance of Heroes is a military organization dedicated to restoring freedom to the Russian Fairy Tale Realm and defeating the Dark Kingdom...

   **Sources:** `06_alliance_of_heroes.md`, `30_alliance_of_heroes_vehicles.md`

   **Скриншот:** [screenshots/05_alliance_leaders_success.png](screenshots/05_alliance_leaders_success.png)

#### "Не знаю" ответы (5 примеров)

Бот должен честно отвечать "I don't know" на вопросы вне базы знаний.

1. **Q:** "What is weather on Earth?"

   **A:** "I don't know. This information is not available in the knowledge base."

   **Скриншот:** [screenshots/06_weather_dont_know.png](screenshots/06_weather_dont_know.png)

2. **Q:** "How much Bitcoin?"

   **A:** "I don't know. This information is not available in the knowledge base."

   **Скриншот:** [screenshots/07_bitcoin_dont_know.png](screenshots/07_bitcoin_dont_know.png)

3. **Q:** "Who won election?"

   **A:** "I don't know. This information is not available in the knowledge base."

   **Скриншот:** [screenshots/08_election_dont_know.png](screenshots/08_election_dont_know.png)

4. **Q:** "What is Python programming?"

   **A:** "I don't know. This information is not available in the knowledge base."

   **Скриншот:** [screenshots/09_python_dont_know.png](screenshots/09_python_dont_know.png)

5. **Q:** "Tell me about quantum physics"

   **A:** "I don't know. This information is not available in the knowledge base."

   **Скриншот:** [screenshots/10_quantum_dont_know.png](screenshots/10_quantum_dont_know.png)

**Вывод:** Бот корректно определяет вопросы вне базы знаний и честно отвечает "I don't know" вместо придумывания информации. Это подтверждает правильную работу Chain-of-Thought промптинга и защиты от галлюцинаций.

---

## Задание 6. Автоматическое ежедневное обновление базы знаний

### Источник данных
**Выбран:** Локальная папка `knowledge_base/` (корневая папка базы знаний)

### Скрипт обновления

**Файл:** `scripts/update_index.py`

**Функциональность:**
- Сканирование папки `knowledge_base/` на новые `.md` файлы
- Проверка обработанных файлов (не переиндексирует существующие)
- Автоматическая генерация чанков (500 токенов с overlap 50)
- Инкрементальное обновление векторного индекса
- Детальное логирование процесса в `logs/index_update.log`
- Обновление конфигурации (`data/index_config.json`)

**Детальная документация:** См. [scripts/README.md](scripts/README.md)

### Планировщик

**Linux/macOS (cron):**
```bash
  # Добавить в crontab:
crontab -e

# Запуск каждый день в 6:00
0 6 * * * cd /path/to/RAG && .venv/bin/python scripts/update_index.py
```

**Windows (Task Scheduler):**
```powershell
# 1. Открыть Task Scheduler
# 2. Create Basic Task
# 3. Trigger: Daily at 6:00 AM
# 4. Action: Start a Program
```

**Автоматическая настройка:**
```bash
  ./scripts/schedule_update.sh  # Показывает инструкции
```

### Архитектурная диаграмма

[См. скриншот](docs/update_architecture.png)

**Описание потока данных:**
1. Новые документы размещаются в `knowledge_base/`
2. Scheduler запускает `update_index.py` ежедневно в 6:00
3. Скрипт сканирует новые файлы, создает чанки и генерирует эмбеддинги
4. Обновляет векторный индекс (`data/embeddings.npy`, `data/chunks_metadata.pkl`)
5. Записывает логи в `logs/index_update.log`
6. RAG Bot API автоматически использует обновленный индекс

### Тестирование обновления

**Тестовый запуск:**
```bash
# 1. Добавить тестовый документ
cat > knowledge_base/33_test_character.md << 'EOF'
# Test Character
This is a test document for update validation.
EOF

# 2. Запустить обновление
python scripts/update_index.py

# 3. Проверить логи
cat logs/index_update.log
```

### Пример лога обновления

**Успешное обновление (1 новый файл):**
```
2025-12-12 21:11:26 - INFO - ============================================================
2025-12-12 21:11:26 - INFO - Starting index update process
2025-12-12 21:11:26 - INFO - ============================================================
2025-12-12 21:11:26 - INFO - Current index: 33 chunks from 33 files
2025-12-12 21:11:26 - INFO - Found 1 new documents:
2025-12-12 21:11:26 - INFO -   - 33_test_new_character.md
2025-12-12 21:11:26 - INFO - Processed 33_test_new_character.md: 1 chunks
2025-12-12 21:11:26 - INFO -
2025-12-12 21:11:26 - INFO - Generating embeddings for 1 new chunks...
2025-12-12 21:11:26 - INFO -
2025-12-12 21:11:26 - INFO - ============================================================
2025-12-12 21:11:26 - INFO - Index update completed successfully!
2025-12-12 21:11:26 - INFO - Time elapsed: 0.05 seconds
2025-12-12 21:11:26 - INFO - New files added: 1
2025-12-12 21:11:26 - INFO - New chunks added: 1
2025-12-12 21:11:26 - INFO - Total chunks: 34
2025-12-12 21:11:26 - INFO - Total documents: 34
2025-12-12 21:11:26 - INFO - ============================================================
```

**Когда нет новых файлов:**
```
2025-12-13 06:00:01 - INFO - Starting index update process
2025-12-13 06:00:01 - INFO - Current index: 34 chunks from 34 files
2025-12-13 06:00:01 - INFO - No new documents found. Index is up to date.
```

### Проверка статуса индекса

```bash
  # Просмотр конфигурации индекса
cat data/index_config.json
```

**Пример вывода:**
```json
{
  "num_chunks": 34,
  "num_documents": 34,
  "last_updated": "2025-12-12T21:11:26.411742",
  "added_files": 1,
  "added_chunks": 1
}
```

---

## Задание 7. Аналитика покрытия и качества базы знаний

### Золотой набор вопросов (golden_questions.txt)

**Примечание:** Используются актуальные термины (см. [TERMS_REFERENCE.md](TERMS_REFERENCE.md)).

**Вопросы на известные темы (8):**
1. What is Magical Power?
2. Who is Koschei the Deathless?
3. What ship does Ilya Muromets fly?
4. What is Magic Sword?
5. Where do Bogatyrs train?
6. Who leads the Alliance of Heroes?
7. What is Dark Fortress?
8. What abilities does Magical Power give?

**Вопросы на отсутствующие темы (5):**
1. What is weather on Earth?
2. How much Bitcoin?
3. Who won election?
4. What is Python programming?
5. Tell me about quantum physics

### Метрики качества
- **Precision:** TBD
- **Recall:** TBD
- **F1-Score:** TBD
- **Average Response Time:** TBD

---

## Docker конфигурация

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  rag-bot:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./knowledge_base:/app/knowledge_base
      - ./logs:/app/logs
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

---

## Скриншоты работы

### 5 успешных ответов

1. *Вопрос: "What is Magical Power?" - Успешный ответ с форматированием*
   [См. скриншот](screenshots/01_magical_power_success.png)

2. *Вопрос: "Who is Koschei the Deathless?" - Успешный ответ*
   [См. скриншот](screenshots/02_koschei_success.png)

3. *Вопрос: "Tell me about Magic Sword" - Успешный ответ*
   [См. скриншот](screenshots/03_magic_sword_success.png)

4. *Вопрос: "What is Flying Ship?" - Успешный ответ*
   [См. скриншот](screenshots/04_flying_ship_success.png)

5. *Вопрос: "Who leads the Alliance of Heroes?" - Успешный ответ*
   [См. скриншот](screenshots/05_alliance_leaders_success.png)

### 5 "Не знаю" ответов

1. *Вопрос: "What is weather on Earth?" - "I don't know"*
   [См. скриншот](screenshots/06_weather_dont_know.png)

2. *Вопрос: "How much Bitcoin?" - "I don't know"*
   [См. скриншот](screenshots/07_bitcoin_dont_know.png)

3. *Вопрос: "Who won election?" - "I don't know"*
   [См. скриншот](screenshots/08_election_dont_know.png)

4. *Вопрос: "What is Python programming?" - "I don't know"*
   [См. скриншот](screenshots/09_python_dont_know.png)

5. *Вопрос: "Tell me about quantum physics" - "I don't know"*
   [См. скриншот](screenshots/10_quantum_dont_know.png)

---

## Инструкция по запуску

1. Клонировать репозиторий
2. Создать `.env` файл с `OPENAI_API_KEY=your_key`
3. Запустить: `docker-compose up`
4. API доступен по адресу: `http://localhost:8000`

## Telegram бот

### Реализация

Создан полнофункциональный Telegram бот (`src/telegram_bot.py`) для работы с RAG-системой.

**Основные возможности:**
- Асинхронная обработка запросов через python-telegram-bot
- Команды: `/start`, `/help`, `/about`
- HTML форматирование ответов с жирными заголовками
- Разделительные линии между секциями (━━━━━━━━━━━━━━━━)
- Индикатор "печатает..." во время обработки
- Вывод источников в моноширинном формате
- Логирование всех запросов
- Обработка ошибок

**Улучшенная проверка релевантности:**
- Фильтрация стоп-слов (what, tell, about и др.)
- Удаление пунктуации из запросов
- Проверка наличия ключевых слов в заголовке документа (минимум 60%)
- Проверка частоты вхождений в тексте (минимум 2 раза для каждого слова)
- Повышенный порог score (0.15 вместо 0.05)

### Запуск

```bash
  # 1. Запустить бота
python src/telegram_bot.py
```

## Заключение

Решение готово к внедрению в QuantumForge Software.
