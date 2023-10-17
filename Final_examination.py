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
        # Панель инструментов "toolbar"
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления
        self.img_add = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text='Добавить', bg='#d7d7d7',
                            bd=0, image=self.img_add,
                            command=self.open_child) 
        btn_add.pack(side=tk.LEFT)

        # Кнопка изменения
        self.img_upd = tk.PhotoImage(file='./img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_upd,
                            command=self.open_update_child) 
        btn_upd.pack(side=tk.LEFT)

        # Кнопка удаления
        self.img_del = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_del,
                            command=self.delete_records) 
        btn_del.pack(side=tk.LEFT)

        # Кнопка поиска (вызова окна поиска)
        self.img_search = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_search,
                            command=self.open_search) 
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления (сброса поиска)
        self.img_refresh = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7',
                            bd=0, image=self.img_refresh,
                            command=self.view_records) 
        btn_refresh.pack(side=tk.LEFT)

        # Таблица
        self.tree = ttk.Treeview(self,
                                columns=('ID', 'name', 'tel', 'email', 'salary'),
                                height=45,
                                show='headings')
        
        # Параметры колонок
        self.tree.column("ID", width = 30, anchor=tk.CENTER)
        self.tree.column("name", width = 300, anchor=tk.CENTER)
        self.tree.column("tel", width = 150, anchor=tk.CENTER)
        self.tree.column("email", width = 150, anchor=tk.CENTER)
        self.tree.column("salary", width = 150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading("ID", text = 'ID')
        self.tree.heading("name", text = 'ФИО')
        self.tree.heading("tel", text = 'Телефон')
        self.tree.heading("email", text = 'E-mail')
        self.tree.heading("salary", text = 'Зарплата')
        
        self.tree.pack(side=tk.LEFT)                                        

        # Добавление скроллбара
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления данных
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    # Отображение данных в treeview
    def view_records(self):
        self.db.cur.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    # Метод посика данных (по ФИО)
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.cur.execute('''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    # Метод обновления (изменения) данных
    def update_record(self, name, tel, email, salary):
        self.db.cur.execute('''UPDATE db SET name = ?, tel = ?, email = ?, salary = ? WHERE ID = ?''',
                           (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления записей
    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cur.execute('''DELETE FROM db WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод вызывающий дочернее окно
    def open_child(self):
        Child()    

     # Метод вызывающий дочернее окно для редактирования данных
    def open_update_child(self):
        Update() 

    # Метод вызывающий дочернее окно для поиска данных
    def open_search(self):
        Search()  

# Класс дочернего окна
class Child(tk.Toplevel): # "Toplevel" - окно верхнего уровня
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализация виджетов дочернего окна
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False, False)
        # Перехватывание всех событий
        self.grab_set()
        # Перехватывание фокуса
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_pay = tk.Label(self, text='Зарплата')
        label_pay.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)
        self.entry_wage = ttk.Entry(self)
        self.entry_wage.place(x=200, y=140)  

        # Кнопка закрытия дочернего окна
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        # Кнопка длбавления
        self.btn_add = tk.Button(self, text='Добавить')
        # Метод "records", которому передаюся значения из строк ввода
        self.btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                    self.entry_email.get(),
                                                                    self.entry_tel.get(),
                                                                    self.entry_wage.get()))
        self.btn_add.place(x=220, y=170)

# Класс дочернего окна для изменения данных
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_email.get(),
                                                                          self.entry_tel.get(),
                                                                          self.entry_wage.get()))
        # Закрытие окна редоктирования
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_add.destroy()

    def default_data(self):
        self.db.cur.execute('''SELECT * FROM db WHERE id=?''',
                           (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        # Доступ к первой записи из выборки
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])
        self.entry_wage.insert(0, row[4])

# Класс окна для поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Инициализация виджетов дочернего окна
    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')

# Класс базы данных
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS db
                        (id integer primary key,
                        name text,
                        tel text,
                        email text,
                        salary text)''')
        self.conn.commit()

    # Добавление данных в БД
    def insert_data(self, name, tel, email, salary):
        self.cur.execute('''INSERT INTO db (name, tel, email, salary)
                        VALUES (?, ?, ?, ?)''',
                        (name, tel, email,salary))
        self.conn.commit()

# При запуске программы
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('800x600')
    root.resizable(False, False)
    root.mainloop()