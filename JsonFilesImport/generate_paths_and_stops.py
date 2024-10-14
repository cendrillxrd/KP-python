import json
import DATABASE.database_2 as db


def extract_points(data, dir):
    all_points = []
    for feature in data['data']['features'][dir]['features']:
        if 'points' in feature:
            all_points.extend(feature['points'])
    all_points = list(map(reversed, all_points))
    return list(map(tuple, all_points))


def extract_stops(data, dir):
    all_stops = []
    for feature in data['data']['features'][dir]['features']:
        if 'coordinates' in feature:
            all_stops.append(feature['coordinates'])
    all_stops = list(map(reversed, all_stops))
    all_stops = list(map(tuple, all_stops))

    all_stops_name = []
    for feature in data['data']['features'][dir]['features']:
        if 'name' in feature:
            all_stops_name.append(feature['name'])
    return list(zip(all_stops_name, all_stops))


def generate_info(path_number, dirrection, time):
    # Загружаем данные (замените на ваш источник данных)
    with open(f'C:/Users/Admin/PycharmProjects/КП/JsonFilesImport/data{path_number}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    if dirrection:
        dir = 1
    else:
        dir = 0

    # Извлекаем точки
    result_path = extract_points(data, dir)
    result_stop = extract_stops(data, dir)
    print(result_path)
    print()
    print(result_stop)

    db.set_route(extract_points(data, dir), path_number, 'Автобус', dirrection, time)
    db.set_bus_stops(extract_stops(data, dir), path_number, dir)
