author: om. uran. - 2026/04/06
# Приложение для проверки паролей

Это простая программа с окошками, которая помогает придумывать и проверять пароли.

## Что она умеет?

- **Регистрация** – можно создать нового пользователя с логином и паролем
- **Вход** – войти под своим логином и паролем
- **Проверка сложности пароля** – пока вы вводите пароль, программа сразу пишет: "Слабый", "Средний" или "Сильный"
  - Слабый – короткий или только буквы
  - Средний – лучше, но не идеал
  - Сильный – длинный, есть заглавные буквы, цифры и спецсимволы
- **Смена пароля** – уже после входа можно сменить пароль
- **Проверить любой пароль** – можно ввести любой пароль и узнать его сложность

## Как запустить?

1. Установите Python (если ещё нет).
2. Сохраните код в файл, например `password_app.py`
3. Откройте командную строку в папке с файлом и напишите:


## Важно знать

- Все логины и пароли хранятся в памяти компьютера только пока работает программа. Закроете окно – всё сотрётся
- Пароли не шифруются, так что для реального использования не подойдёт. Просто учебный пример

## Как пользоваться?

1. При запуске увидите окно входа. Если вы ещё не зарегистрированы – нажмите "Регистрация"
2. При регистрации придумайте логин и пароль. Программа покажет, насколько пароль надёжный
3. Если пароль слабый – спросит "точно продолжать?"
4. После регистрации войдите с логином и паролем
5. Внутри можно сменить пароль, проверить чужой пароль или выйти

Программа использует только встроенные библиотеки Python – ничего дополнительно устанавливать не нужно.

- **tkinter** – создаёт графический интерфейс: окна, кнопки, поля для ввода и т.д.
- **re** (регулярные выражения) – проверяет, есть ли в пароле заглавные буквы, цифры или спецсимволы.
- **messagebox** (часть tkinter) – показывает всплывающие сообщения (ошибки, подтверждения).
- **simpledialog** (часть tkinter) – открывает маленькие окошки для ввода (например, для смены пароля).

Все эти библиотеки уже есть в Python, ничего дополнительно ставить не нужно.



## ENGLISH
## Important notes

- All logins and passwords are stored only in your computer's memory while the program runs. Close the window – everything is gone.
- Passwords are not encrypted, so don't use this for real accounts. It's just a learning example.

## How to use?

1. When you start, you see a login window. If you haven't signed up, click "Sign up".
2. During sign up, choose a login and a password. The app will show you how strong the password is.
3. If the password is weak, it will ask "Are you sure?".
4. After signing up, log in with your login and password.
5. Inside the main window you can change your password, check any other password, or log out.

That's it! 😊

---

## Libraries used

### English

The program uses only built‑in Python libraries – no extra installation needed.

- **tkinter** – creates the graphical interface: windows, buttons, text fields, etc.
- **re** (regular expressions) – checks if the password contains uppercase letters, digits, or special characters.
- **messagebox** (part of tkinter) – shows pop‑up messages like errors or confirmations.
- **simpledialog** (part of tkinter) – opens small input windows (e.g., for changing password).

All these libraries come with Python by default.

GOOD LUCK WITH PROJECT!
