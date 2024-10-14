import tkinter as tk
from tkinter import ttk
from GUI.interface import startMain
from tkinter import messagebox


def open_window():

    autorization_root = tk.Tk()
    autorization_root.title('Окно авторизации')
    autorization_root.geometry("300x200")
    autorization_root.resizable(False, False)
    style = ttk.Style()
    style.theme_use('default')
    style.configure('TButton', padding=10, relief='flat', background='lightblue')
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12))
    frame = ttk.Frame(autorization_root, padding=10)
    frame.pack()
    ttk.Button(frame, text='Кнопка', command=lambda: verify_login(autorization_root)).grid()
    autorization_root.mainloop()


def verify_login(login_window):
    # username, password, login_window
    # Здесь реализуйте логику проверки данных авторизации
    # Например, сравнение с хранимыми в базе данных значениями
    # if username == "admin" and password == "password":
    #     login_window.destroy()  # Закрываем окно авторизации
    #     main_window()  # Открываем основное окно
    # else:
    #     messagebox.showerror("Ошибка", "Неверный логин или пароль")
    if True:
        login_window.destroy()
        startMain()
