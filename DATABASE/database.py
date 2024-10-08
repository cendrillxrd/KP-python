import sqlite3 as sq
import re
import Classes.classes as cl
from pathlib import Path


with sq.connect('C:/Users/Admin/PycharmProjects/КП/DATABASE/routes.db') as con:
    cur = con.cursor()
    # list = [("Гипермаркет О'КЕЙ", (45.01252096, 39.12098739)), ('Харьковская улица', (45.010322227, 39.124888897)), ('Улица Думенко', (45.006874771, 39.104380274)), ('Проспект Чекистов', (45.010450313, 39.101214032)), ('Торговый центр', (45.013605185, 39.098435342)), ('Почта', (45.015293855, 39.08981503)), ('Улица 70 лет Октября', (45.013233915, 39.079091609)), ('Рождественский парк', (45.012609681, 39.074648817)), ('Супермаркет Маяк', (45.014174037, 39.063040548)), ('Школа № 90', (45.013655881, 39.057656867)), ('Улица Думенко', (45.013349389, 39.051867762)), ('Детская школа искусств', (45.016034978, 39.047714113)), ('Харьковская улица', (45.018555099, 39.04896759)), ('Тульская улица', (45.02357749, 39.042508804)), ('Кубанский государственный аграрный университет', (45.024373626, 39.039702389)), ('Улица Калинина', (45.025747897, 39.035087384)), ('ЦКР', (45.026643351, 39.031396008)), ('ТРЦ Галерея Краснодар', (45.031375623, 39.028255807)), ('Улица Коммунаров', (45.034506224, 39.01617089)), ('Улица Янковского', (45.034447257, 39.013800238)), ('Базовская улица', (45.036261, 39.001732233)), ('Садовая улица', (45.036829252, 38.998212659)), ('Улица Корницкого', (45.037593, 38.993237233)), ('Улица Ломоносова', (45.038402, 38.988152233)), ('ВНИИМК', (45.039057, 38.983893233)), ('Улица Филатова', (45.039551279, 38.980648141)), ('Уральская улица', (45.0405497, 38.974580733)), ('Ялтинская улица', (45.038883882, 38.970685132)), ('Поликлиника', (45.0437118, 38.933862233)), ('Волжская улица', (45.043866802, 38.929951805)), ('Улица Стасова', (45.041342, 38.928661233)), ('Улица Селезнёва', (45.039992148, 38.922531099)), ('Старокубанская улица', (45.039108641, 38.917667739)), ('Парк Солнечный остров', (45.038143116, 38.910507364)), ('Парк Солнечный остров', (45.036030137, 38.906593245)), ('Краснодарская ТЭЦ', (45.033078568, 38.904019671)), ('Улица Автолюбителей', (45.029382012, 38.901896078)), ('Краевая улица', (45.02565, 38.904866233)), ('Улица Василия Мачуги', (45.026672, 38.906205233)), ('Улица Плиева', (45.028762555, 38.908355327)), ('Улица Крупской', (45.030562532, 38.912843891)), ('Бородинская улица', (45.032339608, 38.917287935)), ('Горячеключевская улица', (45.033708, 38.920638233)), ('ТРК OZ Mall', (45.036196, 38.926493233))]
    #
    # for stop in list:
    #     name = stop[0]
    #     coords = str(stop[1])
    #     cur.execute("INSERT INTO bus_stops2 (stop_name, coordinates, routes_list) VALUES (?, ?, ?)",
    #                 (name, coords, 77))

def get_paths(number):
    cur.execute(f"""SELECT path FROM routes WHERE id = {number}""")
    input_string = cur.__next__()[0]

    pattern = re.compile(r"\(([^)]+)\)")
    matches = pattern.findall(input_string)

    # Преобразование в список кортежей
    return [tuple(map(float, match.split(','))) for match in matches]


def get_name(number):
    cur.execute(f"""SELECT id, name FROM routes WHERE id = {number}""")
    number, name = cur.__next__()
    return f'{name} №{number}'


def get_bus_stops(number):

    # bus_info = cur.execute(f"""SELECT * FROM bus_stops2 WHERE routes_list like ('%{number}%')""").fetchall()
    # stops = []
    # for i in bus_info:
    #     coords_tuple = tuple(map(float, i[2].strip('()').split(', ')))
    #     stops.append(cl.BusStop(i[0], i[1], coords_tuple))
    # return stops
    bus_info_name_and_coords = cur.execute(f"""
                                        SELECT * FROM bus_stops WHERE coordinates """).fetchall()
    stops = []
    for i in bus_info:
        coords_tuple = tuple(map(float, i[2].strip('()').split(', ')))
        stops.append(cl.BusStop(i[0], i[1], coords_tuple))
    return stops



def set_bus_stops(stop_list, number):
    for stop in stop_list:
        name = stop[0]
        coords = str(stop[1])
        cur.execute("INSERT INTO bus_stops (stop_name, coordinates) VALUES (?, ?)",
                    (name, coords))
        con.commit()
        cur.execute(f"""SELECT stop_id FROM bus_stops WHERE name = {name} AND coordinates = {coords} """)
        cur.execute("INSERT INTO bus_stops_transport (coordinates, path_number) VALUES (?, ?)",
                    (coords, number))

