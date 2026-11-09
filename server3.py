import re
from fastmcp import FastMCP
from typing import List, Dict, Any

mcp = FastMCP("FoodAI-Menu")

MENU_DATABASE = {
    "kfc": [
        {"name": "Шефбургер Де Люкс", "section": "бургеры", "price": 289, "calories": 550,
         "description": "Сытный обед"},
        {"name": "Чизбургер", "section": "бургеры", "price": 119, "calories": 300, "description": "Легкий перекус"},
        {"name": "Баскет Рост (острый)", "section": "закуски", "price": 349, "calories": 800,
         "description": "На компанию"},
        {"name": "Стрипсы (3 шт)", "section": "закуски", "price": 219, "calories": 410,
         "description": "Легкий голод закроет"},
        {"name": "Картофель фри (средний)", "section": "гарниры", "price": 135, "calories": 340,
         "description": "К бургеру"},
        {"name": "Картофельное пюре", "section": "гарниры", "price": 99, "calories": 150,
         "description": "Легкий гарнир"},
    ],
    "додо пицца": [
        {"name": "Пицца Пепперони", "section": "пицца", "price": 709, "calories": 1200, "description": "На компанию"},
        {"name": "Пицца Маргарита", "section": "пицца", "price": 549, "calories": 860,
         "description": "Классический обед"},
        {"name": "Додошки (чесночные)", "section": "закуски", "price": 219, "calories": 450,
         "description": "Перекус с запасом"},
        {"name": "Картофель из печи с соусом", "section": "закуски", "price": 239, "calories": 320,
         "description": "Легкий перекус"},
    ],
    "вкусно и точка": [
        {"name": "Биг Спешиал", "section": "бургеры", "price": 341, "calories": 720, "description": "Нормальный обед"},
        {"name": "Гранд Де Люкс", "section": "бургеры", "price": 279, "calories": 650, "description": "Сытный перекус"},
        {"name": "Чизбургер", "section": "бургеры", "price": 99, "calories": 300,
         "description": "Легкий голод закроет"},
        {"name": "Картофель фри средний", "section": "гарниры", "price": 110, "calories": 340,
         "description": "К бургеру"},
    ],
    "burger king": [
        {"name": "Двойной Воппер", "section": "бургеры", "price": 289, "calories": 850, "description": "Очень сытный"},
        {"name": "Трюфель Кинг", "section": "бургеры", "price": 209, "calories": 450, "description": "Средний обед"},
        {"name": "Чикенбургер Классик", "section": "бургеры", "price": 69, "calories": 250,
         "description": "Легкий перекус"},
        {"name": "Салат Цезарь", "section": "салаты", "price": 289, "calories": 310, "description": "Легкий обед"},
    ],
    "rostic's": [
        {"name": "Баскет L 24 Острых Крылышка", "section": "баскеты", "price": 1379, "calories": 1500,
         "description": "На большую компанию"},
        {"name": "Мега Ролл острый", "section": "роллы", "price": 519, "calories": 650,
         "description": "Сытный перекус"},
        {"name": "Дабл чикен оригинальный", "section": "бургеры", "price": 439, "calories": 550,
         "description": "Нормальный обед"},
        {"name": "Баскет Фри", "section": "гарниры", "price": 309, "calories": 400, "description": "К курице"},
    ],
    "крошка картошка": [
        {"name": "Большой печёный картофель", "section": "картофель", "price": 135, "calories": 300,
         "description": "Основа обеда"},
        {"name": "Сырный с ветчиной", "section": "наполнители", "price": 135, "calories": 200,
         "description": "Сытная добавка"},
        {"name": "Говядина в сырном соусе", "section": "наполнители", "price": 228, "calories": 250,
         "description": "Мясная добавка"},
    ],
    "папа джонс": [
        {"name": "Пицца Пепперони", "section": "пицца", "price": 720, "calories": 1100, "description": "На компанию"},
        {"name": "Пицца 4 сыра", "section": "пицца", "price": 780, "calories": 1300, "description": "Сытный обед"},
        {"name": "Хлебные палочки с сыром", "section": "закуски", "price": 190, "calories": 450,
         "description": "Легкий перекус"},
    ],
    "subway": [
        {"name": "Сабы 15 см (Индейка)", "section": "сабы", "price": 250, "calories": 350,
         "description": "Легкий обед"},
        {"name": "Сабы 30 см (БМТ)", "section": "сабы", "price": 450, "calories": 700, "description": "Сытный обед"},
        {"name": "Печенье с шоколадом", "section": "десерты", "price": 60, "calories": 200, "description": "К кофе"},
    ],
    "chicko": [
        {"name": "Цыпленок гриль (половина)", "section": "курица", "price": 450, "calories": 600,
         "description": "Сытный обед"},
        {"name": "Крылья BBQ (6 шт)", "section": "курица", "price": 390, "calories": 480,
         "description": "Средний перекус"},
        {"name": "Картофель по-деревенски", "section": "гарниры", "price": 180, "calories": 320,
         "description": "К курице"},
    ],

    # --- Азиатская ---
    "тануки": [
        {"name": "Ролл Филадельфия", "section": "роллы", "price": 689, "calories": 450, "description": "Сытный обед"},
        {"name": "Ролл Калифорния с крабом", "section": "роллы", "price": 489, "calories": 350,
         "description": "Легкий обед"},
        {"name": "Том Ям с креветками", "section": "супы", "price": 590, "calories": 250,
         "description": "Согревающий обед"},
    ],
    "техникум": [
        {"name": "Том Ям с кокосовым молоком", "section": "супы", "price": 690, "calories": 300,
         "description": "Сытный суп"},
        {"name": "Поке с лососем", "section": "салаты", "price": 790, "calories": 400, "description": "Полезный обед"},
        {"name": "Бургер с трюфельным майонезом", "section": "горячее", "price": 890, "calories": 750,
         "description": "Очень сытный"},
    ],
    "якитория": [
        {"name": "Сякэ суси", "section": "суси", "price": 198, "calories": 60, "description": "Легкий перекус"},
        {"name": "Чука гункан", "section": "гунканы", "price": 144, "calories": 80, "description": "Закуска"},
        {"name": "Соус Терияки", "section": "соусы", "price": 74, "calories": 50, "description": "Добавка"},
    ],
    "niyama": [
        {"name": "Филадельфия", "section": "роллы", "price": 839, "calories": 480, "description": "Сытный обед"},
        {"name": "Унаги Чиз", "section": "роллы", "price": 819, "calories": 420, "description": "Средний обед"},
        {"name": "Калифорния", "section": "роллы", "price": 699, "calories": 380, "description": "Легкий обед"},
    ],
    "суши wok": [
        {"name": "Ролл Филадельфия", "section": "роллы", "price": 450, "calories": 420,
         "description": "Бюджетный обед"},
        {"name": "Лапша Wok с курицей", "section": "вок", "price": 320, "calories": 550,
         "description": "Сытный перекус"},
    ],
    "фо бо": [
        {"name": "Фо Бо с говядиной", "section": "супы", "price": 420, "calories": 350,
         "description": "Согревающий обед"},
        {"name": "Бан Ми с говядиной", "section": "сэндвичи", "price": 320, "calories": 450,
         "description": "Сытный перекус"},
    ],

    # --- Кофейни ---
    "stars coffee": [
        {"name": "Капучино", "section": "кофе", "price": 340, "calories": 120, "description": "Классика"},
        {"name": "Сырники миндальные", "section": "завтраки", "price": 330, "calories": 380,
         "description": "Сытный завтрак"},
        {"name": "Круассан миндальный", "section": "выпечка", "price": 260, "calories": 410, "description": "К кофе"},
        {"name": "Сэндвич с ростбифом", "section": "сэндвичи", "price": 440, "calories": 520,
         "description": "Сытный обед"},
    ],
    "cofix": [
        {"name": "Сырники", "section": "завтраки", "price": 150, "calories": 300, "description": "Бюджетный завтрак"},
        {"name": "Салат Цезарь с курицей", "section": "ланчи", "price": 210, "calories": 280,
         "description": "Легкий обед"},
        {"name": "Донат шоколадный", "section": "десерты", "price": 90, "calories": 250, "description": "К кофе"},
    ],
    "drinkit": [
        {"name": "Айс Латте Двойной протеин", "section": "напитки", "price": 515, "calories": 200,
         "description": "Спортивный перекус"},
        {"name": "Баскский чизкейк", "section": "десерты", "price": 280, "calories": 350, "description": "К кофе"},
    ],
    "cofefest": [
        {"name": "Сырники", "section": "завтраки", "price": 170, "calories": 320, "description": "Сытный завтрак"},
        {"name": "Омлет с сосисками", "section": "завтраки", "price": 210, "calories": 400,
         "description": "Плотный завтрак"},
    ],
    "one price coffee": [
        {"name": "Капучино", "section": "кофе", "price": 150, "calories": 110, "description": "Бюджетный кофе"},
        {"name": "Круассан", "section": "выпечка", "price": 120, "calories": 320, "description": "К кофе"},
    ],
    "surf coffee": [
        {"name": "Раф лавандовый", "section": "кофе", "price": 380, "calories": 250, "description": "Авторский кофе"},
        {"name": "Сырники", "section": "завтраки", "price": 450, "calories": 400, "description": "Сытный завтрак"},
    ],
    "теремок": [
        {"name": "Блин с ветчиной и сыром", "section": "блины", "price": 214, "calories": 350,
         "description": "Сытный перекус"},
        {"name": "Блин с сёмгой", "section": "блины", "price": 583, "calories": 400, "description": "Премиум блин"},
        {"name": "Борщ Теремковский", "section": "супы", "price": 415, "calories": 250,
         "description": "Согревающий обед"},
    ],
    "кофе хауз": [
        {"name": "Капучино", "section": "кофе", "price": 280, "calories": 120, "description": "Классика"},
        {"name": "Чизкейк", "section": "десерты", "price": 320, "calories": 380, "description": "К кофе"},
    ],
    "starbucks": [
        {"name": "Фраппучино", "section": "напитки", "price": 450, "calories": 300, "description": "Освежающий"},
        {"name": "Сэндвич с индейкой", "section": "сэндвичи", "price": 380, "calories": 450,
         "description": "Легкий обед"},
    ],

    # --- Русская / Европейская ---
    "братья караваевы": [
        {"name": "Сырники школьные", "section": "завтраки", "price": 200, "calories": 300,
         "description": "Как в детстве"},
        {"name": "Салат Оливье", "section": "салаты", "price": 270, "calories": 350, "description": "Классика"},
        {"name": "Борщ", "section": "супы", "price": 215, "calories": 280, "description": "Согревающий"},
    ],
    "добрынинский": [
        {"name": "Блинчики с мясным фаршем", "section": "блины", "price": 300, "calories": 450,
         "description": "Сытный обед"},
        {"name": "Пицца Баварская мясная", "section": "пицца", "price": 480, "calories": 850,
         "description": "На перекус"},
    ],
    "вареничная №1": [
        {"name": "Вареники с вишней", "section": "вареники", "price": 390, "calories": 380,
         "description": "Сладкий обед"},
        {"name": "Борщ с пампушками", "section": "супы", "price": 470, "calories": 450, "description": "Очень сытно"},
    ],
    "шоколадница": [
        {"name": "Сырники со сметаной", "section": "завтраки", "price": 429, "calories": 450,
         "description": "Сытный завтрак"},
        {"name": "Капучино", "section": "кофе", "price": 290, "calories": 120, "description": "К завтраку"},
    ],
    "му-му": [
        {"name": "Борщ с говядиной", "section": "супы", "price": 210, "calories": 250, "description": "Бюджетный обед"},
        {"name": "Котлета по-киевски", "section": "горячее", "price": 310, "calories": 500,
         "description": "Сытное горячее"},
    ],
    "корчма тарас бульба": [
        {"name": "Деруны со сметаной", "section": "горячее", "price": 320, "calories": 400,
         "description": "Национальное блюдо"},
        {"name": "Сало с чесноком", "section": "закуски", "price": 290, "calories": 600, "description": "Для аппетита"},
    ],
    "ресторан москва": [
        {"name": "Оливье с говядиной", "section": "салаты", "price": 400, "calories": 380, "description": "Классика"},
        {"name": "Медовик", "section": "десерты", "price": 290, "calories": 450, "description": "К чаю"},
    ],
    "портал": [
        {"name": "Том-ям с креветками", "section": "супы", "price": 740, "calories": 350, "description": "Экзотика"},
        {"name": "Рибай", "section": "горячее", "price": 2400, "calories": 800, "description": "Стейк"},
    ],
    "парк": [
        {"name": "Цыплёнок табака", "section": "горячее", "price": 930, "calories": 700, "description": "На компанию"},
        {"name": "Лангустины на мангале", "section": "морепродукты", "price": 1550, "calories": 300,
         "description": "Изысканно"},
    ],
    "столовая цмт": [
        {"name": "Салат куриный с сельдереем", "section": "салаты", "price": 165, "calories": 200,
         "description": "Легкий обед"},
        {"name": "Сёмга отварная", "section": "рыба", "price": 552, "calories": 250, "description": "Полезно"},
    ],

    # --- Кавказская ---
    "veriko": [
        {"name": "Тартар из говядины", "section": "закуски", "price": 1150, "calories": 350,
         "description": "Изысканная закуска"},
        {"name": "Пеновани хачапури", "section": "выпечка", "price": 1450, "calories": 600,
         "description": "Сытная выпечка"},
    ],
    "папа хинкали": [
        {"name": "Хачапури по-аджарски", "section": "выпечка", "price": 600, "calories": 550,
         "description": "Классика"},
        {"name": "Грузинский харчо", "section": "супы", "price": 550, "calories": 300, "description": "Согревающий"},
    ],
    "магари": [
        {"name": "Хинкали со свининой и говядиной", "section": "хинкали", "price": 255, "calories": 150,
         "description": "1 шт"},
        {"name": "Хинкали с сыром", "section": "хинкали", "price": 265, "calories": 120, "description": "1 шт"},
    ],
    "грузинский дворик": [
        {"name": "Рулетики из баклажанов", "section": "закуски", "price": 460, "calories": 250,
         "description": "Легкая закуска"},
        {"name": "Оджахури из свинины", "section": "горячее", "price": 570, "calories": 650,
         "description": "Сытное горячее"},
    ],
    "старик хинкалыч": [
        {"name": "Хинкали со свининой и говядиной", "section": "хинкали", "price": 60, "calories": 150,
         "description": "1 шт"},
        {"name": "Хинкали с говядиной", "section": "хинкали", "price": 85, "calories": 130, "description": "1 шт"},
    ],
    "lari": [
        {"name": "Борщ с говядиной", "section": "супы", "price": 790, "calories": 400, "description": "Сытный обед"},
        {"name": "Аджапсандал", "section": "закуски", "price": 650, "calories": 300, "description": "Овощное рагу"},
    ],
    "грузинский вкус": [
        {"name": "Чахохбили", "section": "горячее", "price": 400, "calories": 500, "description": "Сытное горячее"},
        {"name": "Хачапури по-имеретински", "section": "хачапури", "price": 500, "calories": 550,
         "description": "Сырное наслаждение"},
    ],

    # --- Итальянская ---
    "il patio": [
        {"name": "Пицца Пепперони", "section": "пицца", "price": 690, "calories": 1000, "description": "Классика"},
        {"name": "Паста Карбонара", "section": "паста", "price": 620, "calories": 600, "description": "Сытная паста"},
    ],
    "buono": [
        {"name": "Тальятелле с брокколини", "section": "паста", "price": 2200, "calories": 500,
         "description": "Изысканная паста"},
        {"name": "Филе-миньон с фуа-гра", "section": "горячее", "price": 6500, "calories": 800,
         "description": "Премиум стейк"},
    ],
    "butler": [
        {"name": "Устрица Моари", "section": "морепродукты", "price": 1100, "calories": 50, "description": "1 шт"},
        {"name": "Пицца Маргарита", "section": "пицца", "price": 1200, "calories": 900, "description": "Классика"},
    ],
    "sempre": [
        {"name": "Карбонара", "section": "паста", "price": 900, "calories": 600, "description": "Сытная паста"},
        {"name": "Рибай стейк", "section": "горячее", "price": 1600, "calories": 700, "description": "Стейк"},
    ],
    "probka": [
        {"name": "Вителло тоннато", "section": "закуски", "price": 1290, "calories": 300,
         "description": "Классическая закуска"},
        {"name": "Рубленый стейк", "section": "горячее", "price": 1950, "calories": 600, "description": "Сытный обед"},
    ],

    # --- Fine Dining ---
    "white rabbit": [
        {"name": "Каспийский залом с фуа-гра", "section": "закуски", "price": 1590, "calories": 250,
         "description": "Изысканная закуска"},
        {"name": "Запеченный палтус", "section": "горячее", "price": 2090, "calories": 450,
         "description": "Рыбное блюдо"},
    ],
    "savva": [
        {"name": "Пирог из дичи", "section": "закуски", "price": 2550, "calories": 400, "description": "Русская кухня"},
        {"name": "Филе оленя", "section": "горячее", "price": 3250, "calories": 500, "description": "Сытное горячее"},
    ],
    "selfie": [
        {"name": "Паштет из утки", "section": "закуски", "price": 450, "calories": 300, "description": "К бокалу вина"},
        {"name": "Вырезка оленя", "section": "горячее", "price": 2370, "calories": 450, "description": "Премиум мясо"},
    ],
    "сахалин": [
        {"name": "Жареные гедза с вагю", "section": "закуски", "price": 2800, "calories": 350,
         "description": "Азиатская закуска"},
        {"name": "Дорадо на гриле", "section": "горячее", "price": 750, "calories": 300, "description": "100 г"},
    ],
    "белуга": [
        {"name": "Икра осетровая", "section": "икра", "price": 2280, "calories": 100, "description": "Премиум"},
        {"name": "Котлета из медведя", "section": "горячее", "price": 2750, "calories": 600, "description": "Экзотика"},
    ],
    "турандот": [
        {"name": "Морской ёж с крабом", "section": "закуски", "price": 990, "calories": 200,
         "description": "Деликатес"},
        {"name": "Чилийский сибас", "section": "горячее", "price": 9300, "calories": 500,
         "description": "Рыбное блюдо"},
    ],
    "dr. живаго": [
        {"name": "Бутерброд с щучьей котлетой", "section": "закуски", "price": 680, "calories": 350,
         "description": "Русская закуска"},
        {"name": "Драники со сметаной", "section": "завтраки", "price": 450, "calories": 450,
         "description": "Сытный завтрак"},
    ],
    "чайхона №1": [
        {"name": "Плов с бараниной", "section": "горячее", "price": 2900, "calories": 800,
         "description": "На компанию"},
        {"name": "Люля-кебаб", "section": "шашлык", "price": 950, "calories": 500, "description": "Сытное горячее"},
    ],
}


def _normalize_name(name: str) -> str:
    name = name.lower().strip()
    name = name.replace("—", " ").replace("-", " ")
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name


@mcp.tool()
def get_menu(restaurant_name: str) -> Any:
    """
    Возвращает меню ресторана. Если ресторана нет, возвращает not_found для LLM.
    """
    normalized_query = _normalize_name(restaurant_name)

    for key, menu in MENU_DATABASE.items():
        normalized_key = _normalize_name(key)
        if normalized_key in normalized_query or normalized_query in normalized_key:
            return menu

    # Если ресторана нет в базе, возвращаем сигнал для LLM
    return {
        "status": "not_found",
        "restaurant_name": restaurant_name,
        "message": "Меню нет в базе. Сгенерируй примерное меню, цены и калории."
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")