#!/usr/bin/env python3
"""
Translate HTML articles to Russian
"""
import re
import os
from pathlib import Path

# Simple translation dictionary for common terms
TRANSLATIONS = {
    # Headers and meta
    "Read Time:": "Время чтения:",
    "Industry Analysis": "Анализ индустрии",
    "Project Management": "Управление проектами",
    "Market Analysis": "Анализ рынка",
    "Monetization & Community": "Монетизация и сообщество",
    "Updated:": "Обновлено:",
    "November": "Ноябрь",
    "min read": "мин чтения",

    # Common terms
    "Article": "Статья",
    "of": "из",
    "Game Design Insights Series": "Серия инсайтов игрового дизайна",

    # Section headers
    "Why some games go viral and others don't": "Почему одни игры становятся вирусными, а другие нет",
    "Pattern 1: the unexpected win mechanic": "Паттерн 1: механика неожиданной победы",
    "The Psychology:": "Психология:",
    "Why It Works:": "Почему это работает:",
    "Industry Examples:": "Примеры из индустрии:",
    "Implementation Formula:": "Формула реализации:",
    "Design Checklist:": "Чек-лист дизайна:",
    "Testing Benchmark:": "Тестовый бенчмарк:",

    # Navigation
    "Get Free Audit": "Получить бесплатный аудит",
    "Get expert insights on game dev survival": "Получите экспертные инсайты о выживании в геймдеве",
    "Monthly Insights": "Ежемесячные инсайты",
    "Wild Forest Studio": "Wild Forest Studio"
}

def translate_text(text):
    """Simple translation using dictionary"""
    for eng, rus in TRANSLATIONS.items():
        text = text.replace(eng, rus)
    return text

def translate_html_file(input_file, output_file):
    """Translate HTML file content"""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Translate text content (basic approach)
    content = translate_text(content)

    # Write translated content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Main translation function"""
    articles_ru_dir = Path("f:/Projects/101/Land/articles-ru")
    articles_dir = Path("f:/Projects/101/Land/articles")

    # Process articles 1-7
    for i in range(1, 8):
        ru_file = articles_ru_dir / f"article-{i}.html"
        en_file = articles_dir / f"article-{i}.html"

        if ru_file.exists() and en_file.exists():
            print(f"Translating article-{i}.html...")
            translate_html_file(en_file, ru_file)
            print(f"✓ Translated {ru_file.name}")
        else:
            print(f"⚠ Warning: Files not found for article-{i}")

    print("\nTranslation complete!")

if __name__ == "__main__":
    main()