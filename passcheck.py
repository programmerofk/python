import tkinter as tk
from tkinter import messagebox, simpledialog
import re

def check_strength(pwd):
    score = sum([
        len(pwd) >= 8,
        bool(re.search(r'[A-Z]', pwd)),
        bool(re.search(r'[0-9]', pwd)),
        bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd))
    ])
    if score <= 1:
        return "Слабый", "red"
    elif score == 2:
        return "Средний", "orange"
    else:
        return "Сильный", "green"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Проверка пароля")
        self.root.geometry("450x400")
        self.root.configure(bg="#f0f0f0")
        self.users = {}
        self.current_user = None
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_login(self):
        self.clear()
        self.root.configure(bg="#f0f0f0")
        tk.Label(self.root, text="Вход", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=5)
        tk.Label(frame, text="Логин:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.login_entry = tk.Entry(frame)
        self.login_entry.pack(side=tk.LEFT)

        frame2 = tk.Frame(self.root, bg="#f0f0f0")
        frame2.pack(pady=5)
        tk.Label(frame2, text="Пароль:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.pass_entry = tk.Entry(frame2, show="*")
        self.pass_entry.pack(side=tk.LEFT)

        tk.Button(self.root, text="Войти", command=self.login, bg="#2196F3", fg="white", width=15).pack(pady=10)
        tk.Button(self.root, text="Регистрация", command=self.show_reg, bg="#4CAF50", fg="white", width=15).pack()

    def show_reg(self):
        self.clear()
        self.root.configure(bg="#f0f0f0")
        tk.Label(self.root, text="Регистрация", font=("Arial", 20, "bold"), bg="#f0f0f0").pack(pady=20)

        f1 = tk.Frame(self.root, bg="#f0f0f0")
        f1.pack(pady=5)
        tk.Label(f1, text="Логин:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.reg_login = tk.Entry(f1)
        self.reg_login.pack(side=tk.LEFT)

        f2 = tk.Frame(self.root, bg="#f0f0f0")
        f2.pack(pady=5)
        tk.Label(f2, text="Пароль:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.reg_pass = tk.Entry(f2, show="*")
        self.reg_pass.pack(side=tk.LEFT)

        self.strength_label = tk.Label(self.root, text="", bg="#f0f0f0", font=("Arial", 10))
        self.strength_label.pack()
        def update_strength(event=None):
            pwd = self.reg_pass.get()
            if pwd:
                text, col = check_strength(pwd)
                self.strength_label.config(text=f"Сложность: {text}", fg=col)
            else:
                self.strength_label.config(text="")
        self.reg_pass.bind("<KeyRelease>", update_strength)

        f3 = tk.Frame(self.root, bg="#f0f0f0")
        f3.pack(pady=5)
        tk.Label(f3, text="Подтвердите:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        self.reg_confirm = tk.Entry(f3, show="*")
        self.reg_confirm.pack(side=tk.LEFT)

        tk.Button(self.root, text="Зарегистрироваться", command=self.register, bg="#4CAF50", fg="white", width=20).pack(pady=10)
        tk.Button(self.root, text="Назад", command=self.show_login, bg="#cccccc", width=20).pack()

    def register(self):
        log = self.reg_login.get().strip()
        pwd = self.reg_pass.get()
        conf = self.reg_confirm.get()
        if not log or not pwd:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        if pwd != conf:
            messagebox.showerror("Ошибка", "Пароли не совпадают")
            return
        text, _ = check_strength(pwd)
        if text == "Слабый" and not messagebox.askyesno("Внимание", "Ваш пароль слишком слабый. Продолжить?"):
            return
        self.users[log] = pwd
        messagebox.showinfo("Успех", "Регистрация завершена")
        self.show_login()

    def login(self):
        log = self.login_entry.get().strip()
        pwd = self.pass_entry.get()
        if self.users.get(log) == pwd:
            self.current_user = log
            self.show_main()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")

    def show_main(self):
        self.clear()
        self.root.configure(bg="#f0f0f0")
        tk.Label(self.root, text=f"Добро пожаловать, {self.current_user}!", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)
        tk.Button(self.root, text="Сменить пароль", command=self.change_pass, bg="#FF9800", fg="white", width=20).pack(pady=5)
        tk.Button(self.root, text="Проверить пароль", command=self.check_any_pass, bg="#9C27B0", fg="white", width=20).pack(pady=5)
        tk.Button(self.root, text="Выйти", command=self.show_login, bg="#f44336", fg="white", width=20).pack(pady=20)

    def change_pass(self):
        new = simpledialog.askstring("Смена пароля", "Введите новый пароль:", show="*")
        if not new:
            return
        text, _ = check_strength(new)
        if text == "Слабый" and not messagebox.askyesno("Внимание", "Новый пароль слабый. Продолжить?"):
            return
        self.users[self.current_user] = new
        messagebox.showinfo("Успех", "Пароль изменён")

    def check_any_pass(self):
        pwd = simpledialog.askstring("Проверка пароля", "Введите пароль для проверки:", show="*")
        if pwd:
            text, col = check_strength(pwd)
            messagebox.showinfo("Результат", f"Сложность пароля: {text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()