import Base
from aiogram import types

rangs = ["Нет ранга", "Silver I",  "Silver II", "Silver III", "Silver IV", "Silver Elite", "Silver Elite Master", "Gold Nova I", "Gold Nova II", "Gold Nova III", "Gold Nova IV", "Gold Nova Master", "Master Guardian I", "Master Guardian II", "Master Guardian Elite", "Distinguished Master Guardian", "Legendary Eagle", "Legendary Eagle Master", "Supreme Master First Class", "The Global Elite"]

# Функция находит все подходящие анкеты таблицы или сообщает об их отсутствии
def give_ankets(i):
    all_id = Base.get(0, "a")
    ch = True
    try:
        a = all_id[Base.get(i, "Индекс") + 1::]
    except IndexError:
        None
    else:
        for id in a:
            try:
                Base.get(id, "ранг")
                Base.get(id, "Обо_мне")
            except KeyError:
                None
            else:
                if (rangs.index(Base.get(id, "ранг")) >= rangs.index(Base.get(i, "ранг")) - 2 and rangs.index(Base.get(id, "ранг")) <= rangs.index(Base.get(i, "ранг")) + 2) and i != id and Base.get(id, "Статус_поиска"):
                    answer = "Ранг  - " + Base.get(id, "ранг") + "\n Обо мне: " + Base.get(id, "Обо_мне") + "\n Лайки: " + str(Base.get(id, "Лайки")) + "\n Дизлайки: " + str(Base.get(id, "Дизлайки"))
                    ch = False
                    Base.last_index(i, all_id.index(id))
                    break
    if ch:
        Base.last_index(i, len(all_id) - 1)
        answer = "Извините, но подходящих анкет нет. Как только появится подходящая, анкета мы вам напишем автоматически."
    return answer

# Выдача всей основной информации о человеке (для модераторов)
def take_all_data(id):
    answer = "ID - " + str(Base.get(id, "id")) + ", имя в тг - " + str(Base.get(id, "Имя_в_тг")) + ", дискорд - " + Base.get(id, "Дискорд") + ", ранг - " + Base.get(id, "ранг") + ", о нём - " + Base.get(id, "Обо_мне") + ", лайки - " + str(Base.get(id, "Лайки")) + ", дизлайки - " + str(Base.get(id, "Дизлайки"))
    return answer

# Механизм для многостраничной выдачи кнопок Рангов
def take_rang(id):
    global rangs
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 3)
    page = Base.get(id, "Страница_рангов")
    if page == 0:
        but1 = types.KeyboardButton(rangs[0])
        but2 = types.KeyboardButton(rangs[1])
        but3 = types.KeyboardButton(rangs[2])
        but4 = types.KeyboardButton(rangs[3])
        but5 = types.KeyboardButton(rangs[4])
        but6 = types.KeyboardButton("Дальше")
        markup.add(but1, but2, but3, but4, but5, but6)
    elif page >= 5 and page < 17:
        but1 = types.KeyboardButton("Назад")
        but2 = types.KeyboardButton(rangs[page])
        but3 = types.KeyboardButton(rangs[page+1])
        but4 = types.KeyboardButton(rangs[page+2])
        but5 = types.KeyboardButton(rangs[page+3])
        but6 = types.KeyboardButton("Дальше")
        markup.add(but1, but2, but3, but4, but5, but6)
    elif page == 17:
        but1 = types.KeyboardButton("Назад")
        but2 = types.KeyboardButton(rangs[page])
        but3 = types.KeyboardButton(rangs[page+1])
        but4 = types.KeyboardButton(rangs[page+2])
        markup.add(but1, but2, but3, but4) 
    return markup

# Проверка правельности введённого ДС (по стандартам до обновления)
def dc_cheker(id, dc):
    if len(list(dc)) >=5 and len(list(dc)) <=30 and not("'" in list(dc)) and not('"' in list(dc)):
        try:    
            lt = list(dc)[len(list(dc)) - 5::]
        except IndexError:
            return False
        else:
            num = ""
            for i in range(1, 4):
                num += lt[i]
            if num.isnumeric() and lt[0] == "#":
                Base.append_discord(id, dc)
                Base.add_position(id, "О себе")
                return True
            else:
                return False
    else:
        return False

# Проверка допустимости данных "О себе"
def abount_cheker(id, about):
    if len(list(about)) <= 250 and not("'" in list(about)) and not('"' in list(about)):
        Base.append_about_me(id, about)
        Base.add_position(id, "Норм анкета?")
        return True
    else:
        return False

# Возвращает админов и модеров из админки обратно в пользовательскую часть бота 
def return_out_admin(id):
    position = Base.get(id, "положение")
    if position == "выбор ранга" or position == "Изменение ранга":
        Base.add_page(id, 0)
        return "Введи свой ранг (просто нажми на кнопку)", take_rang(id)
    
    elif position == "Забитие дискорда" or position == "Изменение дискорда":
        return "Напишите ваш дискорд", types.ReplyKeyboardRemove()
    
    elif position == "О себе":
        return "Напишите немного о себе (k/d, возвраст, предпочтения в картах и пр.). Не более 250-ти символов", types.ReplyKeyboardRemove()
    
    elif position == "Норм анкета?":
        markup = types.ReplyKeyboardMarkup()
        but1 = types.KeyboardButton("Да")
        but2 = types.KeyboardButton("Нет")
        markup.add(but1, but2)
        return "Ваша анкета:\n" + "Ранг  - " + Base.get(id, "ранг") + "\n Обо мне: " + Base.get(id, "Обо_мне") + "\n Мой дискорд - " + Base.get(id, "Дискорд"), markup 
    
    elif position in ["Изменить анкету", "Начать поиск анкет"]:
        markup = types.ReplyKeyboardMarkup()
        but4 = types.KeyboardButton("Остановить поиск анкет")
        but1 = types.KeyboardButton("Начать поиск анкет")
        but2 = types.KeyboardButton("Изменить анкету")
        markup.add(but1, but2, but4)
        Base.add_position(id, "Начать поиск анкет")
        return "Когда захотите начать поиск анкет - нажмите кнопку", markup
    
    elif position == "Кунить жб":
        return "Пожалуйста, напишите текст жалобы", types.ReplyKeyboardRemove()
    
    elif position == "Кинуть ли жб":
        markup = types.ReplyKeyboardMarkup()
        but1 = types.KeyboardButton("Да")
        but2 = types.KeyboardButton("Нет")
        markup.add(but1, but2)
        return "Спасибо, данные внесены. Xотите отправить жалобу?", markup
    
    elif position == "Оценка":
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        but1 = types.KeyboardButton("👍")
        but2 = types.KeyboardButton("👎")
        markup.add(but1, but2)
        return "Как вы оцените?", markup
    
