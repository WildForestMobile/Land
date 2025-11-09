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

    # Game titles and companies
    "Among Us": "Among Us",
    "Vampire Survivors": "Vampire Survivors",
    "Fall Guys": "Fall Guys",
    "Balatro": "Balatro",
    "Slay the Spire": "Slay the Spire",
    "Gang Beasts": "Gang Beasts",
    "Lethal Company": "Lethal Company",
    "Human Fall Flat": "Human Fall Flat",
    "Dead Cells": "Dead Cells",
    "Phasmophobia": "Phasmophobia",
    "Enter the Gungeon": "Enter the Gungeon",

    # Common phrases
    "was a dead game": "была мертвой игрой",
    "for 2 years": "2 года",
    "before exploding to": "прежде чем взорваться до",
    "downloads": "скачиваний",
    "looked like a flash game": "выглядела как флэш-игра",
    "from": "года",
    "yet made": "но заработала",
    "launched into a market": "вышла на рынок",
    "saturated with": "насыщенный",
    "battle royales": "battle royale",
    "and became a cultural phenomenon": "и стала культурным феноменом",
    "What separates games": "Что отличает игры",
    "that organically spread": "которые органично распространяются",
    "across social media": "в социальных сетях",
    "from those that fade": "от тех, что угасают",
    "despite million-dollar": "несмотря на миллионные",
    "marketing budgets": "бюджеты маркетинга",
    "After analyzing": "После анализа",
    "viral hits": "вирусных хитов",
    "from the past": "за последние",
    "years": "лет",
    "and dissecting": "и разбора",
    "what made them": "что сделало их",
    "shareable": "достойными репостов",
    "we've identified": "мы выделили",
    "seven repeating patterns": "семь повторяющихся паттернов",
    "These aren't marketing tactics": "Это не маркетинговые тактики",
    "These are design decisions": "Это дизайнерские решения",
    "baked into gameplay": "встроенные в геймплей",
    "that trigger player": "которые запускают",
    "sharing behavior": "поведение игроков по шерингу",
    "automatically": "автоматически",
    "Here's the framework": "Вот фреймворк",
    "that separates": "который отделяет",
    "viral games": "вирусные игры",
    "from invisible ones": "от невидимых",
    "Players share moments": "Игроки делятся моментами",
    "that make them feel": "которые заставляют их чувствовать",
    "clever, lucky, or both": "себя умными, удачливыми или и тем, и другим",
    "When your game creates": "Когда ваша игра создает",
    "I can't believe that worked": "я не могу поверить, что это сработало",
    "situations": "ситуации",
    "players instinctively reach": "игроки инстинктивно тянутся",
    "for the screenshot button": "к кнопке скриншота",
    "Creates ego-boosting moments": "Создает моменты, повышающие самооценку",
    "worth broadcasting": "достойные трансляции",
    "Generates unique stories": "Генерирует уникальные истории",
    "per player": "для каждого игрока",
    "Builds mythology around": "Строит мифологию вокруг",
    "impossible": "невозможных",
    "plays": "побед",
    "Random weapon evolution": "Случайные комбинации эволюции оружия",
    "combinations create": "создают",
    "unexpected power spikes": "неожиданные всплески силы",
    "Players discover synergies": "Игроки открывают синергии",
    "organically and rush to share": "органично и спешат поделиться",
    "Wait till you see THIS combo": '"Подожди, пока увидишь ЭТУ комбо"',
    "became the game's viral engine": "стало вирусным двигателем игры",
    "Result:": "Результат:",
    "YouTube videos": "видео на YouTube",
    "mostly user-generated content": "в основном пользовательского контента",
    "Poker hand combinations": "Комбинации покерных рук",
    "that shouldn't work mathematically": "которые математически не должны работать",
    "Players screenshot": "Игроки скринят",
    "absurd score multipliers": "абсурдные множители очков",
    "Community shares": "Сообщество делится",
    "my craziest run": "моим самым безумным забегом",
    "constantly": "постоянно",
    "copies in first month": "копий в первый месяц",
    "from organic sharing": "от органического распространения",
    "Deck synergies": "Синергии колод",
    "that create one-turn kills": "создающие убийства за один ход",
    "Infinite": "Бесконечные",
    "combos that technically shouldn't be possible": "комбо, которые технически не должны быть возможны",
    "Every Ascension": "Каждая Ascension",
    "win felt worth sharing": "победа казалась достойной шеринга",
    "Where:": "Где:",
    "Skill Floor =": "Базовый Навык =",
    "accessible enough to happen": "достаточно доступно, чтобы случалось",
    "Luck Ceiling =": "Потолок Удачи =",
    "impressive when it does": "впечатляет, когда случается",
    "Visual Feedback =": "Визуальная Обратная Связь =",
    "Unmistakable": "Недвусмысленный",
    "this was special": "это было особенным",
    "signal": "сигнал",
    "Mechanic can be executed": "Механику могут выполнить",
    "by 50%+": "50%+",
    "of players": "игроков",
    "Result varies by": "Результат варьируется в",
    "3-5x": "3-5 раз",
    "based on luck/timing": "в зависимости от удачи/тайминга",
    "Visual/audio feedback": "Визуальная/звуковая обратная связь",
    "clearly signals": "четко сигнализирует",
    "exceptional moment": "исключительный момент",
    "Shareable format": "Формат для шеринга",
    "screenshot or": "скриншот или",
    "10-30 second clip": "клип 10-30 секунд",
    "If fewer than": "Если менее",
    "30%": "30%",
    "of play sessions": "игровых сессий",
    "generate at least one": "генерируют хотя бы одну",
    "unexpected win": "неожиданную победу",
    "increase the luck ceiling": "увеличьте потолок удачи",
    "Some mechanics are more impressive": "Некоторые механики более впечатляют",
    "when witnessed than when played": "при просмотре, чем при игре",
    "These create natural": "Они создают естественные",
    "content generation engines": "генераторы контента",
    "Takes": "Занимает",
    "5-30 seconds": "5-30 секунд",
    "perfect clip length": "идеальная длина клипа",
    "Looks more complex": "Выглядит сложнее",
    "than it is": "чем есть на самом деле",
    "Never plays out": "Никогда не разворачивается",
    "exactly the same way twice": "точно так же дважды",
    "Generates its own narrative": "Генерирует собственный нарратив",
    "you had to see this": "ты должен был это увидеть",
    "Physics-based chaos": "Хаос на основе физики",
    "that looks hilarious": "который выглядит уморительно",
    "in clips": "в клипах",
    "Every knockout is unique": "Каждый нокаут уникален",
    "and shareable": "и достоин шеринга",
    "Became YouTube/Twitch gold": "Стал золотом YouTube/Twitch",
    "despite simple mechanics": "несмотря на простые механики",
    "73%": "73%",
    "of marketing was": "маркетинга было",
    "user-generated content": "пользовательским контентом",
    "Voice-activated monster encounters": "Встречи с монстрами, активируемые голосом",
    "Friends screaming in proximity chat": "Друзья кричат в proximity чате",
    "viral clips": "вирусные клипы",
    "Horror + comedy combo": "Комбо ужас + комедия",
    "maximum shareability": "максимальная шербильность",
    "$2M revenue with zero marketing budget": "$2M дохода с нулевым бюджетом маркетинга",
    "Clumsy physics creates": "Неуклюжая физика создает",
    "slapstick moments": "моменты слэпстика",
    "Friends watching =": "Друзья смотрят =",
    "always funnier than": "всегда смешнее, чем",
    "playing alone": "играть одному",
    "40M+ copies sold": "40M+ копий продано",
    "primarily from": "в основном от",
    "streamer/clip virality": "вирусности стримеров/клипов",
    "Shareability Score =": "Оценка Шербильности =",
    "Visual Impact ×": "Визуальный Эффект ×",
    "Unpredictability ×": "Непредсказуемость ×",
    "Social Context": "Социальный Контекст",
    "Guaranteed viral potential": "Гарантированный вирусный потенциал",
    "Strong organic sharing": "Сильное органическое распространение",
    "Below 70": "Ниже 70",
    "Needs paid marketing": "Нужен платный маркетинг",
    "to spread": "для распространения",
    "How impressive it looks": "Насколько впечатляюще выглядит",
    "How much it varies": "Насколько сильно варьируется",
    "each time": "каждый раз",
    "How much better it is": "Насколько лучше с",
    "with audience": "аудиторией",
    "Identify your core loop's": "Определите",
    "peak moment": "пиковый момент",
    "Add": "Добавьте",
    "2-3 variables": "2-3 переменные",
    "that randomize": "которые рандомизируют",
    "outcomes": "исходы",
    "Amplify visual feedback": "Увеличьте визуальную обратную связь",
    "by 200-300%": "на 200-300%",
    "Add social layer": "Добавьте социальный слой",
    "reactions, voice chat, spectating": "реакции, голосовой чат, наблюдение",
    "Warning:": "Предупреждение:",
    "If players can master": "Если игроки могут освоить",
    "the mechanic completely": "механику полностью",
    "it stops being shareable": "она перестает быть достойной шеринга",
    "Maintain chaos": "Поддерживайте хаос",
    "Players don't share": "Игроки не делятся",
    "dominant victories": "доминирующими победами",
    "They share moments": "Они делятся моментами",
    "they barely survived": "когда едва выжили",
    "against impossible odds": "против невозможных шансов",
    "The Data:": "Данные:",
    "Comfortable wins:": "Комфортные победы:",
    "8% share rate": "8% рейтинг шеринга",
    "Close calls": "Близкие победы",
    "victory margin <10%": "отрыв победы <10%",
    "67% share rate": "67% рейтинг шеринга",
    "Last-second victories:": "Победы в последний момент:",
    "89% share rate": "89% рейтинг шеринга",
    "Close calls create emotional intensity": "Близкие победы создают эмоциональную интенсивность",
    "that demands an outlet": "которая требует выхода",
    "Sharing is that outlet": "Шеринг - это выход",
    "Health systems that create": "Системы здоровья, создающие",
    "1 HP boss kills": "убийства боссов с 1 HP",
    "Timer-based doors": "Двери с таймером",
    "force risky decisions": "заставляют принимать рискованные решения",
    "Community built around": "Сообщество построено вокруг",
    "clutch moments": "clutch моментов",
    "10M+ sales driven by": "10M+ продаж, движимых",
    "highlight culture": "культурой хайлайтов",
    "Sanity mechanic creates": "Механика sanity создает",
    "last-second escapes": "побеги в последний момент",
    "Ghost hunts that end": "Охота на призраков, заканчивающаяся",
    "with players hiding": "тем, что игроки прячутся",
    "in lockers": "в шкафах",
    "We barely made it": '"Мы едва справились"',
    "stories fuel the community": "истории питают сообщество",
    "$50M+ revenue with": "$50M+ дохода с",
    "10-person team": "командой из 10 человек",
    "Dodge roll mechanics": "Механики dodge roll",
    "that allow frame-perfect": "позволяющие frame-perfect",
    "escapes": "побеги",
    "Boss fights designed": "Босс-файты, спроектированные",
    "for dramatic final moments": "для драматичных финальных моментов",
    "Half-heart runs": "Забеги с половиной сердца",
    "celebrated as": "празднуемые как",
    "peak gameplay": "пик геймплея",
    "The 40-50 Rule:": "Правило 40-50:",
    "40-50%": "40-50%",
    "of sessions should end": "сессий должны заканчиваться",
    "in a close call": "близкой победой",
    "within 10%": "в пределах 10%",
    "of failure": "от провала",
    "Pseudocode for": "Псевдокод для",
    "dynamic difficulty": "динамической сложности",
    "if player_health > 70%:": "if player_health > 70%:",
    "enemy_damage *= 1.2": "enemy_damage *= 1.2",
    "spawn_rate *= 1.15": "spawn_rate *= 1.15",
    "if player_health < 30%:": "if player_health < 30%:",
    "enemy_damage *= 0.8": "enemy_damage *= 0.8",
    "spawn_rate *= 0.9": "spawn_rate *= 0.9",
    "health_drop_rate *= 1.5": "health_drop_rate *= 1.5",
    "Result: Natural rubber-banding": "Результат: Естественное rubber-banding",
    "toward close calls": "к близким победам",
    "Design Patterns:": "Паттерны дизайна:",
    "Health Gates:": "Health Gates:",
    "Keep players between": "Держите игроков между",
    "20-40% health": "20-40% здоровья",
    "Timer Pressure:": "Timer Pressure:",
    "Last 10%": "Последние 10%",
    "of time = 90%": "времени = 90%",
    "of tension": "напряжения",
    "Resource Scarcity:": "Resource Scarcity:",
    "Force": "Заставляйте",
    "do I use this now": "использовать ли это сейчас",
    "decisions": "решения",
    "Comeback Mechanics:": "Comeback Mechanics:",
    "Give losing players": "Давайте проигрывающим игрокам",
    "tools to clutch": "инструменты для clutch",

    # Article titles
    "The 7 Virality Patterns That Made Indie Games Explode": "7 паттернов вирусности, которые взорвали инди-игры",
    "The 7 virality patterns that made indie games explode": "7 паттернов вирусности, которые взорвали инди-игры",
    "The DNA of Successful Games: Patterns That Separate Hits from Misses": "ДНК успешных игр: Паттерны, которые отделяют хиты от промахов",
    "Crisis-Proof Game Development: Systems That Survive When Everything Goes Wrong": "Кризисоустойчивый геймдев: Системы, которые выживают, когда все идет не так",
    "The Genre Twist Method: Finding Million-Dollar White Spaces in \"Saturated\" Markets": "Метод жанрового твиста: Поиск миллионных белых пространств в 'насыщенных' рынках",
    "Steam Visibility Playbook: The Algorithm Formula for Organic Wishlist Growth": "Плейбук видимости Steam: Формула алгоритма для органического роста вишлистов",
    "The 5 Metrics That Actually Predict Game Success (Before You Launch)": "5 метрик, которые действительно предсказывают успех игры (до запуска)",
    "Early Access Done Right: How to Turn Beta Players Into Revenue and Advocates": "Ранний доступ правильно: Как превратить бета-игроков в доход и адвокатов"
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

    # Fix lang attribute
    content = content.replace('lang="en"', 'lang="ru"')

    # Translate text content (basic approach)
    content = translate_text(content)

    # Update meta tags and title
    content = re.sub(
        r'<meta property="og:title" content="([^"]*)">',
        lambda m: f'<meta property="og:title" content="{translate_text(m.group(1))}">',
        content
    )

    content = re.sub(
        r'<meta name="twitter:title" content="([^"]*)">',
        lambda m: f'<meta name="twitter:title" content="{translate_text(m.group(1))}">',
        content
    )

    content = re.sub(
        r'<title>([^<]*)</title>',
        lambda m: f'<title>{translate_text(m.group(1))}</title>',
        content
    )

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