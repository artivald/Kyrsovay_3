import sqlite3
import tkinter as tk
from tkinter import ttk
import random
import string
from tkinter import ttk, filedialog, messagebox


def clear_window():
    # Перебираем виджеты кроме меню
    for widget in root.winfo_children():
        if widget != menu_bar:
            widget.destroy()

    load_data(filename)


def edit_user():
    global tree_var
    global filename
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    edit_window = tk.Toplevel(root)
    edit_window.title("Редактировать пользователя")

    frame = tk.Frame(edit_window)
    frame.pack(fill=tk.X)

    id_entry = tk.Entry(frame)
    surname_entry = tk.Entry(frame)
    name_entry = tk.Entry(frame)
    patronymic_entry = tk.Entry(frame)
    login_entry = tk.Entry(frame)
    password_entry = tk.Entry(frame)
    division_entry = tk.Entry(frame)
    post_entry = tk.Entry(frame)
    faculty_var = tk.StringVar(edit_window)

    id_label = tk.Label(frame, text="ID")
    surname_label = tk.Label(frame, text="Фамилия")
    name_label = tk.Label(frame, text="Имя")
    patronymic_label = tk.Label(frame, text="Отчество")
    login_label = tk.Label(frame, text="Логин")
    password_label = tk.Label(frame, text="Пароль")
    division_label = tk.Label(frame, text="Подразделение")
    post_label = tk.Label(frame, text="Должность")
    faculty_label = tk.Label(frame, text="Факультет")

    id_label.grid(row=0, column=0, sticky="W")
    id_entry.grid(row=0, column=1, sticky="E")

    surname_label.grid(row=1, column=0, sticky="W")
    surname_entry.grid(row=1, column=1, sticky="E")

    name_label.grid(row=2, column=0, sticky="W")
    name_entry.grid(row=2, column=1, sticky="E")

    patronymic_label.grid(row=3, column=0, sticky="W")
    patronymic_entry.grid(row=3, column=1, sticky="E")

    login_label.grid(row=4, column=0, sticky="W")
    login_entry.grid(row=4, column=1, sticky="E")

    password_label.grid(row=5, column=0, sticky="W")
    password_entry.grid(row=5, column=1, sticky="E")

    division_label.grid(row=6, column=0, sticky="W")
    division_entry.grid(row=6, column=1, sticky="E")

    post_label.grid(row=7, column=0, sticky="W")
    post_entry.grid(row=7, column=1, sticky="E")

    faculty_label.grid(row=8, column=0, sticky="W")
    faculty_combobox = ttk.Combobox(frame, textvariable=faculty_var, values=get_faculty_list())
    faculty_combobox.grid(row=8, column=1, sticky="E")

    selected = tree_var.selection()[0]
    values = tree_var.item(selected)["values"]

    id_entry.insert(0, values[0])
    surname_entry.insert(0, values[1])
    name_entry.insert(0, values[2])
    patronymic_entry.insert(0, values[3])
    login_entry.insert(0, values[4])
    password_entry.insert(0, values[5])
    division_entry.insert(0, values[6])
    post_entry.insert(0, values[7])
    faculty_combobox.set(values[8])
    print(values[8])

    def save_user_after():
        id = id_entry.get()
        surname = surname_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        login = login_entry.get()
        password = password_entry.get()
        division = division_entry.get()
        post = post_entry.get()
        faculty = faculty_combobox.get()

        update_user(surname, name, patronymic, login, password, division, post, faculty, id)

        login_entry.delete(0, tk.END)
        login_entry.insert(0, login)

        clear_fields(surname_entry, name_entry, patronymic_entry, login_entry,
                     password_entry, division_entry, post_entry, faculty_combobox)

    save_button = tk.Button(frame, text="Сохранить", command=save_user_after)
    save_button.grid(row=9, column=0, columnspan=2)


def update_user(surname, name, patronymic, login, password, division, post, faculty, id):
    # генерируем уникальный ID
    # подключение к БД
    global filename
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    # генерация ID


    # формирование запроса
    c.execute("""UPDATE user SET 
                   surname = ?,
                   name = ?, 
                   patronymic = ?,
                   login = ?,
                   password = ?,
                   division = ?,
                   post = ?,
                   faculty = ?
                WHERE id = ?""",
              (surname, name, patronymic, login, password, division, post, faculty, id))
    conn.commit()
    conn.close()
    clear_window()


def check_login_uniqueness(login):
    global filename
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE login=?", (login,))
    result = cursor.fetchone()
    conn.close()
    return result is None


# Функция для генерации уникального логина
def generate_unique_login(surname, name, middle_name=None):
    global filename
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    transliteration_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': '', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': '', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'h', 'щ': 'ch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'J', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
    }
    transliterated_surname = ''.join([transliteration_dict.get(char, char) for char in surname])
    transliterated_name = ''.join([transliteration_dict.get(char, char) for char in name])
    if middle_name:
        transliterated_middle_name = ''.join([transliteration_dict.get(char, char) for char in middle_name])
    else:
        transliterated_middle_name = None
    login = transliterated_surname + transliterated_name[0]
    if transliterated_middle_name:
        login += transliterated_middle_name[0]
    i = 1
    while not check_login_uniqueness(login):
        login = transliterated_surname + transliterated_name[0] + str(i)
        if transliterated_middle_name:
            login = transliterated_surname + transliterated_name[0] + transliterated_middle_name[0]+ str(i)
        i += 1
    conn.close()
    return login




def generationPassword():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(8))
    return password

def get_faculty_list():
    global filename
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute('SELECT facultie_short FROM Faculties')
    faculty_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    return faculty_list


def show_Faculties():
    global filename
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("PRAGMA table_info(Resourcses);")
    columns = [row[1] for row in c.fetchall()]
    # создаем новое окно
    new_window = tk.Toplevel()
    tree = ttk.Treeview(new_window)
    tree.pack()
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
    c.execute("SELECT * FROM Resourcses")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)
    # Автомасштабирование ширины столбцов
    column_widths = {}
    for row in rows:
        for i, cell in enumerate(row):
            column = columns[i]
            length = len(str(cell))
            if column not in column_widths or length > column_widths[column]:
                column_widths[column] = length
    #получить длину заголовка и если длина заголовка больше длины всех значений в столбце сделать ширину по заголовку столбца
    for column, width in column_widths.items():
        tree.column(column, width=width + 110)
    conn.close()

# Функция для выбора файла базы данных
def select_db():
    global filename
    filename = filedialog.askopenfilename(
        initialdir="/database",
        title="Select Database File",
        filetypes=(("DB files", "*.db"), ("all files", "*.*"))
    )
    load_data(filename)


# Функция для удаления выбранных пользователей
def delete_user():
    global tree_var
    global filename
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    # Получаем список выделенных строк
    selected_rows = tree_var.selection()

    # Проверяем, есть ли выделенные строки
    if not selected_rows:
        print("No selected rows")
        return

    # Получаем список ID выделенных пользователей
    selected_ids = []
    for row in selected_rows:
        values = tree_var.item(row)['values']
        selected_ids.append(values[0])

    # Формируем SQL запрос для удаления выделенных пользователей
    sql_query = "DELETE FROM user WHERE id IN (" + ",".join(str(id) for id in selected_ids) + ")"

    # Выполняем SQL запрос
    c.execute(sql_query)

    # Сохраняем изменения в базе данных
    conn.commit()

    # Обновляем дерево представлений с обновленными данными
    refresh_treeview()

    # Закрываем соединение с базой данных
    conn.close()
    clear_window()


# Функция для загрузки данных из выбранного файла базы данных
def load_data(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("PRAGMA table_info(user);")
    columns = [row[1] for row in c.fetchall()]
    tree = ttk.Treeview(root)
    tree.place(x=0, y=0, width=1280, height=640)
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
    c.execute("SELECT * FROM user")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)

    # названия столбцов
    tree.heading("id", text="ID пользователя")
    tree.heading("surname", text="Фамилия")
    tree.heading("name", text="Имя")
    tree.heading("patronymic", text="Отчество")
    tree.heading("login", text="Логин")
    tree.heading("password", text="Пароль")
    tree.heading("division", text="Подразделение")
    tree.heading("post", text="Должность")
    tree.heading("faculty", text="Факультет")

    # Добавление колесика прокрутки
    vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    vsb.place(x=1280-18, y=0, height=640)
    tree.configure(yscrollcommand=vsb.set)

    # Автомасштабирование ширины столбцов
    column_widths = {}
    for row in rows:
        for i, cell in enumerate(row):
            column = columns[i]
            length = len(str(cell))
            if column not in column_widths or length > column_widths[column]:
                column_widths[column] = length
    for column, width in column_widths.items():
        tree.column(column, width=width * 3 + 90)

    # Добавление переменной tree в функцию
    global tree_var
    tree_var = tree
    conn.close()



def select_max_id():
    global filename
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    cursor.execute("""SELECT MAX(id) FROM user""")
    max_id = cursor.fetchone()[0]
    print(max_id)
    conn.close()

    if not max_id:
        return 0
    return max_id
# Функция для создания формы добавления нового пользователя

def add_user_form():
    add_window = tk.Toplevel(root)
    add_window.title('Добавить пользователя')

    frame = tk.Frame(add_window)
    frame.pack(padx=10, pady=10)

    surname_label = tk.Label(frame, text='Фамилия')
    surname_entry = tk.Entry(frame)
    surname_label.grid(row=0, column=0)
    surname_entry.grid(row=0, column=1)

    name_label = tk.Label(frame, text='Имя')
    name_entry = tk.Entry(frame)
    name_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)

    patronymic_label = tk.Label(frame, text='Отчество')
    patronymic_entry = tk.Entry(frame)
    patronymic_label.grid(row=2, column=0)
    patronymic_entry.grid(row=2, column=1)

    login_label = tk.Label(frame, text='Логин')
    login_entry = tk.Entry(frame)
    login_label.grid(row=3, column=0)
    login_entry.grid(row=3, column=1)

    password_label = tk.Label(frame, text='Пароль')
    password_entry = tk.Entry(frame)
    password_label.grid(row=4, column=0)
    password_entry.grid(row=4, column=1)

    division_label = tk.Label(frame, text='Подразделение')
    division_entry = tk.Entry(frame)
    division_label.grid(row=5, column=0)
    division_entry.grid(row=5, column=1)

    post_label = tk.Label(frame, text='Должность')
    post_entry = tk.Entry(frame)
    post_label.grid(row=6, column=0)
    post_entry.grid(row=6, column=1)

    faculty_label = tk.Label(frame, text='Факультет')
    faculty_combobox = ttk.Combobox(frame, values=get_faculty_list())
    faculty_combobox.grid(row=7, column=1)
    faculty_label.grid(row=7, column=0)
    faculty_combobox.grid(row=7, column=1)

    # Генерация и вставка пароля
    password_entry.delete(0, tk.END)
    password_entry.insert(0, generationPassword())

    def generate_login():
        surname = surname_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        login = generate_unique_login(surname, name, patronymic)
        login_entry.delete(0, tk.END)
        login_entry.insert(0, login)

    generate_login_btn = tk.Button(frame, text='Сгенерировать логин', command=generate_login)
    generate_login_btn.grid(row=8, column=0)


    def save_user_and_generate_login():
        surname = surname_entry.get()
        name = name_entry.get()
        patronymic = patronymic_entry.get()
        login = login_entry.get()
        password = password_entry.get()
        division = division_entry.get()
        post = post_entry.get()
        faculty = faculty_combobox.get()
        save_user(surname, name, patronymic, login, password, division, post, faculty)
        login_entry.delete(0, tk.END)
        login_entry.insert(0, login)
        clear_fields(surname_entry, name_entry, patronymic_entry, login_entry, password_entry, division_entry,
                     post_entry, faculty_combobox)
        clear_window()


    save_btn = tk.Button(frame, text='Сохранить', command=save_user_and_generate_login)
    save_btn.grid(row=8, column=1)



def clear_fields(*fields):
    for field in fields:
        field.delete(0, tk.END)


def save_user(surname, name, patronymic, login, password, division, post, faculty):
    # генерируем уникальный ID
    # подключение к БД
    global filename
    conn = sqlite3.connect(filename)
    c = conn.cursor()

    # генерация ID
    max_id = select_max_id()
    id = max_id + 1
    print(max_id)
    # формирование запроса
    c.execute("""INSERT INTO user VALUES 
                     (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
              (id, surname, name, patronymic, login, password,
               division, post, faculty))

    conn.commit()
    conn.close()
    refresh_treeview


def show_Resourcses():
    global filename
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("PRAGMA table_info(Faculties);")
    columns = [row[1] for row in c.fetchall()]
    # создаем новое окно
    new_window = tk.Toplevel()
    tree = ttk.Treeview(new_window)
    tree.pack()
    tree["columns"] = columns
    for column in columns:
        tree.heading(column, text=column)
    c.execute("SELECT * FROM Faculties")
    rows = c.fetchall()
    for row in rows:
        tree.insert('', 'end', values=row)
    # Автомасштабирование ширины столбцов
    column_widths = {}
    for row in rows:
        for i, cell in enumerate(row):
            column = columns[i]
            length = len(str(cell))
            if column not in column_widths or length > column_widths[column]:
                column_widths[column] = length
    for column, width in column_widths.items():
        tree.column(column, width=width + 100)
    conn.close()

# Функция для обновления дерева представлений
def refresh_treeview():
    tree = ttk.Treeview(root)
    # Получаем данные из базы данных
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("SELECT * FROM user")
    rows = c.fetchall()

    # Удаляем все строки из дерева представлений
    tree.delete(*tree.get_children())

    # Заполняем дерево представления данными из базы данных
    for row in rows:
        tree.insert('', 'end', values=row)


# Создаем главное окно программы
root = tk.Tk()
root.geometry("1280x720")

# Добавляем меню в главное окно
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Добавляем пункт "Файл" в меню
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Выбрать базу данных", command=select_db)
file_menu.add_command(label="Обновить таблицу", command=clear_window)

# Добавляем пункт "Редактирование" в меню
edit_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Редактирование", menu=edit_menu)
edit_menu.add_command(label="Удалить", command=delete_user)
edit_menu.add_command(label="Добавить", command=add_user_form)
edit_menu.add_command(label="Редактировать", command=edit_user)

info_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Справочники", menu=info_menu)
info_menu.add_command(label="Факультеты", command=show_Faculties)
info_menu.add_command(label="Ресуры", command=show_Resourcses)

# Запускаем главный цикл программы
root.mainloop()
