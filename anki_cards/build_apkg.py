#!/usr/bin/env python3
"""Собирает .apkg с 6 типами карточек Anki в жёлто-зелёно-коричневой теме.

Запуск:
    pip install genanki
    python3 build_apkg.py

Результат: 6-card-types-demo.apkg (импортируется в Anki desktop и AnkiDroid).
"""

import os
import genanki

BASE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(BASE, "templates")

# Фиксированные ID — чтобы повторный импорт обновлял типы, а не плодил дубли.
DECK_ID = 1748000000001
MODEL_BASIC = 1748000000010
MODEL_REVERSED = 1748000000011
MODEL_TYPE = 1748000000012
MODEL_CLOZE = 1748000000013
MODEL_AUDIO = 1748000000014
MODEL_CHOICE = 1748000000015


def read(name):
    with open(os.path.join(TPL, name), encoding="utf-8") as f:
        return f.read()


with open(os.path.join(BASE, "styling.css"), encoding="utf-8") as f:
    CSS = f.read()


# ---------- 1. Basic (Лицо → Оборот) ----------
basic = genanki.Model(
    MODEL_BASIC,
    "Тема · Базовая",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Image"}],
    templates=[{
        "name": "Карточка",
        "qfmt": read("1_basic_front.html"),
        "afmt": read("1_basic_back.html"),
    }],
    css=CSS,
)

# ---------- 2. Basic + Reversed (2 карточки) ----------
reversed_model = genanki.Model(
    MODEL_REVERSED,
    "Тема · Базовая и обратная",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Image"}],
    templates=[
        {
            "name": "Прямая",
            "qfmt": read("2_reversed_card1_front.html"),
            "afmt": read("2_reversed_card1_back.html"),
        },
        {
            "name": "Обратная",
            "qfmt": read("2_reversed_card2_front.html"),
            "afmt": read("2_reversed_card2_back.html"),
        },
    ],
    css=CSS,
)

# ---------- 3. Type-in (ввод ответа) ----------
type_model = genanki.Model(
    MODEL_TYPE,
    "Тема · Ввод ответа",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Image"}],
    templates=[{
        "name": "Карточка",
        "qfmt": read("3_type_front.html"),
        "afmt": read("3_type_back.html"),
    }],
    css=CSS,
)

# ---------- 4. Cloze (пропуски) ----------
cloze_model = genanki.Model(
    MODEL_CLOZE,
    "Тема · Пропуски",
    fields=[{"name": "Text"}, {"name": "Extra"}],
    templates=[{
        "name": "Пропуск",
        "qfmt": read("4_cloze_front.html"),
        "afmt": read("4_cloze_back.html"),
    }],
    css=CSS,
    model_type=genanki.Model.CLOZE,
)

# ---------- 5. Audio / Прослушать ----------
audio_model = genanki.Model(
    MODEL_AUDIO,
    "Тема · Аудио",
    fields=[
        {"name": "Audio"}, {"name": "Word"}, {"name": "Meaning"},
        {"name": "Image"}, {"name": "Hint"},
    ],
    templates=[{
        "name": "Карточка",
        "qfmt": read("5_audio_front.html"),
        "afmt": read("5_audio_back.html"),
    }],
    css=CSS,
)

# ---------- 6. Multiple choice (выбор ответа) ----------
choice_model = genanki.Model(
    MODEL_CHOICE,
    "Тема · Выбор ответа",
    fields=[
        {"name": "Question"}, {"name": "Image"},
        {"name": "Option1"}, {"name": "Option2"},
        {"name": "Option3"}, {"name": "Option4"},
        {"name": "Answer"}, {"name": "Explanation"},
    ],
    templates=[{
        "name": "Карточка",
        "qfmt": read("6_choice_front.html"),
        "afmt": read("6_choice_back.html"),
    }],
    css=CSS,
)


deck = genanki.Deck(DECK_ID, "Демо · 6 типов карточек (жёлто-зелёная тема)")


def add(model, fields):
    deck.add_note(genanki.Note(model=model, fields=fields))


# 1. Базовая
add(basic, ["Столица Австралии?", "Канберра", ""])
add(basic, [r"Сколько будет \(7 \times 8\)?", "56", ""])
add(basic, [
    "Какая теорема связывает стороны этого треугольника?",
    r"Теорема Пифагора: \(a^2 + b^2 = c^2\)",
    '<img src="triangle.svg">',
])

# 2. Базовая и обратная
add(reversed_model, ["hydrogen", "водород", ""])
add(reversed_model, ["π (число пи) ≈", "3.14159", ""])

# 3. Ввод ответа
add(type_model, ["Столица Японии?", "Токио", ""])
add(type_model, [r"\(12 \times 12 = {?}\)", "144", ""])

# 4. Пропуски
add(cloze_model, [
    r"Теорема Пифагора: {{c1::\(a^2 + b^2 = c^2\)}}",
    "Связывает катеты и гипотенузу прямоугольного треугольника.",
])
add(cloze_model, ["Самая длинная река в мире — {{c1::Нил}}.", ""])

# 5. Аудио (поле Audio пустое → озвучит TTS; свой звук: [sound:файл.mp3])
add(audio_model, ["", "lattice", "решётка (в т.ч. кристаллическая)", "",
                  "термин из математики и кристаллографии"])
add(audio_model, ["", "integral", "интеграл", "", ""])

# 6. Выбор ответа
add(choice_model, [
    "Как переводится слово «lattice»?", "",
    "решётка", "лестница", "широта", "кружево",
    "1",
    "lattice — решётка; lace — кружево, latitude — широта.",
])
add(choice_model, [
    r"Чему равна производная \(\frac{d}{dx}x^3\)?", "",
    r"\(3x^2\)", r"\(x^2\)", r"\(3x\)", r"\(x^3\)",
    "1",
    r"По правилу степени \(\frac{d}{dx}x^n = n\,x^{n-1}\).",
])
add(choice_model, [
    "Какая фигура изображена?", '<img src="triangle.svg">',
    "Прямоугольный треугольник", "Равносторонний треугольник",
    "Квадрат", "Окружность",
    "1",
    "Прямой угол отмечен квадратиком в нижнем левом углу.",
])


pkg = genanki.Package(deck)
pkg.media_files = [os.path.join(BASE, "media", "triangle.svg")]

out = os.path.join(BASE, "6-card-types-demo.apkg")
pkg.write_to_file(out)
print("Готово:", out)
