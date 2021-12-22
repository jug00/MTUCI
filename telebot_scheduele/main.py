import telebot
from telebot import types
from psy import rasp_day, rasp_week, week

bot = telebot.TeleBot('2124745204:AAGc8lQtrkK0G3Ls_BorE1yh35Qj0kplKkA')


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(True)
    keyboard.row('Понедельник', 'Вторник', 'Среда',
                 'Четверг', 'Пятница')
    keyboard.row('Текущая неделя',
                 'Следующая неделя')
    bot.send_message(message.chat.id, 'Здравствуйте! На когда Вас интересует расписание?',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я могу:\n'
                                      '1. /week - узнать верхняя или нижняя сейчас неделя \n'
                                      '2. /mtuci - ссылка на сайт университета \n'
                                      '3. /help - список команд')


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/ - сайт нашего университета')


@bot.message_handler(commands=['week'])
def start_message(message):
    if week() == 'up':
        bot.send_message(message.chat.id, 'Сейчас идет верхняя неделя')
    else:
        bot.send_message(message.chat.id, 'Сейчас идет нижняя неделя')


@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница']:
        res = rasp_day(str(message.text))
        bot.send_message(message.chat.id, '%s' % res)
    elif message.text.lower() == 'текущая неделя':
        ans = rasp_week('current')
        bot.send_message(message.chat.id, '%s' % ans)
    elif message.text.lower() == 'следующая неделя':
        ans = rasp_week('next')
        bot.send_message(message.chat.id, '%s' % ans)
    else:
        bot.send_message(message.chat.id, 'Извините, я Вас не понял >> /help')




bot.infinity_polling()

