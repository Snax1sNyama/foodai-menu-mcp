# server.py
import sqlite3
import re
import os
from fastmcp import FastMCP
from typing import List, Dict, Any, Union

mcp = FastMCP("FoodAI-Menu")
DB_PATH = 'foodai_menu.db'

# Если базы нет (например, на сервере), создаем её
if not os.path.exists(DB_PATH):
    from init_db import init_db
    init_db()

def _normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = name.replace("—", " ").replace("-", " ")
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name

@mcp.tool()
def get_menu(restaurant_name: str) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    """Возвращает меню ресторана из базы данных."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Ищем ресторан (частичное совпадение)
    cursor.execute("SELECT id, name FROM restaurants WHERE name LIKE ?", (f"%{restaurant_name.lower()}%",))
    rest = cursor.fetchone()

    if not rest:
        conn.close()
        return {
            "status": "not_found",
            "restaurant_name": restaurant_name,
            "message": "Меню нет в базе. Сгенерируй примерное меню, цены, калории и сытность (0-100)."
        }

    # Достаем блюда
    cursor.execute("SELECT name, section, price, calories, satiety, description FROM dishes WHERE restaurant_id = ?", (rest["id"],))
    dishes = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return dishes


@mcp.tool()
def save_generated_menu(restaurant_name: str, dishes: List[Dict[str, Any]]) -> str:
    """Сохраняет сгенерированное LLM меню в базу данных."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ищем ресторан, если нет — создаем
    cursor.execute("SELECT id FROM restaurants WHERE name LIKE ?", (f"%{restaurant_name.lower()}%",))
    rest = cursor.fetchone()

    if rest:
        rest_id = rest[0]
    else:
        cursor.execute("INSERT INTO restaurants (name) VALUES (?)", (restaurant_name,))
        rest_id = cursor.lastrowid

    # Вставляем блюда
    for d in dishes:
        cursor.execute('''
            INSERT INTO dishes (restaurant_id, name, section, price, calories, satiety, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            rest_id,
            d.get('name') or d.get('dish'),
            d.get('section', 'сгенерировано'),
            d.get('price'),
            d.get('calories'),
            d.get('satiety', 50),
            d.get('description', '')
        ))

    conn.commit()
    conn.close()
    return f"✅ Меню для '{restaurant_name}' сохранено в БД!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
