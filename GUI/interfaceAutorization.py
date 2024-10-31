import tkinter as tk
from tkinter import ttk
from GUI.interface import startMain
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import DATABASE.database_2 as db


def open_window():
    class ClickableLabel(ctk.CTkLabel):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.bind("<Button-1>", self.registration)

        @staticmethod
        def registration(event):
            # db.set_user(login_entry.get(), password_entry.get())
            open_reg_window(autorization_root, is_driver_var)

    autorization_root = tk.Tk()
    is_driver_var = tk.IntVar(value=0)
    autorization_root.title('Окно авторизации')
    autorization_root.geometry("500x400+525+200")
    autorization_root.resizable(False, False)

    style = ttk.Style()
    style.configure('TButton', font=('Bolt', 20), padding=(10, 10))

    frame = ttk.Frame(autorization_root, padding=10)
    frame.pack()
    ttk.Label(frame, text='Авторизация', font=('Bolt', 20)).grid(column=0, columnspan=2, padx=10, pady=10)
    ttk.Label(frame, text='Логин', font=('Bolt', 16)).grid(column=0, row=1, padx=10, pady=10)
    login_entry = ttk.Entry(frame, font=('Bolt', 16))
    login_entry.grid(column=1, row=1, padx=10, pady=10)
    ttk.Label(frame, text='Пароль', font=('Bolt', 16)).grid(column=0, row=2, padx=10, pady=10)
    password_entry = ttk.Entry(frame, font=('Bolt', 16), show='*')
    password_entry.grid(column=1, row=2, padx=10, pady=10)

    reg_label = ClickableLabel(frame, text='Регистрация', font=('Bolt', 16), text_color='blue')
    reg_label.grid(column=0, row=3, columnspan=2, padx=10, pady=10)

    ttk.Button(frame, text='Войти',
               command=lambda: verify_login(login_entry.get(), password_entry.get(), autorization_root),
               style='TButton').grid(column=0, columnspan=2, padx=10, pady=10)

    image = Image.open("Resources/bus_autoriz.png")
    image = image.resize((100, 100))
    photo = ImageTk.PhotoImage(image)
    # Создаем метку и устанавливаем изображение
    label = ttk.Label(frame, image=photo)
    label.grid(column=0, columnspan=2, padx=10, pady=10)

    autorization_root.mainloop()


def verify_login(username, password, login_window):
    if db.user_check(username, password):
        login_window.destroy()
        startMain(db.is_admin(username), db.is_driver(username))
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")


def open_reg_window(autorization_root, d_var):
    autorization_root.withdraw()
    # Создаем новое окно
    new_window = tk.Toplevel(autorization_root)
    new_window.title('Окно авторизации')
    new_window.geometry("400x300+575+250")
    new_window.resizable(False, False)

    frame = ttk.Frame(new_window, padding=10)
    frame.pack()

    ttk.Label(frame, text='Регистрация', font=('Bolt', 20)).grid(column=0, columnspan=2, padx=10, pady=10)
    ttk.Label(frame, text='Логин', font=('Bolt', 16)).grid(column=0, row=1, padx=10, pady=10)

    login_entry = ttk.Entry(frame, font=('Bolt', 16))
    login_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(frame, text='Пароль', font=('Bolt', 16)).grid(column=0, row=2, padx=10, pady=10)

    password_entry = ttk.Entry(frame, font=('Bolt', 16), show='*')
    password_entry.grid(column=1, row=2, padx=10, pady=10)

    style_check = ttk.Style()
    style_check.configure('TCheckbutton', font=('Helvetica', 20))
    ttk.Checkbutton(frame, text='Вы водитель?',
                    variable=d_var,
                    style='TCheckbutton',
                    takefocus=False
                    ).grid(column=0, columnspan=2)

    ttk.Button(frame, text='Зарегистрироваться',
               command=lambda: reg_user_command(login_entry.get(), password_entry.get(),
                                                new_window, autorization_root, d_var),
               style='TButton').grid(column=0, columnspan=2, padx=10, pady=10)

    def on_closing():
        autorization_root.deiconify()
        new_window.destroy()

    new_window.protocol("WM_DELETE_WINDOW", on_closing)


def reg_user_command(login, password, window, autorization_root, d_var):
    user_set = db.set_user(login, password, d_var.get())
    if user_set:
        messagebox.showinfo("Инфо", "Регистрация выполнена успешно")
        autorization_root.deiconify()
        window.destroy()
    else:
        messagebox.showerror("Инфо", "Ошибка регистрации")
