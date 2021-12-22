import datetime
import time
from random import randint
import telebot, os
from telebot import types
from qr_func import qr_create, random_pass

bot = telebot.TeleBot('2112749065:AAHCSjfavt_IQq17GwhQ17Agd-PfiocmSII')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('Новости МТУСИ', 'Список команд')
    bot.send_message(message.chat.id, 'Привет! Что желаешь?',
                     reply_markup=keyboard)


@bot.message_handler(commands=['qr'])
def qr_ans(message):
    sent = bot.send_message(message.chat.id, 'Отправь данные для qr-кода')
    bot.register_next_step_handler(sent, qr_data)

def qr_data(message):
    data = str(message.text)
    name_qr = str(message.from_user.id)
    name_qr = name_qr + '_' + str(datetime.datetime.now())
    name_qr = name_qr.replace(' ', '_')
    qr_create(data, name_qr)
    f = open('%s' % name_qr, 'rb')
    bot.send_photo(message.chat.id, f)
    f.close()
    os.remove("%s" % name_qr)
    time.sleep(2)


@bot.message_handler(commands=['shlepa'])
def shlepa_img(message):
    number = randint(1, 20)
    f = open('img_shlepa/%s.jpg' % str(number), 'rb')
    bot.send_photo(message.chat.id, f)
    f.close()
    time.sleep(2)


@bot.message_handler(commands=['password'])
def make_pass(message):
    data = random_pass()
    bot.send_message(message.chat.id, 'Твой пароль: %s' % data)

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я могу:\n'
                                      '1. /qr - сгенерировать QR-код с введеным текстом/ссылкой \n'
                                      '2. /shlepa - отправить рандомную пикчу со шлепой \n'
                                      '3. /password - сгенерировать сложный пароль длиной от 10 до 16 символов \n'
                                      '4. /help - список команд')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "новости мтуси":
        bot.send_message(message.chat.id, 'Тогда тебе сюда – https://mtuci.ru/')
    elif message.text.lower() == 'привет':
        answers = ['Ну привет!', 'Салют, как дела?', 'Давно не виделись!']
        ans = randint(0, 2)
        ans = answers[ans]
        bot.send_message(message.chat.id, '%s' % ans)
    elif message.text.lower() == 'список команд':
        bot.send_message(message.chat.id, 'Я могу:\n'
                                          '1. /qr - сгенерировать QR-код с введеным текстом/ссылкой \n'
                                          '2. /shlepa - отправить рандомную пикчу со шлепой \n'
                                          '3. /password - сгенерировать сложный пароль длиной от 10 до 16 символов \n'
                                          '4. /help - список команд')
    else:
        bot.send_message(message.chat.id, 'Не знаю, что ты хочешь, но напоминаю про команду /help')




bot.infinity_polling()

