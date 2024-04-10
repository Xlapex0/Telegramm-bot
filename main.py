import telebot
import sqlite3
import text 
from telebot import types

# подключение к боту в ТГ
BOT = telebot.TeleBot(f'{text.BOT_TOKEN}')

# кнопки
@BOT.message_handler(commands = ['start'])
def start(message):
    # кнопки интерфейса
    Markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton(f'{text.question_new}')
    btn2 = types.KeyboardButton(f'{text.question_active}')
    btn3 = types.KeyboardButton(f'{text.question_all}')
    btn4 = types.KeyboardButton(f'{text.author_card}')
    Markup.row(btn1)
    Markup.row(btn2,btn3)
    Markup.row(btn4)

    # обработка данных пользователя для регистрации
    first_name = ''
    last_name = ''
    if(message.from_user.first_name):
        first_name = message.from_user.first_name
    if(message.from_user.last_name):
        last_name = message.from_user.last_name
    name = first_name + ' ' + last_name

    # подключение к бд
    conn = sqlite3.connect(f'{text.DB_NAME}')
    cur = conn.cursor()

    # создание таблицы Пользователей
    cur.execute(f'{text.Users_table}')
    conn.commit()
    # создание таблицы Тегов
    cur.execute(f'{text.Tags_table}')
    conn.commit()
    # создание таблицы Вопросов
    cur.execute(f'{text.Questions_table}')
    conn.commit()
    # создание таблицы Ответов
    cur.execute(f'{text.Answers_table}')
    conn.commit()

    # внесение нового пользователя
    cur.execute("INSERT INTO Users(user_id, name) VALUES ('%s','%s')" % (message.from_user.username,name))
    conn.commit()

    # закрытие подключения к бд
    cur.close()
    conn.close()
    
    BOT.send_message(message.chat.id, 'Регистрация в системе завершена!')
    BOT.send_message(message.chat.id, f'Здравствуйте, {first_name}', reply_markup=Markup)

# обработка сообщений
@BOT.message_handler()
def info(message):
    match message.text.lower():
        case 'привет':
            # кнопки интерфейса
            Markup = types.ReplyKeyboardMarkup()
            btn1 = types.KeyboardButton(f'{text.question_new}')
            btn2 = types.KeyboardButton(f'{text.question_active}')
            btn3 = types.KeyboardButton(f'{text.question_all}')
            btn4 = types.KeyboardButton(f'{text.author_card}')
            Markup.row(btn1)
            Markup.row(btn2,btn3)
            Markup.row(btn4)

            BOT.send_message(message.chat.id,f'{text.question_new.lower()}')
            BOT.send_message(message.chat.id,f'Здравствуйте, {message.from_user.first_name}', reply_markup=Markup)
        case 'запрос на знание':
            BOT.send_message(message.chat.id,'Внесите запрос')
        case 'активные запросы':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.answer_add}',callback_data='answer')
            sbtn2 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='ansvers')
            Markup.row(sbtn1,sbtn2)

            BOT.send_message(message.chat.id,'<b>Список активных запросов:</b>',parse_mode='html')
            BOT.send_message(message.chat.id,'активный запрос 1', reply_markup=Markup)
            BOT.send_message(message.chat.id,'активный запрос 2', reply_markup=Markup)
            BOT.send_message(message.chat.id,'...')
        case 'все запросы':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.answer_add}',callback_data='answer')
            sbtn2 = types.InlineKeyboardButton(f'{text.answers_list}',callback_data='ansvers')
            Markup.row(sbtn1,sbtn2)

            BOT.send_message(message.chat.id,'<b>Полный список запросов:</b>',parse_mode='html')
            BOT.send_message(message.chat.id,'активный запрос 1', reply_markup=Markup)
            BOT.send_message(message.chat.id,'активный запрос 2', reply_markup=Markup)
            BOT.send_message(message.chat.id,'неактивный запрос 3')
            BOT.send_message(message.chat.id,'неактивный запрос 4')
            BOT.send_message(message.chat.id,'активный запрос 5', reply_markup=Markup)
            BOT.send_message(message.chat.id,'...')
        case 'карточка автора':
            # кнопки сообщения
            Markup = types.InlineKeyboardMarkup()
            sbtn1 = types.InlineKeyboardButton(f'{text.contact_add}',callback_data='answer')
            sbtn2 = types.InlineKeyboardButton(f'{text.contact_del}',callback_data='answer')
            Markup.row(sbtn1,sbtn2)

            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # получение данных пользователя
            cur.execute("SELECT * FROM Users WHERE user = '%s'" %  (message.from_user.first_name))
            user_data = cur.fetchall()[0]

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,'<b>Изменение данных автора:</b>',parse_mode='html')
            BOT.send_message(message.chat.id,f'<b>Имя:</b> {user_data[1]}\n<b>Кол-во вопросов:</b> {user_data[3]}\n<b>Кол-во ответов:</b> {user_data[4]}',parse_mode='html', reply_markup=Markup)
            
        #временная комманда для тестирования
        case 'тест бд':
            # подключение к бд
            conn = sqlite3.connect(f'{text.DB_NAME}')
            cur = conn.cursor()

            # комманда для теста
            cur.execute("INSERT INTO Questions(user_id,tag_id,data) VALUES (1,1,'Test1')")
            conn.commit()

            # закрытие подключения к бд
            cur.close()
            conn.close()

            BOT.send_message(message.chat.id,'Выполнено')
        case _:
            BOT.send_message(message.chat.id,'Комманда не распознана')
    

# обработка кнопок сообщения
@BOT.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    match callback.data:
        case 'answer':
            BOT.send_message(callback.message.chat.id,'Типа написал ответ')
        case 'ansvers':
            BOT.send_message(callback.message.chat.id,'Список ответов:')
            BOT.send_message(callback.message.chat.id,'Типа ответы')
            BOT.send_message(callback.message.chat.id,'Типа ответы')

# бесконечный перезапуск скрипта
BOT.polling(non_stop=True)