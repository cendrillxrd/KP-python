import tkinter as tk
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageTk
import DATABASE.database as db
import numpy as np
from scipy.interpolate import splprep, splev, interp1d
import Classes.classes as cl


root = tk.Tk()
root.title("Автобусные маршруты")
root.geometry("1400x700+30+30")
route_var = tk.IntVar()

# create map widget
map_widget = tkintermapview.TkinterMapView(root, width=800, height=700, corner_radius=10)
map_widget.grid(column=0, row=0)
map_widget.set_position(45.040025, 38.976108)
map_widget.set_zoom(13)

map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

frame1 = ttk.Frame(borderwidth=0, padding=8)
frame1.grid(column=1, row=0, sticky='n')
l1 = ttk.Label(frame1, text='Расписание и остановки маршрута N', padding=8, font=('Bolt', 12))
l1.grid(column=0, row=0, sticky='n')


def radiobutton_command():
    map_widget.delete_all_marker()
    map_widget.delete_all_path()
    path = db.get_paths(route_var.get())

    # Преобразуем координаты в numpy массивы
    # lats, longs = zip(*coords)
    # lats = np.array(lats, dtype=np.float64)
    # longs = np.array(longs, dtype=np.float64)
    #
    # # Интерполяция с использованием кубических сплайнов
    # tck, u = splprep([lats, longs], s=0)
    # unew = np.linspace(0, 1.0, 1000)
    # out = splev(unew, tck)
    #
    # path = list(zip(out[0], out[1]))
    # lats, longs = zip(*coords)
    # lats = np.array(lats, dtype=np.float64)
    # longs = np.array(longs, dtype=np.float64)
    #
    # # Линейная интерполяция
    # f_lat = interp1d(np.arange(len(lats)), lats)
    # f_long = interp1d(np.arange(len(longs)), longs)
    #
    # # Новые значения для интерполяции
    # xnew = np.linspace(0, len(lats) - 1, 1000)  # 1000 новых точек
    #
    # # Вычисляем интерполированные значения
    # lats_new = f_lat(xnew)
    # longs_new = f_long(xnew)
    #
    # # Объединяем интерполированные координаты в список
    # path = list(zip(lats_new, longs_new))

    name = db.get_name(route_var.get())
    stops = db.get_bus_stops(route_var.get())

    schedule = cl.Schedule(0, 'Каждые 10 минут', stops)
    bus_route = cl.BusRoute(0, name, schedule, path)

    bus_system = cl.BusSystem()
    bus_system.add_route(bus_route)

    create_path(bus_system.routes[0])


seven_img = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/КП/Resources/seven.png")
two_img = tk.PhotoImage(file="C:/Users/Admin/PycharmProjects/КП/Resources/two.png")
seven_img = seven_img.subsample(15, 15)
two_img = two_img.subsample(15, 15)

dict_routes = {
    2: {'name': 'Маршрут №2', 'image': two_img},
    7: {'name': 'Маршрут №7', 'image': seven_img},
    # 77: {'name': 'Маршрут №77', 'image': seven_img}
}

frame2 = ttk.Frame(borderwidth=0, padding=8)
frame2.grid(column=2, row=0, sticky='n')
l2 = ttk.Label(frame2, text='Выберете маршрут', padding=8, font=('Bolt', 12))
l2.grid(column=0, row=0, sticky='n')
for route in dict_routes:
    ttk.Radiobutton(frame2, text=dict_routes[route]['name'], variable=route_var, value=route,
                    command=radiobutton_command,image=dict_routes[route]['image'],
                    compound='left').grid(column=0, row=route)

image_path = 'C:/Users/Admin/PycharmProjects/КП/Resources/bus_stop.png'
image = Image.open(image_path)
new_size = (32, 32)
image = image.resize(new_size)
icon = ImageTk.PhotoImage(image)


def create_path(bus_route):
    map_widget.set_path(bus_route.path)
    for stop in bus_route.schedule.bus_stops:
        map_widget.set_marker(stop.coordinates[0], stop.coordinates[1], text=stop.name,
                              icon=icon)


def Start():
    root.mainloop()
