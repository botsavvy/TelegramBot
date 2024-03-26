import telebot
from telebot import types
bot = telebot.TeleBot('6997327762:AAG0TTlHe0Rx2A5w9OsKJRYYvIGqtBXDLqA')

@bot.message_handler(commands=['quiz'])
def question(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    iron = types.InlineKeyboardButton('1 kilo of iron', callback_data='answer_iron', quiz='quiz1')
    cotton = types.InlineKeyboardButton('1 kilo of cotton', callback_data='answer_cotton', quiz='quiz1')
    same = types.InlineKeyboardButton('same weight', callback_data='answer_same', quiz='quiz1')
    no_answer = types.InlineKeyboardButton('no correct answer', callback_data='no_answer', quiz='quiz1')
    markup.add(iron, cotton, same, no_answer)
    bot.send_message(message.chat.id, 'What is lighter?', reply_markup=markup)

@bot.message_handler(commands=['quiz2'])
def question2(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    iron = types.InlineKeyboardButton('iron', callback_data='answer_iron', quiz='quiz2')
    cotton = types.InlineKeyboardButton('cotton', callback_data='answer_cotton', quiz='quiz2')
    same = types.InlineKeyboardButton('same', callback_data='answer_same', quiz='quiz2')
    no_answer = types.InlineKeyboardButton('no answer', callback_data='no_answer', quiz='quiz2')
    markup.add(iron, cotton, same, no_answer)
    bot.send_message(message.chat.id, 'What is air?', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def answer1(callback):
    if callback.message:
        bot.send_message(callback.message.chat.id, 'this is question 1 response')

@bot.callback_query_handler(func=lambda call: True)
def answer2(callback):
    if callback.message:
        bot.send_message(callback.message.chat.id, 'this is question 2 response')

        
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f'Right now I am just a testing bot and I have only 3 builtin commands which are ("/quiz", "/quiz2") and I dont understand what to response on this message\n {message.text}')


bot.polling()