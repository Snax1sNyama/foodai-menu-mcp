# init_db.py
import sqlite3
from menu_data import MENU_DATABASE

def calculate_satiety(calories: int) -> int:
    """
    Формула сытности: 1000 ккал = 100 сытности.
    Максимум 100. Если калорий нет, ставим 50.
    """
    if not calories:
        return 50
    return min(100, int(calories / 10))

def init_db():
    # Подключаемся к файлу базы данных (он создастся автоматически)
    conn = sqlite3.connect('foodai_menu.db')
    cursor = conn.cursor()

    # Удаляем старые таблицы, если они есть (чтобы не было ошибок при перезапуске)
    cursor.execute('DROP TABLE IF EXISTS dishes')
    cursor.execute('DROP TABLE IF EXISTS restaurants')

    # 1. Таблица ресторанов
    cursor.execute('''
        CREATE TABLE restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # 2. Таблица блюд (связана с рестораном по restaurant_id)
    cursor.execute('''
        CREATE TABLE dishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            name TEXT NOT NULL,
            section TEXT,
            price REAL,
            calories INTEGER,
            satiety INTEGER,
            description TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
        )
    ''')

    # 3. Заполняем базу данными из твоего словаря
    for rest_name, dishes in MENU_DATABASE.items():
        # Добавляем ресторан
        cursor.execute('INSERT INTO restaurants (name) VALUES (?)', (rest_name,))
        rest_id = cursor.lastrowid # Получаем ID только что созданного ресторана

        # Добавляем блюда этого ресторана
        for dish in dishes:
            satiety = calculate_satiety(dish.get('calories', 0))
            cursor.execute('''
                INSERT INTO dishes (restaurant_id, name, section, price, calories, satiety, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                rest_id,
                dish.get('name'),
                dish.get('section'),
                dish.get('price'),
                dish.get('calories', 0),
                satiety,
                dish.get('description', '')
            ))

    conn.commit()
    conn.close()
    print("✅ База данных 'foodai_menu.db' успешно создана и заполнена!")

if __name__ == "__main__":
    init_db()