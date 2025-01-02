import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import os

# Убедитесь, что путь к файлу и выходная папка правильные
CSV_FILE_PATH = "vacancies_2024.csv"
OUTPUT_DIR = "static/images"

# Убедитесь, что папка для графиков существует
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Загрузка данных с подавлением предупреждений
data = pd.read_csv(CSV_FILE_PATH, dtype={'key_skills': str}, low_memory=False)

# Фильтрация вакансий для DevOps
data = data[data['name'].str.contains("devops", case=False, na=False)]

# Очистка данных: исключение некорректных записей
data = data[
    (data['salary_to'].fillna(0) < 10_000_000) |
    (data['salary_from'].fillna(0) < 10_000_000)
]

# Преобразование столбца published_at в дату с учетом UTC
data['published_at'] = pd.to_datetime(data['published_at'], errors='coerce', utc=True)

# Извлечение года из столбца published_at
data['published_year'] = data['published_at'].dt.year

# --- График 1: Динамика уровня зарплат по годам ---
salary_by_year = data.groupby('published_year')[['salary_from', 'salary_to']].mean()
plt.figure(figsize=(10, 6))
plt.plot(salary_by_year.index, salary_by_year['salary_from'], label='Зарплата от')
plt.plot(salary_by_year.index, salary_by_year['salary_to'], label='Зарплата до')
plt.title("Динамика уровня зарплат по годам (DevOps)")
plt.xlabel("Год")
plt.ylabel("Средняя зарплата (руб.)")
plt.legend()
plt.grid()
plt.savefig(f"{OUTPUT_DIR}/salary_by_year.png")

# --- График 2: Динамика количества вакансий по годам ---
vacancies_by_year = data.groupby('published_year').size()
plt.figure(figsize=(10, 6))
plt.bar(vacancies_by_year.index, vacancies_by_year.values, color='skyblue')
plt.title("Динамика количества вакансий по годам (DevOps)")
plt.xlabel("Год")
plt.ylabel("Количество вакансий")
plt.grid()
plt.savefig(f"{OUTPUT_DIR}/vacancies_by_year.png")

# --- График 3: Уровень зарплат по городам ---
salary_by_city = data.groupby('area_name')[['salary_from', 'salary_to']].mean().sort_values('salary_to', ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.barh(salary_by_city.index, salary_by_city['salary_to'], color='green')
plt.title("Уровень зарплат по городам (DevOps)")
plt.xlabel("Средняя зарплата (руб.)")
plt.ylabel("Города")
plt.grid()
plt.savefig(f"{OUTPUT_DIR}/salary_by_city.png")

# --- График 4: Доля вакансий по городам ---
vacancies_by_city = data['area_name'].value_counts(normalize=True).head(10)

plt.figure(figsize=(10, 8))  # Увеличиваем размер графика
plt.pie(
    vacancies_by_city.values,
    labels=vacancies_by_city.index,
    autopct='%1.1f%%',
    startangle=140,
    colors=plt.cm.tab10.colors,
    textprops={'fontsize': 12},  # Увеличиваем шрифт текста
    labeldistance=1.1  # Увеличиваем расстояние подписей от центра
)
plt.title("Доля вакансий по городам (DevOps)", fontsize=16, pad=20)  # Увеличиваем заголовок
plt.tight_layout()  # Оптимизируем размещение
plt.savefig(f"{OUTPUT_DIR}/vacancies_by_city.png")


# --- График 5: ТОП-20 навыков ---
data['key_skills'] = data['key_skills'].fillna('')
data['key_skills'] = data['key_skills'].apply(lambda x: x.split(','))
skills_counter = Counter([skill.strip() for skills in data['key_skills'] for skill in skills])
top_skills = skills_counter.most_common(20)

skills, counts = zip(*top_skills)
plt.figure(figsize=(12, 8))  # Увеличиваем размер графика
plt.barh(skills, counts, color='purple')

# Настройка меток
plt.title("ТОП-20 навыков (DevOps)", fontsize=16, pad=20)  # Увеличиваем заголовок
plt.xlabel("Количество упоминаний", fontsize=14, labelpad=10)
plt.ylabel("Навыки", fontsize=14, labelpad=10)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.gca().invert_yaxis()  # Инвертируем ось Y для лучшего отображения
plt.tight_layout()  # Оптимизируем размещение элементов
plt.savefig(f"{OUTPUT_DIR}/top_skills.png")


print("Графики успешно сохранены в папку:", OUTPUT_DIR)
