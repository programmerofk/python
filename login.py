import tkinter as tk
from tkinter import messagebox
import sqlite3
import re

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT UNIQUE,
    password TEXT
)""")
conn.commit()

def check_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r'[A-Z]', password):
        score += 1
    if re.search(r'[0-9]', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    
    if score <= 1:
        return "Слабый", "red"
    elif score == 2:
        return "Средний", "orange"
    else:
        return "Сильный", "green"

def update_strength_label(event=None):
    password = pass_entry.get()
    if password:
        text, color = check_strength(password)
        strength_label.config(text=f"Сложность: {text}", fg=color)
    else:
        strength_label.config(text="")

def register():
    login = login_entry.get()
    password = pass_entry.get()
    confirm = confirm_entry.get()
    
    if not login or not password:
        messagebox.showerror("Ошибка", "Заполните все поля")
        return
    
    if password != confirm:
        messagebox.showerror("Ошибка", "Пароли не совпадают")
        return
    
    text, _ = check_strength(password)
    if text == "Слабый" and not messagebox.askyesno("Внимание", "Ваш пароль слишком слабый. Продолжить?"):
        return
    
    try:
        c.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
        conn.commit()
        messagebox.showinfo("Успех", "Регистрация завершена")
        clear_fields()
        strength_label.config(text="")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Такой логин уже существует")

def login():
    login = login_entry.get()
    password = pass_entry.get()
    
    c.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password))
    if c.fetchone():
        messagebox.showinfo("Успех", f"Добро пожаловать, {login}!")
        clear_fields()
        strength_label.config(text="")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

def clear_fields():
    login_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)
    confirm_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Система регистрации и входа")
root.geometry("350x350")

tk.Label(root, text="Логин:").pack(pady=5)
login_entry = tk.Entry(root)
login_entry.pack()

tk.Label(root, text="Пароль:").pack(pady=5)
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()
pass_entry.bind("<KeyRelease>", update_strength_label)

strength_label = tk.Label(root, text="", font=("Arial", 10))
strength_label.pack()

tk.Label(root, text="Подтверждение пароля:").pack(pady=5)
confirm_entry = tk.Entry(root, show="*")
confirm_entry.pack()

tk.Button(root, text="Зарегистрироваться", command=register, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Войти", command=login, bg="blue", fg="white").pack(pady=5)

root.mainloop()
conn.close()