import telebot
from telebot import types

bot = telebot.TeleBot('6997327762:AAG0TTlHe0Rx2A5w9OsKJRYYvIGqtBXDLqA')

# Define quiz questions and answers
quiz_questions = {
    'quiz1': {
        'question': 'What is lighter?',
        'options': ['1 kilo of iron', '1 kilo of cotton', 'same weight', 'no correct answer'],
        'correct_answer': 'same weight'
    },
    'quiz2': {
        'question': 'What is air?',
        'options': ['iron', 'cotton', 'same', 'no answer'],
        'correct_answer': 'same'
    }
}

@bot.message_handler(commands=['quiz'])
def question(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for option in quiz_questions['quiz1']['options']:
        markup.add(types.InlineKeyboardButton(option, callback_data=option))
    bot.send_message(message.chat.id, quiz_questions['quiz1']['question'], reply_markup=markup)

@bot.message_handler(commands=['quiz2'])
def question2(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    for option in quiz_questions['quiz2']['options']:
        markup.add(types.InlineKeyboardButton(option, callback_data=option))
    bot.send_message(message.chat.id, quiz_questions['quiz2']['question'], reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in [option for option in quiz_questions['quiz1']['options']])
def answer1(callback):
    user_answer = callback.data
    bot.send_message(callback.message.chat.id, user_answer)
    correct_answer = quiz_questions['quiz1']['correct_answer']
    if user_answer == correct_answer:
        bot.send_message(callback.message.chat.id, 'Congratulations! Your response is correct.')
    else:
        bot.send_message(callback.message.chat.id, 'Sorry, your response is incorrect.')

@bot.callback_query_handler(func=lambda call: call.data in [option for option in quiz_questions['quiz2']['options']])
def answer2(callback):
    user_answer = callback.data
    bot.send_message(callback.message.chat.id, user_answer)
    correct_answer = quiz_questions['quiz2']['correct_answer']
    if user_answer == correct_answer:
        bot.send_message(callback.message.chat.id, 'Congratulations! Your response is correct.')
    else:
        bot.send_message(callback.message.chat.id, 'Sorry, your response is incorrect.')


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, f'Right now I am just a testing bot and I have only 3 builtin commands which are ("/quiz", "/quiz2") and I dont understand what to response on this message\n {message.text}')


bot.polling()