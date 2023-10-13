import sqlite3
conn = sqlite3.connect("base.db")
c = conn.cursor()
# Создание таблицы
c.execute("CREATE TABLE IF NOT EXISTS users (id integer, положение text, Лайки integer, Дизлайки integer, Положение_админа text, Индекс integer, Совпадение text, дата_оценки text, Страница_рангов integer, Имя_в_тг text, Статус_поиска text, Статус_ожидания text, Позиция_модера text, Бан text, ранг text, Дискорд text, Обо_мне text, Оцениваемый_id text)")
c.execute("CREATE TABLE IF NOT EXISTS moders (id text)")

# Запись данных SQL таблицы в список
c.execute("SELECT id FROM users")
all_id = c.fetchall()
for i in all_id:
    all_id[all_id.index(i)] = i[0]

c.execute("SELECT id FROM moders")
moders = c.fetchall()
for i in moders:
    moders[moders.index(i)] = i[0]

# Здесь указывается ID Админов (в данном случае просто набор цифр)
admins = [1234567890]

# Создание строки по ID пользователя и введение туда нужных данных (ID, имя и т.д.)
def append_id(id, name):
    if id in all_id:
        return False
    else:
        a = "INSERT INTO users (id, положение, Лайки, Дизлайки, Положение_админа, Индекс, Совпадение, дата_оценки, Страница_рангов, Имя_в_тг, Статус_поиска, Статус_ожидания, Позиция_модера, Бан, ранг, Дискорд, Обо_мне, Оцениваемый_id) VALUES ('" + str(id) + "', 'выбор ранга', '0', '0', '', '-1', '', '', '0', '" + str(name) + "', 'True', 'False', '', 'True', '', '', '', '')"
        c.execute(a)
        conn.commit()
        all_id.append(id)
        return True

def append_rang(id, rang):
    c.execute("UPDATE users SET ранг = '" + rang + "' where id = '" + str(id) + "'")
    conn.commit()

def append_moder_id(id):
    c.execute("INSERT INTO moders (id) VALUES ('" + str(id) + "')")
    moders.append(id)
    conn.commit()

def del_moder_id(id):
    c.execute("DELETE FROM moders WHERE id = '" + str(id) + "'")
    moders.remove(str(id))
    conn.commit()

def append_discord(id, discord):
    c.execute("UPDATE users SET Дискорд = '" + discord + "' where id = '" + str(id) + "'")
    conn.commit()

def append_about_me(id, about_me):
    c.execute("UPDATE users SET Обо_мне = '" + about_me + "' where id = '" + str(id) + "'")
    conn.commit()

def change_status_wayting(id, status):
    c.execute("UPDATE users SET Статус_ожидания = '" + str(status) + "' where id = '" + str(id) + "'")
    conn.commit()

def change_status_searching(id, status):
    c.execute("UPDATE users SET Статус_поиска = '" + str(status) + "' where id = '" + str(id) + "'")
    conn.commit()

def change_ocenshik(id, id_2):
    c.execute("UPDATE users SET Оцениваемый_id = '" + str(id_2) + "' where id = '" + str(id) + "'")
    conn.commit()

def append_coincidence(id, add_id):
    c.execute("SELECT Совпадение FROM users where id = '" + str(id) + "'")
    a = c.fetchall()[0][0]
    if a == "":
        a = a + str(add_id)
    else:
        a = a + " " + str(add_id)
    c.execute("UPDATE users SET Совпадение = '" + str(a) + "' where id = '" + str(id) + "'")
    conn.commit()

def del_coincidence(id, del_id):
    c.execute("SELECT Совпадение FROM users where id = '" + str(id) + "'")
    a = list(c.fetchall()[0][0] + " ")
    b = ""
    l = []
    for i in a:
        if i != " ":
            b += i
        else:
            l.append(b)
            b = ""
    l.remove(str(del_id))
    if len(l) > 0:
        a = l[0]
        for i in l[1::]:
            a += " " + i
    else:
        a = ""
    c.execute("UPDATE users SET Совпадение = '" + str(a) + "' where id = '" + str(id) + "'")
    conn.commit()


def del_date(id, date):
    c.execute("SELECT дата_оценки FROM users where id = '" + str(id) + "'")
    a = list(c.fetchall()[0][0] + " ")
    b = ""
    l = []
    ch = False
    o = 0
    for i in a:
        if i != " ":
            b += i
        elif i == " ":
            l.append(b)
            b = ""
    ch = True
    f = []
    for i in l:
        for j in i:
            if j == ":":
                f.append(b)
                ch = False
                b = ""
            elif ch:
                b += j
            else:
                b += j
        f.append(b)
        b = ""
        l[l.index(i)] = f
        f = []
    for i in l:
        if date in i:
            l.remove(i)
    if len(l) > 0:
        a = l[0][0] + ":" + l[0][1]
        for i in l[1::]:
            a += " " + i[0] + ":" + i[1]
    else:
        a = ""
    c.execute("UPDATE users SET дата_оценки = '" + str(a) + "' where id = '" + str(id) + "'")
    conn.commit()

def like_date(id, coinc_id, date):
    c.execute("SELECT дата_оценки FROM users where id = '" + str(id) + "'")
    a = c.fetchall()[0][0]
    if a == "":
        a = str(date) + ":" + str(coinc_id)
    else:
        a += " " + str(date) + ":" + str(coinc_id)
    c.execute("UPDATE users SET дата_оценки = '" + str(a) + "' where id = '" + str(id) + "'")
    conn.commit()

def last_index(id, indx):
    c.execute("UPDATE users SET Индекс = '" + str(indx) + "' where id = '" + str(id) + "'")
    conn.commit()

def add_position(id, position):
    c.execute("UPDATE users SET положение = '" + str(position) + "' where id = '" + str(id) + "'")
    conn.commit()

def add_page(id, page):
    c.execute("UPDATE users SET Страница_рангов = '" + str(page) + "' where id = '" + str(id) + "'")
    conn.commit()

def add_like(id):
    c.execute("SELECT Лайки FROM users where id = '" + str(id) + "'")
    a = c.fetchall()[0][0] + 1
    c.execute("UPDATE users SET Лайки = '" + str(a) + "' where id = '" + str(id) + "'")
    conn.commit()

def add_dislike(id):
    c.execute("SELECT Дизлайки FROM users where id = '" + str(id) + "'")
    a = c.fetchall()[0][0] + 1
    c.execute("UPDATE users SET Дизлайки = '" + str(a) + "' where id = '" + str(id) + "'")
    conn.commit()

def add_modder_position(id, position):
    c.execute("UPDATE users SET Позиция_модера = '" + str(position) + "' where id = '" + str(id) + "'")
    conn.commit()

def ban(id):
    c.execute("UPDATE users SET Бан = 'False' where id = '" + str(id) + "'")
    conn.commit()

def unban(id):
    c.execute("UPDATE users SET Бан = 'True' where id = '" + str(id) + "'")
    conn.commit()

def add_admin_position(id, position):
    c.execute("UPDATE users SET Положение_админа = '" + str(position) + "' where id = '" + str(id) + "'")
    conn.commit()

# Функция для получения данных из таблиц
def get(id, key):
    if key == "a":
        return all_id
    elif key == "m":
        return moders
    elif key == "b":
        c.execute("SELECT * FROM users")
        return c.fetchall()
    elif key == "ad":
        return admins
    elif key in ["Бан", "Статус_ожидания", "Статус_поиска"]:
        c.execute("SELECT " + str(key) + " FROM users where id = '" + str(id) + "'")
        a = c.fetchall()[0][0]
        if a == "True":
            return True
        else:
            return False
    elif key == "Совпадение":
        c.execute("SELECT Совпадение FROM users where id = '" + str(id) + "'")
        l = ""
        try:
            dsgh = c.fetchall()[0][0]
        except IndexError:
            None
        else: 
            l = []
            if dsgh != "":
                a = list(dsgh + " ")
                b = ""
                for i in a:
                    if i != " ":
                        b += i
                    else:
                        l.append(b)
                        b = ""
        return l
    elif key == "дата_оценки":
        d = {}
        k = ""
        m = ""
        c.execute("SELECT дата_оценки FROM users where id = '" + str(id) + "'")
        try:
            a = list(c.fetchall()[0][0] + " ")
        except IndexError:
            None
        else:
            ch = True
            for i in a:
                if i == ":":
                    ch = False
                elif i == " ":
                    d[k] = m
                    k = ""
                    m = ""
                    ch = True
                elif ch:
                    k += i
                elif not(ch):
                    m += i
            return d
    else:
        c.execute("SELECT " + str(key) + " FROM users where id = '" + str(id) + "'")
        return c.fetchall()[0][0]