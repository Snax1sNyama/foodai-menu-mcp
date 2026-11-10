import sqlite3
import re
import os
import json
from fastmcp import FastMCP
from typing import List, Dict, Any, Union

mcp = FastMCP("FoodAI-Menu")

# 👇 Имя файла базы данных (убедись, что на GitHub лежит именно он)
DB_PATH = 'foodai_menu.db'

def _normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = name.replace("—", " ").replace("-", " ")
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name

@mcp.tool()
def get_menu(restaurant_name: str) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    """Возвращает меню ресторана из базы данных с учетом секций."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Ищем ресторан по частичному совпадению
    cursor.execute("SELECT id, name FROM restaurants WHERE name LIKE ?", (f"%{restaurant_name.lower()}%",))
    rest = cursor.fetchone()

    if not rest:
        conn.close()
        return {
            "status": "not_found",
            "restaurant_name": restaurant_name,
            "message": "Меню нет в базе. Сгенерируй примерное меню, цены, калории и сытность (0-100)."
        }

    # 🚀 JOIN с таблицей sections
    cursor.execute("""
        SELECT 
            d.name, 
            COALESCE(s.name, d.section) as section_name, 
            d.price, 
            d.calories, 
            d.satiety, 
            d.description 
        FROM dishes d
        LEFT JOIN sections s ON d.section_id = s.id
        WHERE d.restaurant_id = ?
    """, (rest["id"],))
    
    dishes = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return dishes


@mcp.tool()
def save_generated_menu(restaurant_name: str, dishes: str) -> str:
    """
    Сохраняет сгенерированное LLM меню в базу данных.
    Автоматически создает секции, если их нет.
    Принимает dishes как JSON-строку.
    """
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

    try:
        dishes_list = json.loads(dishes)
    except Exception:
        dishes_list = []

    for d in dishes_list:
        if not isinstance(d, dict):
            continue
            
        section_name = str(d.get('section', 'сгенерировано')).strip().lower()
        
        # 🚀 Ищем или создаем секцию
        cursor.execute("SELECT id FROM sections WHERE name = ?", (section_name,))
        sec = cursor.fetchone()
        
        if sec:
            section_id = sec[0]
        else:
            cursor.execute("INSERT INTO sections (name) VALUES (?)", (section_name,))
            section_id = cursor.lastrowid

        # Вставляем блюдо
        cursor.execute('''
            INSERT INTO dishes (restaurant_id, name, section, price, calories, satiety, description, section_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            rest_id, 
            d.get('name') or d.get('dish'), 
            section_name,
            d.get('price'), 
            d.get('calories'), 
            d.get('satiety', 50), 
            d.get('description', ''),
            section_id
        ))

    conn.commit()
    conn.close()
    return f"✅ Меню для '{restaurant_name}' сохранено в БД!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
