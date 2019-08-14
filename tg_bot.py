import os
import random
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from dotenv import load_dotenv
from functools import partial
import redis
from questions import get_all_questions

CHOOSING, ATTEMPT = range(2)


def help(bot, update):
    update.message.reply_text(
        '''Это бот для исторической викторины. Выбирай вопросы, давай правильные ответы!

Чтобы выйти, набери команды /exit или /cancel
        '''
        )
    return CHOOSING


def start(bot, update):
    keyboard = [['Новый вопрос', 'Сдаться']]
    markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    user = f'{update.message.from_user.first_name}'
    update.message.reply_text(f'Привет, {user}! Я бот-викторина.', reply_markup=markup)
    return CHOOSING


def handle_new_question(bot, update, questions, redis_db):
    rm_question, rm_answer = random.choice(tuple(questions.items()))
    del questions[rm_question]

    redis_db.set(update.message.chat_id, rm_answer)
    update.message.reply_text(rm_question)
    return ATTEMPT


def handle_answer(bot, update, redis_db):
    answer = redis_db.get(update.message.chat_id)

    if update.message.text.lower() == answer.lower().strip('.'):
        update.message.reply_text('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
        return CHOOSING
    else:
        update.message.reply_text('Неправильно... Попробуешь ещё раз?')
        return ATTEMPT


def handle_give_up(bot, update, redis_db):
    answer = redis_db.get(update.message.chat_id)
    update.message.reply_text(
        f'Правильный ответ был {answer}\n\n'
        f'Для продолжения выбери "Новый Вопрос", для выхода из игры набери команды выхода.'
    )
    return CHOOSING


def end(bot, update):
    user = f'{update.message.from_user.first_name}'
    update.message.reply_text(
        f'Пока {user}! Надеюсь, ты попробуешь еще.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    db_url = os.getenv('REDIS_DATABASE')
    db_port = os.getenv('REDIS_PORT')
    db_password = os.getenv('REDIS_PSWRD')
    tg_token = os.getenv('TG_TOKEN')

    all_questions = get_all_questions()

    redis_db = redis.Redis(
        host=db_url, port=db_port, password=db_password, charset='utf-8', decode_responses=True)

    updater = Updater(tg_token)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            CHOOSING: [RegexHandler('^Новый вопрос$', partial(handle_new_question,
                                                              questions=all_questions,
                                                              redis_db=redis_db)),
                       CommandHandler('help', help)],

            ATTEMPT: [RegexHandler('^Сдаться$', partial(handle_give_up, redis_db=redis_db)),
                      MessageHandler(Filters.text, partial(handle_answer, redis_db=redis_db))]
        },

        fallbacks=[CommandHandler('cancel', end),
                   CommandHandler('exit', end)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    main()
