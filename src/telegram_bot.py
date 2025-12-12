"""
Telegram Bot для RAG системы
Интегрирует RAGBot с Telegram для ответов на вопросы пользователей
"""

import os
import logging
from typing import Optional
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv

from rag_bot import RAGBot


# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class TelegramRAGBot:
    """Telegram бот для работы с RAG системой"""

    def __init__(self, token: str, data_dir: str = "data"):
        """
        Инициализация Telegram бота

        Args:
            token: Telegram Bot API токен
            data_dir: Директория с индексом для RAGBot
        """
        self.token = token
        self.rag_bot = RAGBot(data_dir=data_dir)
        self.application = Application.builder().token(token).build()

        # Регистрация обработчиков
        self._register_handlers()

    def format_markdown_for_telegram(self, text: str) -> str:
        """Форматирование markdown для Telegram HTML"""
        import re

        logger.info(f"Formatting text (first 100 chars): {text[:100]}")

        # Экранируем HTML символы
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')

        # Заменяем Markdown bold (**текст**) на HTML
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

        # Главный заголовок (# ) - жирный с переносом
        text = re.sub(r'^# (.*?)$', r'<b>\1</b>\n', text, flags=re.MULTILINE)

        # Подзаголовки (## ) - жирный с разделительной линией
        text = re.sub(r'^## (.*?)$', r'\n━━━━━━━━━━━━━━━━\n<b>\1</b>', text, flags=re.MULTILINE)

        # Третий уровень заголовков (### )
        text = re.sub(r'^### (.*?)$', r'\n<b>\1</b>', text, flags=re.MULTILINE)

        # Убираем лишние пустые строки (больше 2 подряд)
        text = re.sub(r'\n{3,}', '\n\n', text)

        logger.info(f"Formatted text (first 100 chars): {text[:100]}")

        return text.strip()

    def _register_handlers(self):
        """Регистрация обработчиков команд и сообщений"""
        # Команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("about", self.about_command))

        # Обработка текстовых сообщений
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_message = """
🤖 Добро пожаловать в RAG Bot для QuantumForge Software!

Я помогу вам найти информацию в корпоративной базе знаний.

Просто задайте мне вопрос, и я найду ответ в наших документах.

Используйте /help для получения дополнительной информации.
        """
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_message = """
📚 Доступные команды:

/start - Начать работу с ботом
/help - Показать это сообщение
/about - Информация о боте

❓ Как использовать:
Просто отправьте мне вопрос на английском языке, например:
• What is Magical Power?
• Who is Koschei the Deathless?
• Tell me about Magic Sword

⚡ Особенности:
• Ответы основаны только на документах из базы знаний
• Если информации нет в БД, я честно скажу "I don't know"
• Защита от вредоносных запросов
        """
        await update.message.reply_text(help_message)

    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /about"""
        about_message = """
ℹ️ О боте:

Этот бот использует технологию RAG (Retrieval-Augmented Generation):
• 📊 Векторный поиск по базе знаний
• 🧠 Few-shot prompting для улучшения ответов
• 🔗 Chain-of-Thought для пошагового рассуждения
• 🛡️ Защита от prompt injection

База знаний содержит 32 документа о вселенной QuantumForge Software.

Разработано для проектной работы Яндекс Практикум.
        """
        await update.message.reply_text(about_message)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений от пользователя"""
        user_query = update.message.text
        user_id = update.effective_user.id
        username = update.effective_user.username or "Unknown"

        logger.info(f"Query from {username} (ID: {user_id}): {user_query}")

        # Отправляем индикатор "печатает..."
        await update.message.chat.send_action(action="typing")

        try:
            # Получаем ответ от RAG бота
            result = self.rag_bot.answer_query(user_query, verbose=False)

            # Формируем ответ
            answer = result["answer"]
            sources = result["sources"]

            # Форматируем ответ для Telegram
            formatted_answer = self.format_markdown_for_telegram(answer)

            # Добавляем вступление в зависимости от типа вопроса (если есть ответ)
            if result["has_answer"]:
                query_lower = user_query.lower()
                if "what is" in query_lower or "what are" in query_lower:
                    formatted_answer = "📖 <i>Based on the knowledge base:</i>\n\n" + formatted_answer
                elif "who is" in query_lower or "who are" in query_lower:
                    formatted_answer = "📖 <i>According to the documents:</i>\n\n" + formatted_answer
                elif "how" in query_lower:
                    formatted_answer = "📖 <i>The knowledge base explains:</i>\n\n" + formatted_answer
                else:
                    formatted_answer = "📖 <i>Here's what I found:</i>\n\n" + formatted_answer

            # Добавляем источники к ответу, если они есть
            if sources and result["has_answer"]:
                sources_text = "\n\n📚 <b>Источники:</b>\n" + "\n".join(
                    f"• <code>{source}</code>" for source in sources
                )
                full_answer = formatted_answer + sources_text
            else:
                full_answer = formatted_answer

            # Отправляем ответ пользователю с HTML форматированием
            await update.message.reply_text(full_answer, parse_mode="HTML")

            logger.info(f"Response sent to {username}: has_answer={result['has_answer']}")

        except Exception as e:
            logger.error(f"Error processing query from {username}: {str(e)}")
            error_message = (
                "❌ Произошла ошибка при обработке вашего запроса. "
                "Пожалуйста, попробуйте еще раз или переформулируйте вопрос."
            )
            await update.message.reply_text(error_message)

    def run(self):
        """Запуск бота в режиме polling"""
        logger.info("Starting Telegram bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Точка входа для запуска бота"""
    # Загружаем переменные окружения
    load_dotenv()

    # Получаем токен из переменных окружения
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN not found in environment variables. "
            "Please set it in .env file or export it."
        )

    # Путь к директории с данными
    data_dir = os.getenv("DATA_DIR", "data")

    # Создаем и запускаем бота
    bot = TelegramRAGBot(token=token, data_dir=data_dir)
    bot.run()


if __name__ == "__main__":
    main()
