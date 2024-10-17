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


def startMain():
    root = tk.Tk()
    root.title("Автобусные маршруты")
    root.geometry("1400x700+30+30")
    root.resizable(False, False)

    # x = None
    # y = None
    # def on_click(event):
    #     global x
    #     global y
    #     x, y = event.x, event.y
    #     print(f"Координаты курсора: x={x}, y={y}")
    #
    # root.bind('<Button-1>', on_click)

    new_size_for_icon = (32, 32)
    new_size_for_numbers = (35, 35)

    images_dict = {
        'seven_img': load_image("C:/Users/Admin/PycharmProjects/КП/Resources/seven.png",
                                new_size_for_numbers),
        'two_img': load_image("C:/Users/Admin/PycharmProjects/КП/Resources/two.png",
                              new_size_for_numbers),
        'seventy_seven_img': load_image("C:/Users/Admin/PycharmProjects/КП/Resources/seventy_seven.png",
                                        new_size_for_numbers),
        'bus_icon_img': load_image("C:/Users/Admin/PycharmProjects/КП/Resources/bus_stop.png",
                                   new_size_for_icon),
        'bus_autoriz_img': load_image("C:/Users/Admin/PycharmProjects/КП/Resources/bus_autoriz.png",
                                      (100, 100))
    }

    dict_routes = {
        2: {'name': 'Маршрут №2', 'image': images_dict['two_img']},
        7: {'name': 'Маршрут №7', 'image': images_dict['seven_img']},
        77: {'name': 'Маршрут №77', 'image': images_dict['seventy_seven_img']}
    }

    dict_colors = {
        7: 'blue',
        2: 'green',
        77: 'red'
    }

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
    frame1.rowconfigure(index=0, weight=1)
    frame1.rowconfigure(index=1, weight=1)

    frame1_1 = ttk.Frame(frame1)
    frame1_1.grid(column=0, row=0, sticky='nsew')

    l1_1 = ttk.Label(frame1_1, text='Расписание и остановки маршрута №', padding=8, font=('Bolt', 12))
    l1_1.grid(padx=10, pady=10)

    frame1_2 = ttk.Frame(frame1)
    frame1_2.grid(column=0, row=1, sticky='nsew')
    frame1_2.columnconfigure(index=0, weight=1)
    frame1_2.rowconfigure(index=0, weight=0)

    frame2 = ttk.Frame(padding=10)
    frame2.grid(column=2, row=0, sticky='nsew')
    l2 = ttk.Label(frame2, text='Выберете маршрут', padding=8, font=('Bolt', 12))
    l2.grid(column=0, row=0, sticky='n')

    frame2_1 = ttk.Frame(frame2, padding=8)
    frame2_1.grid()

    bus_stops_list = tk.Listbox(frame1_1, height=20)
    bus_stops_list.grid(padx=10, pady=10, sticky='nsew')

    scrollbar = ttk.Scrollbar(bus_stops_list, orient="vertical", command=bus_stops_list.yview)
    scrollbar.place(relx=1, rely=0, relheight=1, anchor='ne')

    bus_stops_list.configure(yscrollcommand=scrollbar.set)

    l1_2 = ttk.Label(frame1_1, image=images_dict['bus_autoriz_img'])
    l1_2.grid(padx=10, pady=10)
    l1_3 = ttk.Label(frame1_1, text='', font=('Bolt', 12))
    l1_3.grid(padx=10)

    # frame1_2.columnconfigure(index=1, weight=1)
    # frame1_2.rowconfigure(index=1, weight=0)
    # frame1_2.columnconfigure(index=2, weight=1)
    # frame1_2.rowconfigure(index=2, weight=0)
    def map_clear():
        map_widget.delete_all_marker()
        map_widget.delete_all_path()

    def radiobutton_command():
        map_clear()

        for widget in frame1_2.winfo_children():
            widget.destroy()

        bus_route = db.get_bus_route_info(route_var.get(), False)
        bus_stops = db.get_bus_stops_for_routes(route_var.get(), False)

        create_path(bus_route)
        create_bus_stops(bus_stops)
        direction_var.set(False)

        recreate_bus_stop_list(bus_stops)

        l1_4 = ttk.Label(frame1_2, text='Выбор направления', padding=8, font=('Bolt', 12))
        l1_4.grid(column=0, row=0, sticky='n')

        recreate_direction_view()

        schedule()

    def schedule():
        bus_route = db.get_bus_route_info(route_var.get(), False)
        tb = bus_route.get_schedule()
        l1_3['text'] = tb

    def recreate_bus_stop_list(bus_stops):
        def selected(event):
            selected_index = bus_stops_list.curselection()[0]
            bus_stop_name = bus_stops_list.get(selected_index)
            coordinates = (0, 0)
            for bus_stop in bus_stops:
                if bus_stop.name == bus_stop_name:
                    coordinates = bus_stop.coordinates
                    break
            map_widget.set_position(coordinates[0], coordinates[1])
            map_widget.set_zoom(15)

        bus_stops_list.delete(0, tk.END)
        for stop in bus_stops:
            bus_stops_list.insert(tk.END, stop.name)
        bus_stops_list.bind("<<ListboxSelect>>", selected)

    def recreate_direction_view():
        first_variation = db.get_end_bus_stop(route_var.get(), False, False)
        second_variation = db.get_end_bus_stop(route_var.get(), True, False)

        dict_direction = {
            False: f'{first_variation[0]}→{first_variation[1]}',
            True: f'{second_variation[0]}→{second_variation[1]}',
        }
        for direction in dict_direction:
            ttk.Radiobutton(frame1_2,
                            text=dict_direction[direction],
                            variable=direction_var,
                            value=direction,
                            command=direction_command,
                            ).grid(padx=8, pady=4, )

    def direction_command():
        map_clear()

        bus_route = db.get_bus_route_info(route_var.get(), direction_var.get())
        bus_stops = db.get_bus_stops_for_routes(route_var.get(), direction_var.get())

        create_path(bus_route)
        create_bus_stops(bus_stops)

        recreate_bus_stop_list(bus_stops)

    def create_path(bus_route):
        map_widget.set_path(bus_route.path, color=dict_colors[route_var.get()])

    def create_bus_stops(bus_stops):
        def click_on_marker(marker):

            trans_list = list(map(str,db.info_about_bus_stop(marker.position)))
            trans_str = ', '.join(trans_list)

            popup = tk.Toplevel()  # Создаем новое окно
            popup.wm_title("Маршруты")
            popup.overrideredirect(True)

            # Определяем текст окна
            frame = tk.Frame(popup, relief=tk.RIDGE, borderwidth=4,  bg="blue")
            frame.pack()  # Отступы для создания видимой границы

            # Размещаем метку внутри рамки
            label = ttk.Label(frame, text=f"Маршруты: {trans_str}", font='Bolt', background='#AFE7E1')
            label.pack()

            # Размещаем окно выше курсора мыши
            x = popup.winfo_pointerx()
            y = popup.winfo_pointery() - 30  # Поднимаем окно немного вверх
            popup.geometry(f"+{x}+{y}")  # Устанавливаем позицию окна
            popup.after(3000, popup.destroy)
            # Закрываем окно при клике
            popup.bind("<Button-1>", lambda e: popup.destroy())

        for stop in bus_stops:
            map_widget.set_marker(stop.coordinates[0],
                                  stop.coordinates[1],
                                  text=stop.name,
                                  icon=images_dict['bus_icon_img'],
                                  command=click_on_marker)

    for route in dict_routes:
        ttk.Radiobutton(frame2_1,
                        text=dict_routes[route]['name'],
                        variable=route_var,
                        value=route,
                        command=radiobutton_command,
                        compound='left',
                        image=dict_routes[route]['image']
                        ).grid(column=0, row=route, sticky='w')
    root.mainloop()
