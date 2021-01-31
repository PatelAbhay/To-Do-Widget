import tkinter as tk
from tkinter import messagebox
from win10toast import ToastNotifier
import threading
import sys
import datetime
import time
import sqlite3


class Window(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        sys.exit()

    def syncDatabase(self):
        while(len(self.task_list) > 0):
            self.task_list.pop()
        
        self.curs.execute('SELECT * FROM tasks')
        rows = self.curs.fetchall()
        for row in rows:
            print(row)
            self.task_list.append(row[0])
            self.dates[row[0]] = row[1]

    def run(self):
        self.task_list = []
        self.dates = {}

        self.toaster = ToastNotifier()

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('To-Do List')
        self.root.geometry("400x250")
        self.root.attributes('-alpha', 0.8)
        self.root.resizable(0, 0)

        self.entry_label = tk.Label(self.root, text='Enter task title: ')
        self.task_name = tk.Entry(self.root, width=21)
        self.date_label = tk.Label(
            self.root, text='Enter due date (yyyy-mm-dd): ')
        self.end_date = tk.Entry(self.root, width=21)
        self.current_tasks = tk.Listbox(
            self.root, width=28, height=14, selectmode='SINGLE')
        self.add_btn = tk.Button(self.root, text='Add task',
                                 width=20, command=self.addTask)
        self.remove_btn = tk.Button(self.root, text='Delete',
                                    width=20, command=self.deleteTask)
        self.delete_all_btn = tk.Button(self.root, text='Delete all',
                                        width=20, command=self.deleteAll)

        self.entry_label.place(x=30, y=10)
        self.task_name.place(x=33, y=30)
        self.date_label.place(x=30, y=60)
        self.end_date.place(x=33, y=80)
        self.add_btn.place(x=30, y=110)
        self.remove_btn.place(x=30, y=140)
        self.delete_all_btn.place(x=30, y=170)
        self.current_tasks.place(x=210, y=10)

        self.db = sqlite3.connect('database.db')
        self.curs = self.db.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS tasks
             (name, date)''')

        self.syncDatabase()
        self.updateList()
        print(self.task_list)

        self.root.mainloop()

        self.db.commit()
        self.cur.close()

    def addTask(self):
        name = self.task_name.get()
        date = self.end_date.get()
        if len(name) == 0:
            messagebox.showinfo('Empty Entry', 'Enter task name')
        elif len(date) != 10:
            messagebox.showinfo(
                'Invalid Date', 'Remember to follow the date format provided')
        else:
            if name in self.task_list:
                messagebox.showinfo(
                    'Task Already in List', 'A task with the same name is in the list already')
            else:
                self.task_list.append(name)
                self.dates[name] = [date, False]
                self.curs.execute('INSERT INTO tasks (task, date) VALUES (?,?)', (name,date))
                self.db.commit()
                self.updateList()
                print(self.task_list)
                self.task_name.delete(0, 'end')
                self.end_date.delete(0, 'end')

    def updateList(self):
        self.current_tasks.delete(0, 'end')
        for task in self.task_list:
            self.current_tasks.insert('end', task)

    def deleteTask(self):
        try:
            name = self.current_tasks.get(self.current_tasks.curselection())
            if name in self.task_list:
                self.task_list.remove(name)
                self.dates.pop(name)
                self.curs.execute('DELETE from tasks where task = (?)', (name))
                self.db.commit()
                self.updateList()
        except:
            messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

    def deleteAll(self):
        popup = messagebox.askyesno('Delete All', 'Are you sure?')
        if popup == True:
            while(len(self.task_list) != 0):
                self.task_list.pop()
                self.dates.pop()
            self.curs.execute('DELETE from tasks')
            self.db.commit()
            self.updateList()

    def sendNotification(self, task_name):
        self.toaster.show_toast(
            "Task Due Today!", task_name + " is due today!")
        self.dates[task_name][1] = True


window = Window()

while True:
    today = str(datetime.date.today())

    for key in window.dates:
        print(window.dates[key])
        if today == window.dates[key][0] and not window.dates[key][1]:
            window.sendNotification(key)
            time.sleep(3)

    if not window.is_alive():
        sys.exit()

    time.sleep(5)
