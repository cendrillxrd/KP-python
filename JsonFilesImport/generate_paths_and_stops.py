import json
import DATABASE.database as db

def extract_points(data):
    """Извлекает данные из ключа "points" во всех вложенных словарях.

    Args:
      data: Исходный JSON-словарь.

    Returns:
      Список списков координат.
    """

    all_points = []
    for feature in data['data']['features'][1]['features']:
        if 'points' in feature:
            all_points.extend(feature['points'])
    all_points = list(map(reversed, all_points))
    return list(map(tuple, all_points))

def extract_stops(data):
    """Извлекает данные из ключа "points" во всех вложенных словарях.

    Args:
      data: Исходный JSON-словарь.

    Returns:
      Список списков координат.
    """

    all_stops = []
    for feature in data['data']['features'][1]['features']:
        if 'coordinates' in feature:
            all_stops.append(feature['coordinates'])
    all_stops = list(map(reversed, all_stops))
    all_stops = list(map(tuple, all_stops))

    all_stops_name = []
    for feature in data['data']['features'][0]['features']:
        if 'name' in feature:
            all_stops_name.append(feature['name'])
    return list(zip(all_stops_name, all_stops))

# Загружаем данные (замените на ваш источник данных)
with open('C:/Users/Admin/PycharmProjects/КП/JsonFilesImport/data7.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Извлекаем точки
result = extract_points(data)
result_stop = extract_stops(data)
print(result)
print()
print(result_stop)

# db.set_bus_stops(result_stop, 7)
# db.set_bus_stops(result_stop, 7)
# Выводим результат (для проверки)

