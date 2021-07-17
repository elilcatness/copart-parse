import os
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler

from data.copart import Copart
from data.utils import EditThread


def search(update: Update, context):
    default_args = [*([0, float('inf')] * 2)]
    names = ['year_from', 'year_to', 'price_from', 'price_to']
    try:
        filters = {names[i]: int(context.args[i]) if i < len(context.args) and context.args[i] != '-1'
                   else default_args[i] for i in range(len(default_args))}
    except ValueError:
        return update.message.reply_text('Все аргументы должны быть целочисленными!')
    message = update.message.reply_text('Начинаем поиск...')
    edit_thread = EditThread(message)
    edit_thread.start()
    start_time = time.time()
    copart = Copart()
    output = copart.get_data(filters)
    edit_thread.stop()
    update.message.reply_text(f'Найдено {len(output)} автомобилей.\n'
                              f'Время поиска: {time.time() - start_time:.2f} секунд')
    for car in output:
        update.message.reply_text(car['ld'])


def start(update, _):
    update.message.reply_text('Привет! Это бот-парсер американских автобирж. '
                              'Введите /search {year_from} {year_to} {price_from} {price_to} '
                              'для поиска авто')


def main():
    updater = Updater(os.getenv('tg_token'))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('search', search, pass_args=True))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
