import tkinter as tk
from tkinter import ttk
import sqlite3

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
  
  


# Инициализация виджетов главного окна
    def init_main(self):
        # Верхняя панель для кнопок
        toolbar = tk.Frame(bg='#BC8F8F',  bd=2,)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./project/img/add.png')
        # Создание кнопки
        btn_open_dialog = tk.Button(toolbar, bg='#BC8F8F', bd=0, 
                                    image=self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # Кнопка  редактирования
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        # Создание кнопки
        btn_upd_open_dialog = tk.Button(toolbar, bg='#BC8F8F', bd=0, 
                                    image=self.upd_img,
                                    command=self.open_update_dialog)
        btn_upd_open_dialog.pack(side=tk.LEFT)

        # Кнопка удаления записей 
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        # Создание кнопки
        btn_del_open_dialog = tk.Button(toolbar, bg='#BC8F8F', bd=0, 
                                    image=self.del_img,
                                    command=self.delete_record)
        btn_del_open_dialog.pack(side=tk.LEFT)


        # содание кнопки поиска по фио
        self.search_img = tk.PhotoImage(file='./img/search.png')
        # Создание кнопки
        btn_search_dialog = tk.Button(toolbar, bg='#BC8F8F', bd=0, 
                                    image=self.search_img,
                                    command=self.open_search_dialog)
        btn_search_dialog.pack(side=tk.LEFT)



        # Кнопка обновления данных
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        # Создание кнопки
        btn_refresh = tk.Button(toolbar, bg='#BC8F8F', bd=0, 
                                    image=self.refresh_img,
                                    command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)



      # Создание Treeview (таблица)
    # Скрываем нулевой столбец show='headings'
        self.tree = ttk.Treeview(self,
                                  columns=['ID', 'name', 'phone', 'email', 'salary'],
                                  height=50, show='headings')


        # задаем ширину и выравнивание текста
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)   
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # задаем  подписи к столбцам
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)


        # скроллбар
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


# Метод для вызова добавления данных в базу данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary, )
        self.view_records()

# метод изменения данных
    def update_record(self, name, phone, email, salary):
        self.db.c.execute('''
                    UPDATE employees
                    SET name = ?, phone = ?, email = ?, salary = ?
                    WHERE id = ?''', (name, phone, email, salary,
                                      self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

# удаление выделенных данных
    def delete_record(self):
        for sel_row in self.tree.selection():
            self.db.c.execute('''
                DELETE FROM employees
                WHERE id=?''', (self.tree.set(sel_row, '#1'), ))
        self.db.conn.commit()
        self.view_records()


# метод поиска записи
    def search_records(self, name):
        self.db.c.execute('''SELECT *
                            FROM employees
                            WHERE name LIKE ?''', ('%' + name + '%' ,))
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]


# Метод отбражения данных
    def view_records(self):
        self.db.c.execute('''SELECT * FROM employees''')
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]


    def open_dialog(self):
        Child()


    def open_update_dialog(self):
        Update()


    def open_search_dialog(self):
        Search()    


# Класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


# Инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200+200+200')
        self.resizable(False, False)
        # перехватываем все события
        self.grab_set()
        # фокус
        self.focus_set()

        label_name =tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_phone =tk.Label(self, text='Телефон')
        label_phone.place(x=50, y=80)
        label_email =tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary =tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=170, y=50)
        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=170, y=80)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=170, y=110)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=170, y=140)

        # Кнопки закытия и добавления

        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=230, y=170)
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records(
                                        self.entry_name.get(), 
                                        self.entry_phone.get(),
                                        self.entry_email.get(),
                                        self.entry_salary.get())) 
        self.btn_ok.place(x=300, y=170)


# Класс для изменения данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.load_data()


# инициализация виджетов окна редактирования

    def init_edit(self):
        self.title('Редактирование конакта')
        btn_edit = tk.Button(self, text='Изменить')
        btn_edit.bind('<Button-1>',  lambda ev: self.view.update_record(self.entry_name.get(), 
                                         self.entry_phone.get(),
                                         self.entry_email.get(), 
                                         self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        btn_edit.place(x=300, y=170)
        self.btn_ok.destroy()

    # подстановка данных в редактирование 
    def load_data(self):
        self.db.c.execute('''
                        SELECT * 
                        FROM employees 
                        WHERE id = ?''', self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])
        
#### класс дочернего окна поиска по фио

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app


# Инициализация виджетов дочернего окна поиска
    def init_child(self):
        self.title('Поиск')
        self.geometry('400x200+200+200')
        self.resizable(False, False)
        # перехватываем все события
        self.grab_set()
        # фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=65)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=170, y=65)


        # Кнопки закрытия и поиска

        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=230, y=140)

        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=300, y=140)


####
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('employees.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS employees (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                salary TEXT)''')
        self.conn.commit()

#  Добавление в базу данных
    def insert_data(self, name, phone, email, salary):
        self.c.execute('''INSERT INTO employees (name, phone, email, salary)
                          VALUES (?, ?, ?, ?)''', (name, phone, email, salary))
        self.conn.commit()

if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Сотрудники')
    root.geometry('800x450+300+200')
    root.resizable(False, False)
    root.mainloop()