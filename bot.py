# -*- coding: utf-8 -*-

import telebot
import config
import dbworker
from models import *

bot = telebot.TeleBot(config.token)

Base.metadata.create_all(engine)
session = Session()

# Начало диалога
@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(message.chat.id, "Привіт! Як я можу до тебе звертатися?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)
# По команде /reset будем сбрасывать состояния, возвращаясь к началу диалога
@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Що ж, почнемо заново. Як тебе звати?")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_NAME.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_NAME.value)
def user_entering_name(message):
    # В случае с именем не будем ничего проверять, пусть хоть "25671", хоть Евкакий
    # save Info(name=message.text, chat_id=message.chat.id
    bot.send_message(message.chat.id, "Відмінне ім'я, запам'ятаю! " +message.text+", тепер вкажи, будь ласка, свій вік.")
    dbworker.set_state(message.chat.id, config.States.S_ENTER_AGE.value)
    info = Info()
    info.name = message.text
    info.chat_id = message.chat.id
    session.add(info)
    session.commit()


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_AGE.value)
def user_entering_age(message):
    # А вот тут сделаем проверку
    if not message.text.isdigit():
        # Состояние не меняем, поэтому только выводим сообщение об ошибке и ждём дальше
        bot.send_message(message.chat.id, "Щось не так, спробуй ще раз!")
        return
    # На данном этапе мы уверены, что message.text можно преобразовать в число, поэтому ничем не рискуем
    if int(message.text) < 5 or int(message.text) > 100:
        bot.send_message(message.chat.id, "Якийсь дивний вік. Не вірю! Відповідай чесно.")
        return
    else:
        # Возраст введён корректно, можно идти дальше
        bot.send_message(message.chat.id, "Колись і мені було стільки років ...Втім, не будемо відволікатися."
                                          "Напиши свій номер телефону в форматі + 380ХХХХХХХХХ.")
        dbworker.set_state(message.chat.id, config.States.S_SEND_PHONE.value)
        info = session.query(Info).filter_by(chat_id=message.chat.id).first()
        info.age = message.text
        session.add(info)
        session.commit()

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_PHONE.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Відмінно! Напиши свою пошту.") 
    dbworker.set_state(message.chat.id, config.States.S_SEND_MAIL.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.phone = message.text
    session.add(info)
    session.commit()

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_SEND_MAIL.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Яка посада тебе цікавить?   "
                                       "Якщо кілька запиши через кому") 
    dbworker.set_state(message.chat.id, config.States.S_ENTER_JOB.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.mail = message.text
    session.add(info)
    session.commit()    


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ENTER_JOB.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Подобається тобі працювати в команді?") 
    dbworker.set_state(message.chat.id, config.States.S_LIKE.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.job = message.text
    session.add(info)
    session.commit()         

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_LIKE.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Наскільки ти комунікабельна людина? (Від 1 до 10)") 
    dbworker.set_state(message.chat.id, config.States.S_KOMUN.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.like = message.text
    session.add(info)
    session.commit()  

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_KOMUN.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Чи є у тебе хоббі? Яке саме?") 
    dbworker.set_state(message.chat.id, config.States.S_HOBBY.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.komun = message.text
    session.add(info)
    session.commit()  


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_HOBBY.value)
def user_sending_photo(message):

    bot.send_message(message.chat.id, "вау, круто! Хотів би і я мати хоббі. В якому районі краще працювати в Києві?") 
    dbworker.set_state(message.chat.id, config.States.S_DISTRICT.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.hobby = message.text
    session.add(info)
    session.commit()  

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_DISTRICT.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Який графік роботи тебе цікавить? Вкажи від якої години, та до якої.") 
    dbworker.set_state(message.chat.id, config.States.S_GRAF.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.district = message.text
    session.add(info)
    session.commit()     

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GRAF.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Маєш вищу освіту? Якщо так то яку, якщо немає так і напиши.") 
    dbworker.set_state(message.chat.id, config.States.S_EDUCATION.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.graf = message.text
    session.add(info)
    session.commit()  

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_EDUCATION.value)
def user_sending_photo(message):
    bot.send_message(message.chat.id, "Дякую тобі за співбесіду. У найближчий час тобі зателефонують. Гарного настрою.") 
    dbworker.set_state(message.chat.id, config.States.S_START.value)
    info = session.query(Info).filter_by(chat_id=message.chat.id).first()
    info.education = message.text
    session.add(info)
    session.commit()  

bot.polling()
