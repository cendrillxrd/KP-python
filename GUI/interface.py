import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

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


def checkbutton_state(route_number):
    if db.is_active(route_number):
        return 1
    else:
        return 0


def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def startMain(is_admin):
    root = tk.Tk()
    root.title("Автобусные маршруты")
    root.geometry("1400x725+30+30")
    root.resizable(False, False)

    route_var = tk.IntVar()
    direction_var = tk.BooleanVar()
    map_var = tk.IntVar(value=1)

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
        77: {'name': 'Маршрут №77', 'image': images_dict['seventy_seven_img']},
    }

    dict_colors = {
        7: 'blue',
        2: 'green',
        77: 'red'
    }

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.X)
    notebook.pack_propagate(False)

    frame_admin = ttk.Frame(notebook)
    frame_user = ttk.Frame(notebook)

    # create map widget
    map_widget = tkintermapview.TkinterMapView(frame_user, width=800, height=700, corner_radius=10)
    map_widget.grid(column=0, row=0)
    map_widget.set_position(45.040025, 38.976108)
    map_widget.set_zoom(13)

    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    frame1 = ttk.Frame(frame_user)
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

    frame2 = ttk.Frame(frame_user, padding=10)
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

    style = ttk.Style()
    style.configure("TRadiobutton", font=('Helvetica', 14))

    style1 = ttk.Style()
    style1.configure("Default.TRadiobutton", font=('Helvetica', 10))

    if is_admin:
        notebook.add(frame_admin, text="admin")
    notebook.add(frame_user, text="user")

    def map_clear():
        map_widget.delete_all_marker()
        map_widget.delete_all_path()

    def generate_route_text():
        if route_var.get():
            l1_1.config(text=f'Расписание и остановки маршрута № {route_var.get()}')
        else:
            l1_1.config(text=f'Расписание и остановки маршрута')

    def radiobutton_command():
        map_clear()
        generate_route_text()

        for widget in frame1_2.winfo_children():
            widget.destroy()

        bus_route = db.get_bus_route_info(route_var.get(), False)
        bus_stops = db.get_bus_stops_for_routes(route_var.get(), False)

        create_path(bus_route)
        create_bus_stops(bus_stops)
        direction_var.set(False)

        recreate_bus_stop_list(bus_stops)

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

        clear_frame(frame1_2)

        dict_direction = {
            False: f'{first_variation[0]}→{first_variation[1]}',
            True: f'{second_variation[0]}→{second_variation[1]}',
        }

        l1_4 = ttk.Label(frame1_2, text='Выбор направления', padding=8, font=('Bolt', 12))
        l1_4.grid(column=0, row=0, sticky='n')

        for direction in dict_direction:
            ttk.Radiobutton(frame1_2,
                            text=dict_direction[direction],
                            variable=direction_var,
                            value=direction,
                            command=direction_command,
                            style="Default.TRadiobutton"
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
            trans_list = list(map(str, db.info_about_bus_stop(marker.position)))
            trans_str = ', '.join(trans_list)

            popup = tk.Toplevel()  # Создаем новое окно
            popup.wm_title("Маршруты")
            popup.overrideredirect(True)

            # Определяем текст окна
            frame = tk.Frame(popup, relief=tk.RIDGE, borderwidth=4, bg="blue")
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

    def create_route_radiobutton():
        for route_number in dict_routes:
            if checkbutton_state(route_number):
                ttk.Radiobutton(frame2_1,
                                text=dict_routes[route_number]['name'],
                                variable=route_var,
                                value=route_number,
                                command=radiobutton_command,
                                compound='left',
                                image=dict_routes[route_number]['image'],
                                style="TRadiobutton"
                                ).grid(column=0, row=route_number, sticky='w')

    create_route_radiobutton()
    root.option_add("*tearOff", tk.FALSE)

    def refresh_map():
        map_clear()
        bus_stops_list.delete(0, tk.END)
        clear_frame(frame1_2)
        clear_frame(frame2_1)
        create_route_radiobutton()
        route_var.set(0)
        generate_route_text()
        l1_3['text'] = ''

    def edit_menu_radiobutton():
        match map_var.get():
            case 1:
                map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            case 2:
                map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        pass

    file_menu = tk.Menu()
    file_menu.add_command(label="Save")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: root.destroy())

    view_menu = tk.Menu()
    view_menu.add_radiobutton(label='Карта 1', command=edit_menu_radiobutton, value=1, variable=map_var)
    view_menu.add_radiobutton(label='Карта 2', command=edit_menu_radiobutton, value=2, variable=map_var)
    view_menu.add_separator()
    view_menu.add_command(label='refresh', command=refresh_map)

    main_menu = tk.Menu()
    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Edit")
    main_menu.add_cascade(label="View", menu=view_menu)

    root.config(menu=main_menu)

    frame_admin_1 = tk.Frame(frame_admin, borderwidth=1, relief=tk.SOLID)
    frame_admin_1.grid_propagate(False)
    frame_admin_1.grid(column=0, row=0, sticky='nsew', rowspan=3)

    frame_admin_2 = tk.Frame(frame_admin, borderwidth=1, relief=tk.SOLID)
    frame_admin_2.grid_propagate(False)
    frame_admin_2.grid(column=1, row=0, sticky='nsew', rowspan=3)

    frame_admin_3 = tk.Frame(frame_admin, borderwidth=1, relief=tk.SOLID)
    frame_admin_3.grid_propagate(False)
    frame_admin_3.grid(column=2, row=0, sticky='nsew', rowspan=3)

    for i in range(0, 3):
        frame_admin.columnconfigure(index=i, weight=1)
        frame_admin.rowconfigure(index=i, weight=1)

    def activateRoute(route_number):
        if checkbox_values[route_number].get() == 1:
            showinfo(title="Info", message="Включено")
        else:
            showinfo(title="Info", message="Отключено")
        db.change_route_state(route_number)
        refresh_map()

    style_check = ttk.Style()
    style_check.configure('TCheckbutton', font=('Helvetica', 20))
    checkbox_values = {}

    for route in dict_routes:
        v = tk.IntVar()
        v.set(checkbutton_state(route))
        checkbox_values[route] = v
        ttk.Checkbutton(frame_admin_1,
                        text=dict_routes[route]['name'],
                        compound='left',
                        image=dict_routes[route]['image'],
                        style='TCheckbutton',
                        variable=v,
                        command=lambda r=route: activateRoute(r),
                        ).grid(padx=(100, 0), ipady=20, sticky='w')

    root.mainloop()
