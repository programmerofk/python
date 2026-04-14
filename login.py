import tkinter as tk              # Подключаем tkinter для создания окна (GUI)
from tkinter import messagebox   # Для всплывающих окон (ошибки, успех и т.д.)
import sqlite3                   # База данных SQLite (будем хранить пользователей)
import re                        # Для проверки пароля через регулярные выражения

# Подключаемся к базе данных (если файла нет — он создастся)
conn = sqlite3.connect("users.db")
c = conn.cursor()  # "курсор" — через него выполняем SQL команды

# Создаем таблицу users, если её ещё нет
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  # Уникальный ID (сам увеличивается)
    login TEXT UNIQUE,                    # Логин (уникальный)
    password TEXT                         # Пароль (пока без шифрования)
)""")
conn.commit()  # Сохраняем изменения

# Функция проверки сложности пароля
def check_strength(password):
    score = 0  # Счётчик "силы" пароля
    
    if len(password) >= 8:  # Если длина >= 8
        score += 1
    if re.search(r'[A-Z]', password):  # Есть ли заглавные буквы
        score += 1
    if re.search(r'[0-9]', password):  # Есть ли цифры
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Есть ли спецсимволы
        score += 1
    
    # Возвращаем уровень сложности и цвет
    if score <= 1:
        return "Слабый", "red"
    elif score == 2:
        return "Средний", "orange"
    else:
        return "Сильный", "green"

# Эта функция обновляет текст "Сложность пароля" при вводе
def update_strength_label(event=None):
    password = pass_entry.get()  # Берем текст из поля пароля
    
    if password:
        text, color = check_strength(password)  # Проверяем сложность
        strength_label.config(text=f"Сложность: {text}", fg=color)  # Меняем текст и цвет
    else:
        strength_label.config(text="")  # Если пусто — убираем надпись

# Функция регистрации
def register():
    login = login_entry.get()      # Берём логин из поля
    password = pass_entry.get()    # Берём пароль
    confirm = confirm_entry.get()  # Берём подтверждение
    
    # Проверка: все ли поля заполнены
    if not login or not password:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return
    
    # Проверка: совпадают ли пароли
    if password != confirm:
        messagebox.showerror("Ошибка", "Пароли не совпадают")
        return
    
    # Проверка сложности пароля
    text, _ = check_strength(password)
    
    # Если пароль слабый — спрашиваем "ты точно хочешь?"
    if text == "Слабый" and not messagebox.askyesno("Внимание", "Ваш пароль слишком слабый. Продолжить?"):
        return
    
    try:
        # Пытаемся добавить пользователя в базу
        c.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
        conn.commit()  # Сохраняем
        
        messagebox.showinfo("Успех", "Регистрация завершена")
        clear_fields()  # Очищаем поля
        strength_label.config(text="")  # Убираем текст сложности
        
    except sqlite3.IntegrityError:
        # Если логин уже есть (из-за UNIQUE)
        messagebox.showerror("Ошибка", "Такой логин уже существует")

# Функция входа
def login():
    login = login_entry.get()
    password = pass_entry.get()
    
    # Проверяем есть ли такой пользователь
    c.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    
    if c.fetchone():  # Если нашли — вход успешный
        messagebox.showinfo("Успех", f"Добро пожаловать, {login}!")
        clear_fields()
        strength_label.config(text="")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Очистка всех полей ввода
def clear_fields():
    login_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    confirm_entry.delete(0, tk.END)

# --- СОЗДАНИЕ ОКНА ---
root = tk.Tk()
root.title("Система регистрации и входа")  # Заголовок окна
root.geometry("350x350")  # Размер окна

# Поле логина
tk.Label(root, text="Логин:").pack(pady=5)
login_entry = tk.Entry(root)
login_entry.pack()

# Поле пароля
tk.Label(root, text="Пароль:").pack(pady=5)
pass_entry = tk.Entry(root, show="*")  # show="*" скрывает пароль
pass_entry.pack()

# Отслеживаем ввод (каждую клавишу) — чтобы обновлять сложность
pass_entry.bind("<KeyRelease>", update_strength_label)

# Надпись сложности пароля
strength_label = tk.Label(root, text="", font=("Arial", 10))
strength_label.pack()

# Поле подтверждения пароля
tk.Label(root, text="Подтверждение пароля:").pack(pady=5)
confirm_entry = tk.Entry(root, show="*")
confirm_entry.pack()

# Кнопка регистрации
tk.Button(root, text="Зарегистрироваться", command=register, bg="green", fg="white").pack(pady=5)

# Кнопка входа
tk.Button(root, text="Войти", command=login, bg="blue", fg="white").pack(pady=5)

# Запуск программы (бесконечный цикл окна)
root.mainloop()

# Закрываем базу данных при завершении
conn.close()