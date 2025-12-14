#!/usr/bin/env python
"""
Скрипт для оценки качества RAG-бота на golden questions
"""

import sys
sys.path.append("src")

from rag_bot import RAGBot
import time
import json


def load_golden_questions():
    """Загружает golden questions из файла"""
    questions = {
        "known": [
            "What is Synth Flux?",
            "Who is Xarn Velgor?",
            "What is a Photon Blade?",
            "What is the Stellar Hawk?",
            "Who leads the Resistance Coalition?",
            "What was the Battle of Verdantis?",
            "What is the Void Core Station?",
            "Who is Supreme Archon Malakor?",
        ],
        "unknown": [
            "What is the economic system of QuantumVerse?",
            "How does interstellar trade work?",
            "What religions exist in QuantumVerse?",
            "What is the history of Synth Flux creation?",
            "How do quantum tunneling drives work in detail?",
        ]
    }
    return questions


def evaluate_bot():
    """Оценивает качество бота на golden questions"""
    print("=" * 80)
    print("RAG Bot Quality Evaluation")
    print("=" * 80)

    bot = RAGBot()
    questions = load_golden_questions()

    results = {
        "known": [],
        "unknown": [],
        "metrics": {}
    }

    # Тест на known questions
    print("\\n" + "=" * 80)
    print("Testing KNOWN questions (should answer)")
    print("=" * 80)

    correct_answers = 0
    total_time = 0

    for i, question in enumerate(questions["known"], 1):
        start_time = time.time()
        result = bot.answer_query(question)
        elapsed = time.time() - start_time
        total_time += elapsed

        has_answer = result["has_answer"]
        correct_answers += 1 if has_answer else 0

        print(f"\\n[{i}/{len(questions['known'])}] {question}")
        print(f"Status: {'PASS' if has_answer else 'FAIL'}")
        print(f"Time: {elapsed:.2f}s")

        results["known"].append({
            "question": question,
            "answer": result["answer"][:200],
            "has_answer": has_answer,
            "time": elapsed
        })

    known_accuracy = correct_answers / len(questions["known"])
    avg_time_known = total_time / len(questions["known"])

    print(f"\\nKnown Questions Accuracy: {known_accuracy:.2%} ({correct_answers}/{len(questions['known'])})")
    print(f"Average Response Time: {avg_time_known:.2f}s")

    # Тест на unknown questions
    print("\\n" + "=" * 80)
    print("Testing UNKNOWN questions (should refuse)")
    print("=" * 80)

    correct_refusals = 0
    total_time = 0

    for i, question in enumerate(questions["unknown"], 1):
        start_time = time.time()
        result = bot.answer_query(question)
        elapsed = time.time() - start_time
        total_time += elapsed

        refused = not result["has_answer"]
        correct_refusals += 1 if refused else 0

        print(f"\\n[{i}/{len(questions['unknown'])}] {question}")
        print(f"Status: {'PASS' if refused else 'FAIL'}")
        print(f"Time: {elapsed:.2f}s")

        results["unknown"].append({
            "question": question,
            "answer": result["answer"][:200],
            "refused": refused,
            "time": elapsed
        })

    unknown_accuracy = correct_refusals / len(questions["unknown"])
    avg_time_unknown = total_time / len(questions["unknown"])

    print(f"\\nUnknown Questions Accuracy: {unknown_accuracy:.2%} ({correct_refusals}/{len(questions['unknown'])})")
    print(f"Average Response Time: {avg_time_unknown:.2f}s")

    # Итоговые метрики
    overall_accuracy = (correct_answers + correct_refusals) / (len(questions["known"]) + len(questions["unknown"]))

    results["metrics"] = {
        "known_accuracy": known_accuracy,
        "unknown_accuracy": unknown_accuracy,
        "overall_accuracy": overall_accuracy,
        "avg_response_time": (avg_time_known + avg_time_unknown) / 2,
        "total_questions": len(questions["known"]) + len(questions["unknown"])
    }

    # Сохраняем результаты
    with open("logs/evaluation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\\n" + "=" * 80)
    print("FINAL RESULTS")
    print("=" * 80)
    print(f"Overall Accuracy: {overall_accuracy:.2%}")
    print(f"Known Questions: {known_accuracy:.2%}")
    print(f"Unknown Questions: {unknown_accuracy:.2%}")
    print(f"Average Response Time: {results['metrics']['avg_response_time']:.2f}s")
    print("\\nResults saved to: logs/evaluation_results.json")
    print("=" * 80)

    return results


if __name__ == "__main__":
    evaluate_bot()
