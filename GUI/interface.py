import tkinter as tk
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageTk
import DATABASE.database_2 as db
import Classes.classes as cl


def load_image(image_path, size):
    try:
        image = Image.open(image_path)
        image = image.resize(size)
        photo = ImageTk.PhotoImage(image)
        return photo
    except FileNotFoundError:
        print(f"Изображение не найдено: {image_path}")
        return None


def direction_command(map_widget, route_var, direction_var, icon):
    map_widget.delete_all_marker()
    map_widget.delete_all_path()

    bus_route = db.get_bus_route_info(route_var.get(), direction_var.get())
    bus_stops = db.get_bus_stops_for_routes(route_var.get(), direction_var.get())

    create_path(bus_route, map_widget, route_var)
    create_bus_stops(bus_stops, map_widget, icon)


def radiobutton_command(map_widget, frame1_2, route_var, direction_var, icon):
    map_widget.delete_all_marker()
    map_widget.delete_all_path()

    for widget in frame1_2.winfo_children():
        widget.destroy()

    bus_route = db.get_bus_route_info(route_var.get(), False)
    bus_stops = db.get_bus_stops_for_routes(route_var.get(), False)

    create_path(bus_route, map_widget, route_var)
    create_bus_stops(bus_stops, map_widget, icon)
    direction_var.set(False)

    l1_2 = ttk.Label(frame1_2, text='Выбор направления', padding=8, font=('Bolt', 12))
    l1_2.grid(column=0, row=0, sticky='n')
    first_variation = db.get_end_bus_stop(route_var.get(), False, False)
    second_variation = db.get_end_bus_stop(route_var.get(), True, False)
    dict_direction = {
        False: f'{first_variation[0]}→{first_variation[1]}',
        True: f'{second_variation[0]}→{second_variation[1]}',
    }
    for direction in dict_direction:
        ttk.Radiobutton(frame1_2, text=dict_direction[direction], variable=direction_var,
                        value=direction, command=lambda: direction_command(map_widget, route_var,
                                                                           direction_var, icon)).grid(sticky='n', padx=8,
                                                                                                pady=4)
    frame1_2.columnconfigure(index=1, weight=1)
    frame1_2.rowconfigure(index=1, weight=0)
    frame1_2.columnconfigure(index=2, weight=1)
    frame1_2.rowconfigure(index=2, weight=0)


def create_path(bus_route, map_widget, route_var):
    dict_colors = {
        7: 'blue',
        2: 'green',
        77: 'red'
    }
    map_widget.set_path(bus_route.path, color=dict_colors[route_var.get()])


def create_bus_stops(bus_stops, map_widget, icon):
    for stop in bus_stops:
        map_widget.set_marker(stop.coordinates[0], stop.coordinates[1], text=stop.name, icon=icon)


def startMain():
    root = tk.Tk()
    root.title("Автобусные маршруты")
    root.geometry("1400x700+30+30")

    seven_img_path = "C:/Users/Admin/PycharmProjects/КП/Resources/seven.png"
    two_img_path = "C:/Users/Admin/PycharmProjects/КП/Resources/two.png"
    seventy_seven_img_path = "C:/Users/Admin/PycharmProjects/КП/Resources/seventy_seven.png"
    bus_icon_img_path = "C:/Users/Admin/PycharmProjects/КП/Resources/bus_stop.png"

    new_size_for_icon = (32, 32)
    new_size_for_numbers = (35, 35)

    seven_img_tk = load_image(seven_img_path, new_size_for_numbers)
    two_img_tk = load_image(two_img_path, new_size_for_numbers)
    seventy_seven_img_tk = load_image(seventy_seven_img_path, new_size_for_numbers)
    icon = load_image(bus_icon_img_path, new_size_for_icon)

    # create map widget
    map_widget = tkintermapview.TkinterMapView(root, width=800, height=700, corner_radius=10)
    map_widget.grid(column=0, row=0)
    map_widget.set_position(45.040025, 38.976108)
    map_widget.set_zoom(13)

    # map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    route_var = tk.IntVar()
    direction_var = tk.BooleanVar()

    frame1 = ttk.Frame()
    frame1.grid(column=1, row=0, sticky='ns')
    frame1.columnconfigure(index=0, weight=1)
    frame1.rowconfigure(index=0, weight=1)
    frame1.columnconfigure(index=1, weight=1)
    frame1.rowconfigure(index=1, weight=1)

    frame1_1 = ttk.Frame(frame1)
    frame1_1.grid(column=0, row=0, sticky='nsew')
    frame1_1.columnconfigure(index=0, weight=1)
    frame1_1.rowconfigure(index=0, weight=1)

    l1_1 = ttk.Label(frame1_1, text='Расписание и остановки маршрута №', padding=8, font=('Bolt', 12))
    l1_1.grid(column=0, row=0, sticky='n')

    frame1_2 = ttk.Frame(frame1)
    frame1_2.grid(column=0, row=1, sticky='nsew')
    frame1_2.columnconfigure(index=0, weight=1)
    frame1_2.rowconfigure(index=0, weight=0)

    frame2 = ttk.Frame()
    frame2.grid(column=2, row=0, sticky='n')
    l2 = ttk.Label(frame2, text='Выберете маршрут', padding=8, font=('Bolt', 12))
    l2.grid(column=0, row=0, sticky='n')

    dict_routes = {
        2: {'name': 'Маршрут №2', 'image': two_img_tk},
        7: {'name': 'Маршрут №7', 'image': seven_img_tk},
        77: {'name': 'Маршрут №77', 'image': seventy_seven_img_tk}
    }

    for route in dict_routes:
        ttk.Radiobutton(frame2, text=dict_routes[route]['name'], variable=route_var, value=route,
                        command=lambda: radiobutton_command(map_widget, frame1_2, route_var, direction_var, icon),
                        compound='left', image=dict_routes[route]['image']).grid(column=0, row=route)
    root.mainloop()
