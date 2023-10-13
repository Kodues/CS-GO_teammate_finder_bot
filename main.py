from aiogram import Bot, Dispatcher, types, executor
import asyncio
import Base
import Defs
from datetime import datetime, timedelta

# Список всех рангов CS:GO по порядку
rangs = ["Нет ранга", "Silver I",  "Silver II", "Silver III", "Silver IV", "Silver Elite", "Silver Elite Master", "Gold Nova I", "Gold Nova II", "Gold Nova III", "Gold Nova IV", "Gold Nova Master", "Master Guardian I", "Master Guardian II", "Master Guardian Elite", "Distinguished Master Guardian", "Legendary Eagle", "Legendary Eagle Master", "Supreme Master First Class", "The Global Elite"]

token = "куцекцук"

bot = Bot(token = token)
dp = Dispatcher(bot)

# Запуск бота, запись основных данных в таблицу, проверка, писал ли человек ранее /start
@dp.message_handler(commands=("start"))
async def welcum(message):
    if Base.append_id(message.chat.id, message.from_user.username):
        markup = Defs.take_rang(message.chat.id)
        await dp.bot.send_message(message.chat.id, "Привет, " + message.from_user.first_name + "! Это тг бот для поиска тиммейтов в CS:GO. Для начала введи свой ранг (просто нажми на кнопку)", reply_markup=markup)
    else:
        await dp.bot.send_message(message.chat.id, "Вы уже прописывали /start, если хотите узнать что делает этот бот - пропишите /help")

# Вход в админку для модераторов, с проверкой (является ли человек модером)
@dp.message_handler(commands=("moder"))
async def moder_welcum(message):
    print(message.text)
    if str(message.chat.id) in Base.get(0, "m"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Забанить по id")
        but2 = types.KeyboardButton("Разбанить по id")
        but3 = types.KeyboardButton("Вернуться к обычному боту")
        markup.add(but1, but2, but3)
        Base.add_modder_position(message.chat.id, "старт")
        await dp.bot.send_message(message.chat.id, "Привет, ты - модер нашего проекта. Что хочешь сделать?", reply_markup=markup)

# Вход в админку для админов, с проверкой (является ли человек модером)
@dp.message_handler(commands=("admin"))
async def moder_welcum(message):
    if message.chat.id in Base.get(0, "ad"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Забанить по id")
        but2 = types.KeyboardButton("Разбанить по id")
        but3 = types.KeyboardButton("Удалить модера по id")
        but4 = types.KeyboardButton("Добавить модера по id")
        but5 = types.KeyboardButton("Скинуть всем пользователям рекламу")
        but6 = types.KeyboardButton("Вернуться к обычному боту")
        markup.add(but1, but2, but3, but4, but5, but6)
        Base.add_admin_position(message.chat.id, "старт")
        await dp.bot.send_message(message.chat.id, "Привет, ты - модер нашего проекта. Что хочешь сделать?", reply_markup=markup)

# Функция для рассылки фото всем пользователям (только для админов)
@dp.message_handler(content_types = [types.ContentType.PHOTO])
async def give_anketa(message):
    if message.chat.id in Base.get(0, "ad"):
        for i in Base.get(0, "a"):
            await dp.bot.send_photo(i, message.photo)

@dp.message_handler(content_types = [types.ContentType.TEXT])
async def give_anketa(message):
    markup = None
    #проверка, сидит ли человек сейчас в модераторке
    if Base.get(message.chat.id, "Позиция_модера") == "старт":
        # Исходя из того, какую кнопку нажал модер в модерке, бот задаёт ему вопрос и ждёт данных
        if message.text == "Забанить по id":
            Base.add_modder_position(message.chat.id, "Банит")
            answer = "Введите id"
        elif message.text == "Разбанить по id":
            Base.add_modder_position(message.chat.id, "Анбанит")
            answer = "Введите id"
        elif message.text == "Вернуться к обычному боту":
            Base.add_modder_position(message.chat.id, None)
            answer, markup = Defs.return_out_admin(message.chat.id)
        else:
            answer = "Просто нажмите на кнопку"
    elif Base.get(message.chat.id, "Положение_админа") == "старт":
        # То же, что для модеров в предыдущем ответвлении
        if message.text == "Забанить по id":
            Base.add_admin_position(message.chat.id, "Банит")
            answer = "Введите id"
        elif message.text == "Разбанить по id":
            Base.add_admin_position(message.chat.id, "Анбанит")
            answer = "Введите id"
        elif message.text == "Удалить модера по id":
            Base.add_admin_position(message.chat.id, "Банит модера")
            answer =  "Введите id"
        elif message.text == "Добавить модера по id":
            Base.add_admin_position(message.chat.id, "Добавляет модера")
            answer =  "Введите id"
        elif message.text == "Скинуть всем пользователям рекламу":
            Base.add_admin_position(message.chat.id, "Рекламная рассылка")
            answer = "скиньте сначала картинку потом текст рекламы"
        elif  message.text == "a":
            answer = str(len(Base.get(12, "a")))
        elif message.text == "Вернуться к обычному боту":
            Base.add_admin_position(message.chat.id, None)
            answer, markup = Defs.return_out_admin(message.chat.id)
        else:
            answer = "Просто нажмите на кнопку"
    # Функция баннит человек по введённому ID (если это делает модер)
    elif Base.get(message.chat.id, "Позиция_модера") == "Банит" or Base.get(message.chat.id, "Положение_админа") == "Банит":
        if message.text.isnumeric() and int(message.text) in Base.get(0, "a"):
            Base.ban(int(message.text))
            answer = "Пользователь забанен"
        else:
            answer = "Пользователя с таким id нет"
        if Base.get(message.chat.id, "Позиция_модера") == "Банит":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but1 = types.KeyboardButton("Забанить по id")
            but2 = types.KeyboardButton("Разбанить по id")
            but3 = types.KeyboardButton("Вернуться к обычному боту")
            markup.add(but1, but2, but3)
            Base.add_modder_position(message.chat.id, "старт")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but1 = types.KeyboardButton("Забанить по id")
            but2 = types.KeyboardButton("Разбанить по id")
            but3 = types.KeyboardButton("Удалить модера по id")
            but4 = types.KeyboardButton("Добавить модера по id")
            but5 = types.KeyboardButton("Скинуть всем пользователям рекламу")
            but6 = types.KeyboardButton("Вернуться к обычному боту")
            markup.add(but1, but2, but3, but4, but5, but6)
            Base.add_admin_position(message.chat.id, "старт")
    # Функция разбанивает по ID
    elif Base.get(message.chat.id, "Позиция_модера") == "Анбанит" or Base.get(message.chat.id, "Положение_админа") == "Анбанит":
        if message.text.isnumeric() and int(message.text) in Base.get(0, "a"):
            Base.unban(int(message.text))
            answer = "Пользователь разбанен"
        else:
            answer = "Пользователя с таким id нет"
        if Base.get(message.chat.id, "Позиция_модера") == "Анбанит":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but1 = types.KeyboardButton("Забанить по id")
            but2 = types.KeyboardButton("Разбанить по id")
            but3 = types.KeyboardButton("Вернуться к обычному боту")
            markup.add(but1, but2, but3)
            Base.add_modder_position(message.chat.id, "старт")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            but1 = types.KeyboardButton("Забанить по id")
            but2 = types.KeyboardButton("Разбанить по id")
            but3 = types.KeyboardButton("Удалить модера по id")
            but4 = types.KeyboardButton("Добавить модера по id")
            but5 = types.KeyboardButton("Скинуть всем пользователям рекламу")
            but6 = types.KeyboardButton("Вернуться к обычному боту")
            markup.add(but1, but2, but3, but4, but5, but6)
            Base.add_admin_position(message.chat.id, "старт")
    # Функция для админа (удалить модератора)
    elif Base.get(message.chat.id, "Положение_админа") == "Банит модера":
        if message.text.isnumeric() and message.text in Base.get(0, "m"):
            Base.del_moder_id(int(message.text))
            Base.add_modder_position(int(message.text), None)
            answer = "Модер забанен"
        else:
            answer = "Пользователя с таким id нет"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Забанить по id")
        but2 = types.KeyboardButton("Разбанить по id")
        but3 = types.KeyboardButton("Удалить модера по id")
        but4 = types.KeyboardButton("Добавить модера по id")
        but5 = types.KeyboardButton("Скинуть всем пользователям рекламу")
        but6 = types.KeyboardButton("Вернуться к обычному боту")
        markup.add(but1, but2, but3, but4, but5, but6)
        Base.add_admin_position(message.chat.id, "старт")
    # Функция для админа (добавить модератора)
    elif Base.get(message.chat.id, "Положение_админа") == "Добавляет модера":
        if message.text.isnumeric() and not(int(message.text) in Base.get(0, "m")):
            Base.append_moder_id(int(message.text))
            answer = "Пользоваетль добавлен"
        else:
            answer = "Неверный id"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Забанить по id")
        but2 = types.KeyboardButton("Разбанить по id")
        but3 = types.KeyboardButton("Удалить модера по id")
        but4 = types.KeyboardButton("Добавить модера по id")
        but5 = types.KeyboardButton("Скинуть всем пользователям рекламу")
        but6 = types.KeyboardButton("Вернуться к обычному боту")
        markup.add(but1, but2, but3, but4, but5, but6)
        Base.add_admin_position(message.chat.id, "старт")
    # Функция для админа (разослать всем пользователям текст)
    elif Base.get(message.chat.id, "Положение_админа") == "Рекламная рассылка":
        txt = message.text
        for i in Base.get(0, "a"):
            await dp.bot.send_message(i, txt)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but1 = types.KeyboardButton("Забанить по id")
        but2 = types.KeyboardButton("Разбанить по id")
        but3 = types.KeyboardButton("Удалить модера по id")
        but4 = types.KeyboardButton("Добавить модера по id")
        but5 = types.KeyboardButton("Скинуть всем пользователям рекламу")
        but6 = types.KeyboardButton("Вернуться к обычному боту")
        markup.add(but1, but2, but3, but4, but5, but6)
        Base.add_admin_position(message.chat.id, "старт")
        answer = "рассылка окончена"
    #Если пользователь не забанен и он существует, то
    elif message.chat.id in Base.get(0, "a") and Base.get(message.chat.id, "Бан"):
        if Base.get(message.chat.id, "положение") == "Начать поиск анкет":
            # Останавливает поиск анкет
            if message.text == "Остановить поиск анкет":
                Base.change_status_searching(message.chat.id, False)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                but = types.KeyboardButton("Продолжить поиск")
                markup.add(but)
                answer = "Поиск анкет остановлен"
            elif Base.get(message.chat.id, "Статус_поиска") and message.text in ["Да", "Нет", "Начать поиск анкет"]:
                    if message.text == "Да":
                        if str(message.chat.id) in Base.get(Base.get(0, "a")[Base.get(message.chat.id, "Индекс")], "Совпадение") and str(message.chat.id) != Base.get(message.chat.id, "Индекс"):
                            await dp.bot.send_message(Base.get(0, "a")[Base.get(message.chat.id, "Индекс")], "У ВАС СОВПАДЕНИЕ. Вот дискорд " + Base.get(message.chat.id, "Дискорд"))
                            await dp.bot.send_message(message.chat.id, "У ВАС СОВПАДЕНИЕ. Вот дискорд " + Base.get(Base.get(0, "a")[Base.get(message.chat.id, "Индекс")], "Дискорд"))
                            date = (datetime.strptime(str((datetime.today()).date()), '%Y-%m-%d') + timedelta(days=2)).strftime('%Y-%m-%d')
                            Base.like_date(Base.get(0, "a")[Base.get(message.chat.id, "Индекс")], message.chat.id, date)
                            Base.like_date(message.chat.id, Base.get(0, "a")[Base.get(message.chat.id, "Индекс")], date)
                            Base.del_coincidence(Base.get(0, "a")[Base.get(message.chat.id, "Индекс")], message.chat.id)
                        else:
                            Base.append_coincidence(message.chat.id, Base.get(0, "a")[Base.get(message.chat.id, "Индекс")])
                    elif message.text == "Нет" and str(message.chat.id) in Base.get(Base.get(0, "a")[Base.get("Индекс")], "Совпадение"):
                        Base.del_coincidence(Base.get(0, "a")[Base.get("Индекс")], message.chat.id)
                    answer = Defs.give_ankets(message.chat.id)
                    if answer == "Извините, но подходящих анкет нет. Как только появится подходящая анкета мы вам напишем автоматически":
                        markup = types.ReplyKeyboardMarkup(row_width=2)
                        but1 = types.KeyboardButton("Изменить анкету")
                        but4 = types.KeyboardButton("Остановить поиск анкет")
                        markup.add(but1, but4)
                        Base.change_status_wayting(message.chat.id, True)
                    else:
                        markup = types.ReplyKeyboardMarkup(row_width=2)
                        but1 = types.KeyboardButton("Да")
                        but2 = types.KeyboardButton("Нет")
                        but3 = types.KeyboardButton("Изменить анкету")
                        but4 = types.KeyboardButton("Остановить поиск анкет")
                        markup.add(but1, but2, but3, but4)
            elif message.text =="Изменить анкету":
                Base.add_position(message.chat.id, "Изменение")
                markup = types.ReplyKeyboardMarkup(row_width=2)
                but1 = types.KeyboardButton("Ранг")
                but2 = types.KeyboardButton("Дискорд")
                but3 = types.KeyboardButton("О себе")
                but4 = types.KeyboardButton("Изенить всю анкету")
                markup.add(but1, but2, but3, but4)
                answer = "Что вы хотите изменить?"
            elif message.text == "Продолжить поиск" and not(Base.get(message.chat.id, "Статус_поиска")):
                Base.change_status_searching(message.chat.id, True)
                markup = types.ReplyKeyboardMarkup(row_width=2)
                but1 = types.KeyboardButton("Да")
                but2 = types.KeyboardButton("Нет")
                but3 = types.KeyboardButton("Изменить анкету")
                but4 = types.KeyboardButton("Остановить поиск анкет")
                markup.add(but1, but2, but3, but4)
                answer = Defs.give_ankets(message.chat.id)
            else:
                answer = "Просто нажмите на кнопку"
        
        elif Base.get(message.chat.id, "положение") == "Изменение":
            if message.text == "Ранг":
                Base.add_position(message.chat.id, "Изменение ранга")
                answer = "Введи свой ранг (просто нажми на кнопку)"
                Base.add_page(message.chat.id, 0)
                markup = Defs.take_rang(message.chat.id)
            elif message.text == "Дискорд":
                Base.add_position(message.chat.id, "Изменение дискорда")
                answer = "Напишите ваш дискорд"
                markup = types.ReplyKeyboardRemove()
            elif message.text == "О себе":
                Base.add_position(message.chat.id, "О себе")
                markup = types.ReplyKeyboardRemove()
                answer = "Напишите немного о себе (k/d, возвраст, предпочтения в картах и пр.). Не более 250-и символов"
            elif message.text == "Изенить всю анкету":
                Base.add_position(message.chat.id, "выбор ранга")
                answer = "Введи свой ранг (просто нажми на кнопку)"
                Base.add_page(message.chat.id, 0)
                markup = Defs.take_rang(message.chat.id)
            else:
                answer = "Просто нажмите на кнопку"
        
        elif Base.get(message.chat.id, "положение") == "Оценка":
            if message.text == "👍":
                Base.add_like(Base.get(message.chat.id, "Оцениваемый_id"))
                answer = "Спасибо, данные внесены"
                markup = types.ReplyKeyboardMarkup()
                but1 = types.KeyboardButton("Начать поиск анкет")
                but2 = types.KeyboardButton("Изменить анкету")
                but3 = types.KeyboardButton("Остановить поиск анкет")
                markup.add(but1, but2, but3)
                Base.add_position(message.chat.id, "Начать поиск анкет")
            elif message.text == "👎":
                Base.add_dislike(Base.get(message.chat.id, "Оцениваемый_id"))
                answer = "Спасибо, данные внесены. Xотите отправить жалобу?"
                Base.add_position(message.chat.id, "Кинуть ли жб")
                markup = types.ReplyKeyboardMarkup()
                but1 = types.KeyboardButton("Да")
                but2 = types.KeyboardButton("Нет")
                markup.add(but1, but2)
            else: 
                answer = "Просто нажмите на кнопку"

        elif Base.get(message.chat.id, "положение") == "Кинуть ли жб":
            if message.text == "Нет":
                answer = "Что вы хотите сделать?"
                markup = types.ReplyKeyboardMarkup()
                but1 = types.KeyboardButton("Начать поиск анкет")
                but2 = types.KeyboardButton("Изменить анкету")
                but3 = types.KeyboardButton("Остановить поиск анкет")
                markup.add(but1, but2, but3)
                Base.add_position(message.chat.id, "Начать поиск анкет")
            elif message.text == "Да":
                answer = "Пожалуйста, напишите текст жалобы"
                Base.add_position(message.chat.id, "Кунить жб")
                markup = types.ReplyKeyboardRemove()
            else:
                answer = "Просто нажмите на кнопку"

        elif Base.get(message.chat.id, "положение") == "Кунить жб":
            answer = "Данные кинувшего: " + Defs.take_all_data(message.chat.id) + ".\nДанные на которого кидают: " + Defs.take_all_data(Base.get(message.chat.id, "Оцениваемый_id")) + ".\nТекст жб: " + message.text
            await dp.bot.send_message(chat_id= "-686386885", text = answer)
            answer = "Спасибо, жалоба отправлена"
            markup = types.ReplyKeyboardMarkup()
            but1 = types.KeyboardButton("Начать поиск анкет")
            but2 = types.KeyboardButton("Изменить анкету")
            but3 = types.KeyboardButton("Остановить поиск анкет")
            markup.add(but1, but2, but3)
            Base.add_position(message.chat.id, "Начать поиск анкет")

        elif Base.get(message.chat.id, "положение") == "Изменение дискорда":
            if Defs.dc_cheker(message.chat.id, message.text):
                Base.append_discord(message.chat.id, message.text)
                Base.add_position(message.chat.id, "Норм анкета?")
                markup = types.ReplyKeyboardMarkup()
                but1 = types.KeyboardButton("Да")
                but2 = types.KeyboardButton("Нет")
                markup.add(but1, but2)
                answer = "Ваша анкета:\n" + "Ранг  - " + Base.get(message.chat.id, "ранг") + "\n Обо мне: " + Base.get(message.chat.id, "Обо_мне") + "\n Мой дискорд - " + Base.get(message.chat.id, "Дискорд")
            else:
                answer = "Введите ваш дискорд типа nick_name#XXXX (возможно вы ввели слишком длинный дискорд)"

        elif Base.get(message.chat.id, "положение") == "Изменение ранга":
            if message.text in rangs:
                Base.append_rang(message.chat.id, message.text)
                Base.add_position(message.chat.id, "Норм анкета?")
                markup = types.ReplyKeyboardMarkup()
                but1 = types.KeyboardButton("Да")
                but2 = types.KeyboardButton("Нет")
                markup.add(but1, but2)
                answer = "Ваша анкета:\n" + "Ранг  - " + Base.get(message.chat.id, "ранг") + "\n Обо мне: " + Base.get(message.chat.id, "Обо_мне") + "\n Мой дискорд - " + Base.get(message.chat.id, "Дискорд")
            elif message.text == "Дальше":
                page = Base.get(message.chat.id, "Страница_рангов")
                if page < 17:
                    if page == 0:
                        Base.add_page(message.chat.id, page + 5)
                    else:
                        Base.add_page(message.chat.id, page + 4)
                    answer = "Переключаюсь на следующую страницу"
                else:
                    answer = "Вы уже на последней странице"
                markup = Defs.take_rang(message.chat.id)
            elif message.text == "Назад":
                page = Base.get(message.chat.id, "Страница_рангов")
                if page > 0:
                    if page == 5:
                        Base.add_page(message.chat.id, page - 5)
                    else:
                        Base.add_page(message.chat.id, page - 4)
                    answer = "Переключаюсь на предыдущую страницу"
                else:
                    answer = "Вы уже на первой странице"
                markup = Defs.take_rang(message.chat.id)
            else:
                answer = "Просто нажмите на кнопку"

        elif Base.get(message.chat.id, "положение") == "выбор ранга":
            if message.text in rangs:
                markup = types.ReplyKeyboardRemove()
                answer = "Теперь напишите ваш дискорд"
                Base.append_rang(message.chat.id, message.text)
                Base.add_position(message.chat.id, "Забитие дискорда")
            elif message.text == "Дальше":
                page = Base.get(message.chat.id, "Страница_рангов")
                if page < 17:
                    if page == 0:
                        Base.add_page(message.chat.id, page + 5)
                    else:
                        Base.add_page(message.chat.id, page + 4)
                    answer = "Переключаюсь на следующую страницу"
                else:
                    answer = "Вы уже на последней странице"
                markup = Defs.take_rang(message.chat.id)
            elif message.text == "Назад":
                page = Base.get(message.chat.id, "Страница_рангов")
                if page > 0:
                    if page == 5:
                        Base.add_page(message.chat.id, page - 5)
                    else:
                        Base.add_page(message.chat.id, page - 4)
                    answer = "Переключаюсь на предыдущую страницу"
                else:
                    answer = "Вы уже на первой странице"
                markup = Defs.take_rang(message.chat.id)
            else:
                answer = "Просто нажмите на кнопку"
        
        elif Base.get(message.chat.id, "положение") == "Забитие дискорда":
            if Defs.dc_cheker(message.chat.id, message.text):
                answer = "Хорошо. Теперь напишите немного о себе (k/d, возвраст, предпочтения в картах и пр.). Не более 250-ти символов"
            else:
                answer = "Введите ваш дискорда тип nick_name#XXXX (возможно вы ввели слишком длинный дискорд)"
        
        elif Base.get(message.chat.id, "положение") == "О себе":
            if Defs.abount_cheker(message.chat.id, message.text):
                markup = types.ReplyKeyboardMarkup()
                but1 = types.KeyboardButton("Да")
                but2 = types.KeyboardButton("Нет")
                markup.add(but1, but2)
                answer = "Ваша анкета:\n" + "Ранг  - " + Base.get(message.chat.id, "ранг") + "\n Обо мне: " + Base.get(message.chat.id, "Обо_мне") + "\n Мой дискорд - " + Base.get(message.chat.id, "Дискорд")
            else:
                answer = "Пожалуйста, сократите объём текста до 250-и символов"

        elif Base.get(message.chat.id, "положение") == "Норм анкета?":
            if message.text == "Да":
                answer = "Когда захотите начать поиск анкет - нажмите кнопку"
                markup = types.ReplyKeyboardMarkup()
                but4 = types.KeyboardButton("Остановить поиск анкет")
                but1 = types.KeyboardButton("Начать поиск анкет")
                but2 = types.KeyboardButton("Изменить анкету")
                markup.add(but1, but2, but4)
                Base.add_position(message.chat.id, "Начать поиск анкет")
            elif message.text == "Нет":
                Base.add_position(message.chat.id, "Изменение")
                markup = types.ReplyKeyboardMarkup(row_width=2)
                but1 = types.KeyboardButton("Ранг")
                but2 = types.KeyboardButton("Дискорд")
                but3 = types.KeyboardButton("О себе")
                but4 = types.KeyboardButton("Изенить всю анкету")
                markup.add(but1, but2, but3, but4)
                answer = "Что вы хотите изменить"
    else:
        answer = "Вы были забанены. По всем вопросом к https://t.me/Dima_Schukin"
    if markup == None:
        await dp.bot.send_message(message.chat.id, text = answer)
    else:
        await dp.bot.send_message(message.chat.id, text = answer, reply_markup=markup)

# Проверяет, появились подходящие анкеты (действует раз в 23 часа)
async def for_searching():
    while True:
        all_id = Base.get(0, "a")
        for i in all_id:
            if Base.get(i, "Статус_ожидания"):
                answer = Defs.give_ankets(i)
                if answer != "Извините, но подходящих анкет нет. Как только появится подходящая анкета мы вам напишем автоматически":
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    but1 = types.KeyboardButton("Да")
                    but2 = types.KeyboardButton("Нет")
                    but3 = types.KeyboardButton("Изменить анкету")
                    but4 = types.KeyboardButton("Остановить поиск анкет")
                    markup.add(but1, but2, but3, but4)
                    Base.change_status_wayting(i, False)
                    await dp.bot.send_message(i, answer, reply_markup=markup)
        await asyncio.sleep(82800)

# Проверяет, нужно ли кого-нибудь спросить о том, как прошла его встреча с тимейтом (действует раз в 23 часа)
async def coincidence():
    while True:
        all_id = Base.get(0, "a")
        for i in all_id:
            if Base.get(i, "дата_оценки") != {}:
                for j in list((Base.get(i, "дата_оценки")).keys()):
                    if j == (datetime.strptime(str((datetime.today()).date()), '%Y-%m-%d')).strftime('%Y-%m-%d'):
                        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                        but1 = types.KeyboardButton("👍")
                        but2 = types.KeyboardButton("👎")
                        markup.add(but1, but2)
                        Base.add_position(i, "Оценка")
                        Base.add_position(Base.get(i, 'дата_оценки')[j], "Оценка")
                        Base.change_ocenshik(i, Base.get(i, 'дата_оценки')[j])
                        Base.change_ocenshik(Base.get(i, 'дата_оценки')[j], i)
                        await dp.bot.send_message(i, "Как вы оценити " + Base.get((Base.get(i, "дата_оценки"))[j], "Дискорд") + " ?", reply_markup = markup)
                        await dp.bot.send_message(Base.get(i, 'дата_оценки')[j], "Как вы оценити " + Base.get(i, "Дискорд") + " ?", reply_markup = markup)
                        d = Base.get(i, 'дата_оценки')[j]
                        Base.del_date(i, j)
                        Base.del_date(d, j)
                        break
        await asyncio.sleep(82800)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(for_searching())
    loop2 = asyncio.get_event_loop()
    loop2.create_task(coincidence())
    executor.start_polling(dp, on_startup=print("Запуск бота... \nБот запущен"))