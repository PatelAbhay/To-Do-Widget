import tkinter as tk
from tkinter import messagebox
from win10toast import ToastNotifier
import threading
import sys
import datetime
import time


task_list = []
dates = {}


class Window(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        sys.exit()

    def run(self):
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

        self.root.mainloop()

    def addTask(self):
        name = self.task_name.get()
        date = self.end_date.get()
        if len(name) == 0:
            messagebox.showinfo('Empty Entry', 'Enter task name')
        elif len(date) != 10:
            messagebox.showinfo(
                'Invalid Date', 'Remember to follow the date format provided')
        else:
            if name in task_list:
                messagebox.showinfo(
                    'Task Already in List', 'A task with the same name is in the list already')
            else:
                task_list.append(name)
                dates[name] = [date, False]
                self.listUpdate()
                self.task_name.delete(0, 'end')
                self.end_date.delete(0, 'end')

    def updateList(self):
        self.current_tasks.delete(0, 'end')
        for task in task_list:
            self.current_tasks.insert('end', task)

    def deleteTask(self):
        try:
            name = self.current_tasks.get(self.current_tasks.curselection())
            if name in task_list:
                task_list.remove(name)
                dates.pop(name)
                self.updateList()
        except:
            messagebox.showinfo('Cannot Delete', 'No Task Item Selected')

    def deleteAll(self):
        popup = messagebox.askyesno('Delete All', 'Are you sure?')
        if popup == True:
            while(len(task_list) != 0):
                task_list.pop()
                dates.pop()
            self.updateList()

    def sendNotification(self, task_name):
        self.toaster.show_toast(
            "Task Due Today!", task_name + " is due today!")
        dates[task_name][1] = True


window = Window()

while True:
    today = str(datetime.date.today())

    for key in dates:
        print(dates[key])
        if today == dates[key][0] and not dates[key][1]:
            window.sendNotification(key)
            time.sleep(3)

    if not window.is_alive():
        sys.exit()

    time.sleep(5)
