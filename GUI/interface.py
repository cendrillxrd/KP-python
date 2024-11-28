import tkinter as tk
from tkinter import ttk, messagebox

import tkintermapview
from PIL import Image, ImageTk
import DATABASE.database_2 as db


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


def startMain(user):
    root = tk.Tk()
    root.title("Автобусные маршруты")
    root.geometry("1400x725+30+30")
    root.resizable(False, False)

    route_var = tk.IntVar()
    direction_var = tk.BooleanVar(value=False)
    map_var = tk.IntVar(value=1)
    theme_var = tk.StringVar(value='white')
    route_var_driver = tk.IntVar()

    new_size_for_icon = (32, 32)
    new_size_for_numbers = (35, 35)

    images_dict = {
        'seven_img': load_image("Resources/seven.png",
                                new_size_for_numbers),
        'two_img': load_image("Resources/two.png",
                              new_size_for_numbers),
        'seventy_seven_img': load_image("Resources/seventy_seven.png",
                                        new_size_for_numbers),
        'twenty_img': load_image("Resources/twenty.png",
                                 new_size_for_numbers),
        'twelve_img': load_image("Resources/twelve.png",
                                 new_size_for_numbers),
        'fourteen_img': load_image("Resources/fourteen.png",
                                   new_size_for_numbers),
        'bus_icon_img': load_image("Resources/bus_stop.png",
                                   new_size_for_icon),
        'bus_autoriz_img': load_image("Resources/bus_autoriz.png",
                                      (100, 100))
    }

    dict_routes = {
        2: {'name': 'Маршрут №2', 'image': images_dict['two_img']},
        7: {'name': 'Маршрут №7', 'image': images_dict['seven_img']},
        77: {'name': 'Маршрут №77', 'image': images_dict['seventy_seven_img']},
        20: {'name': 'Маршрут №20', 'image': images_dict['twenty_img']},
        12: {'name': 'Маршрут №12', 'image': images_dict['twelve_img']},
        14: {'name': 'Маршрут №14', 'image': images_dict['fourteen_img']},
    }

    dict_colors = {
        7: 'blue',
        2: 'green',
        77: 'red',
        20: 'orange',
        12: 'purple',
        14: '#f51de6'
    }

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.X)
    notebook.pack_propagate(False)

    style0 = ttk.Style()
    style0.configure("TFrame", bg='white')

    frame_admin = tk.Frame(notebook)
    frame_user = tk.Frame(notebook)
    frame_driver = tk.Frame(notebook)

    # create map widget
    map_widget = tkintermapview.TkinterMapView(frame_user, width=800, height=700, corner_radius=10)
    map_widget.grid(column=0, row=0)
    map_widget.set_position(45.040025, 38.976108)
    map_widget.set_zoom(13)

    map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    frame1 = tk.Frame(frame_user)
    frame1.grid(column=1, row=0, sticky='ns')
    frame1.rowconfigure(index=0, weight=1)
    frame1.rowconfigure(index=1, weight=1)

    frame1_1 = tk.Frame(frame1)
    frame1_1.grid(column=0, row=0, sticky='nsew')

    l1_1 = ttk.Label(frame1_1, text='Расписание и остановки маршрута №', padding=8, font=('Bolt', 12))
    l1_1.grid(padx=10, pady=10)

    frame1_2 = tk.Frame(frame1)
    frame1_2.grid(column=0, row=1, sticky='nsew')
    frame1_2.columnconfigure(index=0, weight=1)
    frame1_2.rowconfigure(index=0, weight=0)

    frame2 = tk.Frame(frame_user, padx=10, pady=10)
    frame2.grid(column=2, row=0, sticky='nsew')
    l2 = ttk.Label(frame2, text='Выберете маршрут', padding=8, font=('Bolt', 12))
    l2.grid(column=0, row=0, sticky='n')

    frame2_1 = tk.Frame(frame2, padx=10, pady=10)
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

    if user.is_admin:
        notebook.add(frame_admin, text="admin")
        notebook.add(frame_user, text="user")
        notebook.add(frame_driver, text="driver")
    elif user.is_driver:
        notebook.add(frame_driver, text="driver")
    else:
        notebook.add(frame_user, text="user")

    def map_clear(is_user):
        if is_user:
            map_widget.delete_all_marker()
            map_widget.delete_all_path()
        else:
            map_widget_driver.delete_all_marker()
            map_widget_driver.delete_all_path()

    def generate_route_text():
        if route_var.get():
            l1_1.config(text=f'Расписание и остановки маршрута № {route_var.get()}')
        else:
            l1_1.config(text=f'Расписание и остановки маршрута')

    def radiobutton_command():
        map_clear(True)
        generate_route_text()

        for widget in frame1_2.winfo_children():
            widget.destroy()

        bus_route = db.get_bus_route_info(route_var.get(), False)
        bus_stops = db.get_bus_stops_for_routes(route_var.get(), False)

        create_path(True, bus_route)
        create_bus_stops(True, bus_stops)
        direction_var.set(False)

        recreate_bus_stop_list(bus_stops)

        recreate_direction_view(True)

        schedule()

    def schedule():
        bus_route = db.get_bus_route_info(route_var.get(), False)
        tb = bus_route.get_schedule()
        l1_3['text'] = tb

    def recreate_bus_stop_list(bus_stops):
        def selected(event):
            try:
                selected_index = bus_stops_list.curselection()[0]
                bus_stop_name = bus_stops_list.get(selected_index)
                coordinates = (0, 0)
                for bus_stop in bus_stops:
                    if bus_stop.name == bus_stop_name:
                        coordinates = bus_stop.coordinates
                        break
                map_widget.set_position(coordinates[0], coordinates[1])
                map_widget.set_zoom(15)
            except IndexError:
                print('temp')

        bus_stops_list.delete(0, tk.END)
        for stop in bus_stops:
            bus_stops_list.insert(tk.END, stop.name)
        bus_stops_list.bind("<<ListboxSelect>>", selected)

    def recreate_direction_view(is_user):
        if is_user:
            first_variation = db.get_end_bus_stop(route_var.get(), False, False)
            second_variation = db.get_end_bus_stop(route_var.get(), True, False)

            clear_frame(frame1_2)

            l1_4 = ttk.Label(frame1_2, text='Выбор направления', padding=8, font=('Bolt', 12))
            l1_4.grid(column=0, row=0, sticky='n')

            dict_direction = {
                False: f'{first_variation[0]}→{first_variation[1]}',
                True: f'{second_variation[0]}→{second_variation[1]}',
            }

            for direction in dict_direction:
                ttk.Radiobutton(frame1_2,
                                text=dict_direction[direction],
                                variable=direction_var,
                                value=direction,
                                command=lambda: direction_command(True),
                                style="Default.TRadiobutton",
                                takefocus=False
                                ).grid(padx=8, pady=4, )
        else:
            if user.is_admin:
                x = db.get_driver_path(combobox_drivers_dr.get())
            else:
                x = db.get_driver_path(user.login)
            first_variation = db.get_end_bus_stop(x, False, False)
            second_variation = db.get_end_bus_stop(x, True, False)

            clear_frame(frame_driver_1_1)

            l = ttk.Label(frame_driver_1_1, text='Выбор направления', padding=8, font=('Bolt', 12))
            l.grid(column=0, row=0, sticky='n')

            dict_direction = {
                False: f'{first_variation[0]}→{first_variation[1]}',
                True: f'{second_variation[0]}→{second_variation[1]}',
            }
            for direction in dict_direction:
                ttk.Radiobutton(frame_driver_1_1,
                                text=dict_direction[direction],
                                variable=direction_var,
                                value=direction,
                                command=lambda: direction_command(False),
                                style="Default.TRadiobutton",
                                takefocus=False
                                ).grid(padx=8, pady=4, )

    def direction_command(is_user):
        if is_user:
            map_clear(True)

            bus_route = db.get_bus_route_info(route_var.get(), direction_var.get())
            bus_stops = db.get_bus_stops_for_routes(route_var.get(), direction_var.get())

            create_path(True, bus_route)
            create_bus_stops(True, bus_stops)

            recreate_bus_stop_list(bus_stops)
        else:
            map_clear(False)
            if user.is_admin:
                r = db.get_driver_path(combobox_drivers_dr.get())
            else:
                r = db.get_driver_path(user.login)

            bus_route = db.get_bus_route_info(r, direction_var.get())
            bus_stops = db.get_bus_stops_for_routes(r, direction_var.get())

            create_path(False, bus_route)
            create_bus_stops(False, bus_stops)

            recreate_bus_stop_list_driver(bus_stops)

    def create_path(is_user, bus_route):
        if is_user:
            map_widget.set_path(bus_route.path, color=dict_colors[route_var.get()])
        else:
            map_widget_driver.set_path(bus_route.path, color=dict_colors[route_var.get()])

    def create_bus_stops(is_user, bus_stops):
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

        if is_user:
            for stop in bus_stops:
                map_widget.set_marker(stop.coordinates[0],
                                      stop.coordinates[1],
                                      text=stop.name,
                                      icon=images_dict['bus_icon_img'],
                                      command=click_on_marker)
        else:
            for stop in bus_stops:
                map_widget_driver.set_marker(stop.coordinates[0],
                                             stop.coordinates[1],
                                             text=stop.name,
                                             icon=images_dict['bus_icon_img'])

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
                                style="TRadiobutton",
                                takefocus=False
                                ).grid(column=0, row=route_number, sticky='w')

    create_route_radiobutton()
    root.option_add("*tearOff", tk.FALSE)

    def refresh_map(is_user):
        if is_user:
            map_clear(is_user)
            bus_stops_list.delete(0, tk.END)
            clear_frame(frame1_2)
            clear_frame(frame2_1)
            create_route_radiobutton()
            route_var.set(0)
            generate_route_text()
            l1_3['text'] = ''
        else:
            frame_driver_1_1.focus()
            map_clear(is_user)
            clear_frame(frame_driver_1_1)
            route_var_driver.set(0)

    def edit_menu_radiobutton():
        match map_var.get():
            case 1:
                map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
                map_widget_driver.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            case 2:
                map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                           max_zoom=22)
                map_widget_driver.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga",
                                                  max_zoom=22)

        pass

    def change_theme(widget=notebook):
        try:
            widget.config(bg=theme_var.get())
        except tk.TclError:
            pass  # Игнорируем виджеты, у которых нет параметра bg

            # Рекурсивно обходим всех дочерних виджетов
        for child in widget.winfo_children():
            change_theme(child)

    file_menu = tk.Menu()
    file_menu.add_command(label="Save")
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: root.destroy())

    theme_menu = tk.Menu()
    theme_menu.add_radiobutton(label='white', command=change_theme, value='#F0F0F0', variable=theme_var)
    theme_menu.add_radiobutton(label='black', command=change_theme, value='#3C3B3C', variable=theme_var)

    view_menu = tk.Menu()
    view_menu.add_radiobutton(label='Карта 1', command=edit_menu_radiobutton, value=1, variable=map_var)
    view_menu.add_radiobutton(label='Карта 2', command=edit_menu_radiobutton, value=2, variable=map_var)
    view_menu.add_cascade(label='theme', menu=theme_menu)
    view_menu.add_separator()
    view_menu.add_command(label='refresh', command=lambda: refresh_map(True))

    main_menu = tk.Menu()
    main_menu.add_cascade(label="File", menu=file_menu)
    # main_menu.add_cascade(label="Edit")
    main_menu.add_cascade(label="View", menu=view_menu)

    root.config(menu=main_menu)

    # .......................................................................................admin

    frame_admin_1 = tk.Frame(frame_admin, borderwidth=1, relief=tk.SOLID)
    frame_admin_1.grid_propagate(False)
    frame_admin_1.grid(column=0, row=0, sticky='nsew', rowspan=3)

    frame_admin_2 = tk.Frame(frame_admin, borderwidth=1, relief=tk.SOLID)
    frame_admin_2.grid_propagate(False)
    frame_admin_2.grid(column=1, row=0, sticky='nsew', rowspan=3)

    frame_admin_3 = tk.Frame(frame_admin, borderwidth=1, relief=tk.SOLID)
    frame_admin_3.grid_propagate(False)
    frame_admin_3.grid(column=2, row=0, sticky='nsew', rowspan=3)

    # наполнение frame_admin_1
    for i in range(0, 3):
        frame_admin.columnconfigure(index=i, weight=1)
        frame_admin.rowconfigure(index=i, weight=1)

    ttk.Label(frame_admin_1, text='Активация маршрута', font=('Helvetica', 20)
              ).grid(padx=(100, 0), ipady=20, sticky='w')

    def activateRoute(route_number):
        if checkbox_values[route_number].get() == 1:
            messagebox.showinfo(title="Info", message="Включено")
        else:
            messagebox.showinfo(title="Info", message="Отключено")
        db.change_route_state(route_number)
        refresh_map(True)

    style_check = ttk.Style()
    style_check.configure('TCheckbutton', font=('Helvetica', 20))
    checkbox_values = {}

    for route in dict_routes:
        v = tk.IntVar(value=checkbutton_state(route))

        checkbox_values[route] = v
        ttk.Checkbutton(frame_admin_1,
                        text=dict_routes[route]['name'],
                        compound='left',
                        image=dict_routes[route]['image'],
                        style='TCheckbutton',
                        variable=v,
                        command=lambda r=route: activateRoute(r),
                        takefocus=False
                        ).grid(padx=(100, 0), ipady=20, sticky='w')

    # наполнение frame_admin_2
    ttk.Label(frame_admin_2, text='Настройка расписания', font=('Helvetica', 20)
              ).grid(padx=(90, 0), ipady=20, sticky='w')

    def on_select(event):
        frame_admin_2.focus()

    routes = [route_number for route_number in dict_routes]
    combobox_paths1 = ttk.Combobox(frame_admin_2, values=routes, font=('Helvetica', 18), state="readonly")
    combobox_paths1.grid(padx=(94, 0), sticky='w', pady=20)
    combobox_paths1.bind("<<ComboboxSelected>>", on_select)

    ttk.Label(frame_admin_2, text='Введите время ожидания', font=('Helvetica', 20)
              ).grid(padx=(70, 0), ipady=20, sticky='w')

    time_entry = ttk.Entry(frame_admin_2, font=('Helvetica', 19))
    time_entry.grid(padx=(93, 0), sticky='w')

    def set_timetable():
        try:
            db.change_time_value(int(combobox_paths1.get()), int(time_entry.get()))
            refresh_map(True)
            messagebox.showinfo(title="Info", message="Расписание изменено")
        except:
            messagebox.showerror("Ошибка", "Не корректные данные")

    style_button = ttk.Style()
    style_button.configure('TButton', font=('Bolt', 20))
    ttk.Button(frame_admin_2,
               text='Принять',
               style='TButton',
               command=set_timetable
               ).grid(sticky='w', padx=(145, 0), pady=30)

    # наполнение frame_admin_3
    ttk.Label(frame_admin_3, text='Работа с водителями', font=('Helvetica', 20)
              ).grid(padx=(100, 0), ipady=20, sticky='w')

    drivers = [driver for driver in db.get_drivers()]
    combobox_drivers = ttk.Combobox(frame_admin_3, values=drivers, font=('Helvetica', 18), state="readonly")
    combobox_drivers.grid(padx=(94, 0), sticky='w', pady=20)
    combobox_drivers.bind("<<ComboboxSelected>>", on_select)

    ttk.Label(frame_admin_3, text='Выберете маршрут', font=('Helvetica', 20)
              ).grid(padx=(110, 0), ipady=20, sticky='w')

    routes = [route_number for route_number in dict_routes]
    combobox_paths2 = ttk.Combobox(frame_admin_3, values=routes, font=('Helvetica', 18), state="readonly")
    combobox_paths2.grid(padx=(94, 0), sticky='w')

    combobox_paths2.bind("<<ComboboxSelected>>", on_select)

    def set_driver():
        try:
            path_number = int(combobox_paths2.get())
            res = db.change_driver_path(combobox_drivers.get(), path_number)
            if res:
                refresh_map(True)
                if path_number != 0:
                    messagebox.showinfo(title="Info", message="Водитель назначен")
                else:
                    messagebox.showinfo(title="Info", message="Водитель снят с линии")
            else:
                messagebox.showinfo(title="Info",
                                    message=f"Этот маршрут уже назначен для водителя"
                                            f" {db.get_driver_name_with_path(path_number)}")
        except:
            messagebox.showerror("Ошибка", "Не корректные данные")

    def get_info_driver():
        try:
            messagebox.showinfo(title="Info", message=db.get_info_driver(combobox_drivers.get()))
        except:
            messagebox.showerror("Ошибка", "Не корректные данные")

    ttk.Button(frame_admin_3,
               text='Назначить маршрут',
               style='TButton',
               command=set_driver
               ).grid(sticky='w', padx=(105, 0), pady=(30, 10))

    ttk.Button(frame_admin_3,
               text='Снять с линии',
               style='TButton',
               command=lambda: set_driver(0)
               ).grid(sticky='w', padx=(140, 0))

    ttk.Button(frame_admin_3,
               text='Инфо',
               style='TButton',
               command=get_info_driver
               ).grid(sticky='w', padx=(150, 0), pady=10)

    # .......................................................................................driver

    map_widget_driver = tkintermapview.TkinterMapView(frame_driver, width=800, height=700, corner_radius=10)
    map_widget_driver.grid(column=0, row=0)
    map_widget_driver.set_position(45.040025, 38.976108)
    map_widget_driver.set_zoom(13)

    map_widget_driver.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

    frame_driver_1 = tk.Frame(frame_driver, borderwidth=1, relief=tk.SOLID, width=600, height=700)
    frame_driver_1.grid_propagate(False)
    frame_driver_1.grid(column=2, row=0)

    ttk.Label(frame_driver_1, text="Информация о маршруте", font=('Helvetica', 20)
              ).grid(column=0, row=0, padx=(140, 0))

    ttk.Label(frame_driver_1, text='Назначенный маршрут', font=('Helvetica', 20)
              ).grid(column=0, row=1, padx=(140, 0))

    bus_stops_list_driver = tk.Listbox(frame_driver_1, height=20)
    bus_stops_list_driver.grid(padx=(135, 0), pady=10, sticky='nsew')

    scrollbar_driver = ttk.Scrollbar(bus_stops_list_driver, orient="vertical", command=bus_stops_list.yview)
    scrollbar_driver.place(relx=1, rely=0, relheight=1, anchor='ne')

    bus_stops_list_driver.configure(yscrollcommand=scrollbar.set)

    def recreate_bus_stop_list_driver(bus_stops):
        def selected_dr(event):
            try:
                selected_index = bus_stops_list_driver.curselection()[0]
                bus_stop_name = bus_stops_list_driver.get(selected_index)
                coordinates = (0, 0)
                for bus_stop in bus_stops:
                    if bus_stop.name == bus_stop_name:
                        coordinates = bus_stop.coordinates
                        break
                map_widget_driver.set_position(coordinates[0], coordinates[1])
                map_widget_driver.set_zoom(15)
            except IndexError:
                print('temp')

        bus_stops_list_driver.delete(0, tk.END)
        for stop in bus_stops:
            bus_stops_list_driver.insert(tk.END, stop.name)
        bus_stops_list_driver.bind("<<ListboxSelect>>", selected_dr)

    def on_select_driver(event):
        bus_stops_list_driver.select_clear(first=0, last=tk.END)
        refresh_map(False)



        login = combobox_drivers_dr.get()
        route_var_driver.set(value=db.get_driver_path(login))
        if route_var_driver.get():
            l_ad.configure(text=f'Маршрут {route_var_driver.get()} назначен')
            driver_bus_stops = db.get_bus_stops_for_routes(route_var_driver.get(), direction_var.get())
            r = db.get_driver_path(login)
            route_var.set(r)
            create_path(False, db.get_bus_route_info(r, direction_var.get()))
            create_bus_stops(False, db.get_bus_stops_for_routes(r, direction_var.get()))
            recreate_direction_view(False)
            recreate_bus_stop_list_driver(driver_bus_stops)
        else:
            # ttk.Label(frame_driver_1, text='Маршрут не назначен', font=('Helvetica', 20)
            #           ).grid(column=0, row=3, padx=(140, 0))
            l_ad.configure(text='Маршрут не назначен')

    if user.is_admin:
        l_ad = ttk.Label(frame_driver_1, text=f'{user.login}', font=('Helvetica', 20))
        l_ad.grid(column=0, row=3, padx=(140, 0))

        combobox_drivers_dr = ttk.Combobox(frame_driver_1, values=drivers, font=('Helvetica', 18), state="readonly")
        combobox_drivers_dr.grid(padx=(160, 0), sticky='w', pady=20)
        combobox_drivers_dr.bind("<<ComboboxSelected>>", on_select_driver)

        frame_driver_1_1 = tk.Frame(frame_driver_1)
        frame_driver_1_1.grid(column=0, row=1, sticky='nsew')
        frame_driver_1_1.columnconfigure(index=0, weight=1)
        frame_driver_1_1.rowconfigure(index=0, weight=0)
    elif user.is_driver:
        ttk.Label(frame_driver_1, text=f'{user.login}', font=('Helvetica', 20)
                  ).grid(column=0, row=3, padx=(140, 0))

        frame_driver_1_1 = tk.Frame(frame_driver_1)
        frame_driver_1_1.grid(column=0, row=1, sticky='nsew')
        frame_driver_1_1.columnconfigure(index=0, weight=1)
        frame_driver_1_1.rowconfigure(index=0, weight=0)

        route_var_driver.set(value=db.get_driver_path(user.login))
        if route_var_driver.get():
            driver_bus_stops = db.get_bus_stops_for_routes(route_var_driver.get(), False)
            recreate_bus_stop_list_driver(driver_bus_stops)
            r = db.get_driver_path(user.login)
            route_var.set(r)
            create_path(False, db.get_bus_route_info(r, False))
            create_bus_stops(False, db.get_bus_stops_for_routes(r, False))
            recreate_direction_view(False)
        else:
            ttk.Label(frame_driver_1, text='Маршрут не назначен', font=('Helvetica', 20)
                      ).grid(column=0, row=3, padx=(140, 0))

    root.mainloop()
