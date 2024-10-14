import tkinter as tk
from tkinter import ttk
from GUI.interface import startMain
from tkinter import messagebox


def open_window():
    autorization_root = tk.Tk()
    autorization_root.title('Окно авторизации')
    ttk.Button(autorization_root, text='Кнопка', command=lambda: verify_login(autorization_root)).grid()
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
