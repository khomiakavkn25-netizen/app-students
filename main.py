import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

DATA_FILE = "attendance.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"students": [], "subjects": [], "attendance": {}}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


data = load_data()

def add_student():
    name = simpledialog.askstring("Новий студент", "Введіть ПІБ студента:")
    if not name:
        return

    if name in data["students"]:
        messagebox.showerror("Помилка", "Такий студент вже існує.")
        return

    data["students"].append(name)
    data["attendance"][name] = {subj: 0 for subj in data["subjects"]}
    save_data(data)
    messagebox.showinfo("Готово", "Студента додано.")


def delete_student():
    if not data["students"]:
        messagebox.showerror("Помилка", "Немає студентів.")
        return

    name = simpledialog.askstring("Видалити студента", "Введіть ПІБ студента:")
    if name not in data["students"]:
        messagebox.showerror("Помилка", "Студента не знайдено.")
        return

    data["students"].remove(name)
    del data["attendance"][name]
    save_data(data)
    messagebox.showinfo("Готово", "Студента видалено.")


def add_subject():
    subj = simpledialog.askstring("Нова дисципліна", "Введіть назву дисципліни:")
    if not subj:
        return

    if subj in data["subjects"]:
        messagebox.showerror("Помилка", "Така дисципліна вже існує.")
        return

    data["subjects"].append(subj)
    for st in data["students"]:
        data["attendance"][st][subj] = 0

    save_data(data)
    messagebox.showinfo("Готово", "Дисципліну додано.")


def delete_subject():
    if not data["subjects"]:
        messagebox.showerror("Помилка", "Немає дисциплін.")
        return

    subj = simpledialog.askstring("Видалити дисципліну", "Введіть назву дисципліни:")
    if subj not in data["subjects"]:
        messagebox.showerror("Помилка", "Дисципліну не знайдено.")
        return

    data["subjects"].remove(subj)

    for st in data["students"]:
        del data["attendance"][st][subj]

    save_data(data)
    messagebox.showinfo("Готово", "Дисципліну видалено.")


def add_absence():
    if not data["students"] or not data["subjects"]:
        messagebox.showerror("Помилка", "Спочатку додайте студентів і дисципліни.")
        return

    student = simpledialog.askstring("Студент", "Введіть ПІБ студента:")
    if student not in data["students"]:
        messagebox.showerror("Помилка", "Студента не знайдено.")
        return

    subj = simpledialog.askstring("Дисципліна", "Введіть назву дисципліни:")
    if subj not in data["subjects"]:
        messagebox.showerror("Помилка", "Дисципліну не знайдено.")
        return

    data["attendance"][student][subj] += 1
    save_data(data)
    messagebox.showinfo("Готово", "Пропуск зараховано.")


def view_table():
    win = tk.Toplevel(root)
    win.title("Таблиця відвідування")

    cols = ["Студент"] + data["subjects"]
    table = ttk.Treeview(win, columns=cols, show="headings")

    for c in cols:
        table.heading(c, text=c)
        table.column(c, width=120)

    for st in data["students"]:
        row = [st] + [data["attendance"][st][s] for s in data["subjects"]]
        table.insert("", tk.END, values=row)

    table.pack(fill="both", expand=True)


def view_student():
    name = simpledialog.askstring("Студент", "Введіть ПІБ студента:")
    if name not in data["students"]:
        messagebox.showerror("Помилка", "Студента не знайдено.")
        return

    win = tk.Toplevel(root)
    win.title(f"Пропуски – {name}")

    text = tk.Text(win, width=50, height=10)
    for subj, cnt in data["attendance"][name].items():
        text.insert(tk.END, f"{subj}: {cnt}\n")

    text.pack()

root = tk.Tk()
root.title("Облік відвідування занять")

btn1 = tk.Button(root, text="Додати студента", width=30, command=add_student)
btn2 = tk.Button(root, text="Видалити студента", width=30, command=delete_student)
btn3 = tk.Button(root, text="Додати дисципліну", width=30, command=add_subject)
btn4 = tk.Button(root, text="Видалити дисципліну", width=30, command=delete_subject)
btn5 = tk.Button(root, text="Додати пропуск", width=30, command=add_absence)
btn6 = tk.Button(root, text="Переглянути таблицю", width=30, command=view_table)
btn7 = tk.Button(root, text="Переглянути студента", width=30, command=view_student)
btn8 = tk.Button(root, text="Вихід", width=30, command=root.quit)

btn1.pack(pady=3)
btn2.pack(pady=3)
btn3.pack(pady=3)
btn4.pack(pady=3)
btn5.pack(pady=3)
btn6.pack(pady=3)
btn7.pack(pady=3)
btn8.pack(pady=3)

root.mainloop()
