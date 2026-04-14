import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

conn = sqlite3.connect("contacts.db")
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    email TEXT,
    address TEXT
)""")
conn.commit()

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()
    
    if not name or not phone:
        messagebox.showerror("Ошибка", "Имя и телефон обязательны")
        return
    
    c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)",
              (name, phone, email, address))
    conn.commit()
    messagebox.showinfo("Успех", "Контакт добавлен")
    clear_fields()
    view_contacts()

def view_contacts():
    listbox.delete(0, tk.END)
    c.execute("SELECT id, name, phone FROM contacts")
    for row in c.fetchall():
        listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]}")

def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите контакт")
        return
    
    item = listbox.get(selected[0])
    contact_id = item.split(" - ")[0]
    
    if messagebox.askyesno("Подтверждение", "Удалить контакт?"):
        c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
        conn.commit()
        view_contacts()
        clear_fields()

def edit_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showerror("Ошибка", "Выберите контакт")
        return
    
    item = listbox.get(selected[0])
    contact_id = item.split(" - ")[0]
    
    c.execute("SELECT name, phone, email, address FROM contacts WHERE id = ?", (contact_id,))
    contact = c.fetchone()
    
    new_name = simpledialog.askstring("Редактирование", "Новое имя:", initialvalue=contact[0])
    new_phone = simpledialog.askstring("Редактирование", "Новый телефон:", initialvalue=contact[1])
    new_email = simpledialog.askstring("Редактирование", "Новый email:", initialvalue=contact[2])
    new_address = simpledialog.askstring("Редактирование", "Новый адрес:", initialvalue=contact[3])
    
    if new_name and new_phone:
        c.execute("UPDATE contacts SET name=?, phone=?, email=?, address=? WHERE id=?",
                  (new_name, new_phone, new_email, new_address, contact_id))
        conn.commit()
        view_contacts()
        messagebox.showinfo("Успех", "Контакт обновлён")

def search_contact():
    keyword = simpledialog.askstring("Поиск", "Введите имя или телефон:")
    if keyword:
        listbox.delete(0, tk.END)
        c.execute("SELECT id, name, phone FROM contacts WHERE name LIKE ? OR phone LIKE ?",
                  (f"%{keyword}%", f"%{keyword}%"))
        for row in c.fetchall():
            listbox.insert(tk.END, f"{row[0]} - {row[1]} - {row[2]}")

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

def load_contact_to_form(event):
    selected = listbox.curselection()
    if not selected:
        return
    
    item = listbox.get(selected[0])
    contact_id = item.split(" - ")[0]
    
    c.execute("SELECT name, phone, email, address FROM contacts WHERE id = ?", (contact_id,))
    contact = c.fetchone()
    
    clear_fields()
    name_entry.insert(0, contact[0])
    phone_entry.insert(0, contact[1])
    email_entry.insert(0, contact[2] if contact[2] else "")
    address_entry.insert(0, contact[3] if contact[3] else "")

root = tk.Tk()
root.title("Контактная книга")
root.geometry("800x500")

left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

tk.Label(left_frame, text="Имя:", font=("Arial", 10)).pack(anchor="w")
name_entry = tk.Entry(left_frame, width=30)
name_entry.pack(fill="x", pady=5)

tk.Label(left_frame, text="Телефон:", font=("Arial", 10)).pack(anchor="w")
phone_entry = tk.Entry(left_frame, width=30)
phone_entry.pack(fill="x", pady=5)

tk.Label(left_frame, text="Email:", font=("Arial", 10)).pack(anchor="w")
email_entry = tk.Entry(left_frame, width=30)
email_entry.pack(fill="x", pady=5)

tk.Label(left_frame, text="Адрес:", font=("Arial", 10)).pack(anchor="w")
address_entry = tk.Entry(left_frame, width=30)
address_entry.pack(fill="x", pady=5)

tk.Button(left_frame, text="Добавить", command=add_contact, bg="green", fg="white", width=20).pack(pady=5)
tk.Button(left_frame, text="Редактировать", command=edit_contact, bg="orange", fg="white", width=20).pack(pady=5)
tk.Button(left_frame, text="Удалить", command=delete_contact, bg="red", fg="white", width=20).pack(pady=5)
tk.Button(left_frame, text="Поиск", command=search_contact, bg="blue", fg="white", width=20).pack(pady=5)
tk.Button(left_frame, text="Очистить поля", command=clear_fields, bg="gray", fg="white", width=20).pack(pady=5)

tk.Label(right_frame, text="Список контактов:", font=("Arial", 12, "bold")).pack()
listbox = tk.Listbox(right_frame, width=50, height=20)
listbox.pack(fill=tk.BOTH, expand=True)
listbox.bind("<<ListboxSelect>>", load_contact_to_form)

view_contacts()
root.mainloop()
conn.close()