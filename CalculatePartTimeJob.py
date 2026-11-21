import sqlite3
import tkinter as tk
from tkinter import messagebox , ttk
from datetime import datetime
from tkcalendar import DateEntry
import os

BASE = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(os.path.join(BASE, "worktime.db"))
conn.execute("CREATE TABLE IF NOT EXISTS worklog (date TEXT, entry TEXT, exit TEXT, minutes INTEGER)")

def load_data():
    tree.delete(*tree.get_children())
    rows = conn.execute(
        "SELECT date, entry, exit, minutes FROM worklog ORDER BY date DESC"
    ).fetchall()
    for r in rows:
        tree.insert("", "end", values=(r[0], r[1], r[2], f"{r[3] // 60}:{r[3] % 60:02d}"))
    total = sum(r[3] for r in rows)
    # try:
    #     totalamount=float(salary.get())
    # except ValueError:
    #     totalamount = 0
    
    totalamount=100* (total/60)
    total_label.config(text=f"{len(rows)}: تعداد روز  \n جمع کل:{total // 60} ساعت و {total % 60} دقیقه\n حقوق دریافتی :{totalamount:,.2f}")



def save():
    try:
        t_in = datetime.strptime(entryTime.get(), "%H:%M")
        t_out = datetime.strptime(exitTime.get(), "%H:%M")
    except ValueError:
        messagebox.showerror("خطا", "ساعت را به شکل 08:30 وارد کنید")
        return
    minutes = int((t_out - t_in).total_seconds() // 60) % (24 * 60)
    conn.execute("INSERT INTO worklog VALUES (?, ?, ?, ?)",
                 (date_entry.get_date().isoformat(), entryTime.get(), exitTime.get(), minutes))
    conn.commit()
    messagebox.showinfo("ثبت شد", f"مدت کار: {minutes // 60} ساعت و {minutes % 60} دقیقه")

root = tk.Tk()
root.title("محاسبه ساعت کاری")

tk.Label(root, text="تاریخ :").pack()
date_entry = DateEntry(root, date_pattern="yyyy-mm-dd")
date_entry.pack(padx=10, pady=10)

tk.Label(root, text="ساعت ورود:").pack()
entryTime = tk.Entry(root)
entryTime.pack()

tk.Label(root, text="ساعت خروج:").pack()
exitTime = tk.Entry(root)
exitTime.pack()

tk.Label(root, text=" اضافه کاری :").pack()
salary = tk.Entry(root)
salary.pack()

tk.Button(root, text="ثبت", command=save).pack(pady=10)

frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

columns = ("date", "entry", "exit", "duration")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
for col, title, width in [
    ("date", "تاریخ", 100),
    ("entry", "ورود", 70),
    ("exit", "خروج", 70),
    ("duration", "مدت", 70),
]:
    tree.heading(col, text=title)
    tree.column(col, width=width, anchor="center")

vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

total_label = tk.Label(root, text="")
total_label.pack(pady=(0, 8))

load_data()  
root.mainloop()