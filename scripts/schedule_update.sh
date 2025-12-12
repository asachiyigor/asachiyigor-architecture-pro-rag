#!/bin/bash
# Скрипт для настройки автоматического обновления индекса

# Для Linux/macOS - добавить в crontab
# Запуск каждый день в 6:00
# 0 6 * * * cd /path/to/RAG && /path/to/.venv/bin/python scripts/update_index.py

echo "Setting up automatic index updates..."
echo ""
echo "For Linux/macOS (cron):"
echo "  Run: crontab -e"
echo "  Add: 0 6 * * * cd $(pwd) && $(pwd)/.venv/bin/python scripts/update_index.py"
echo ""
echo "For Windows (Task Scheduler):"
echo "  1. Open Task Scheduler"
echo "  2. Create Basic Task"
echo "  3. Trigger: Daily at 6:00 AM"
echo "  4. Action: Start a Program"
echo "     Program: $(pwd)/.venv/Scripts/python.exe"
echo "     Arguments: scripts/update_index.py"
echo "     Start in: $(pwd)"
echo ""
echo "Manual test:"
echo "  python scripts/update_index.py"
