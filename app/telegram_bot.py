import asyncio
import os

from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot import asyncio_filters
import pandas as pd

import database as db
from constants import *

bot = AsyncTeleBot(os.getenv('TOKEN'))
FIRST_USER = int(os.getenv('FIRST_USER'))
SECOND_USER = int(os.getenv('SECOND_USER'))


@bot.message_handler(chat_id=[FIRST_USER, SECOND_USER], commands=['movies', 'places', 'grocery', 'notes'])
async def tables(message):
    """ Quick access to the tables """

    buttons = ['/movies', '/places', '/grocery', '/notes']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    table = pd.read_sql_table(table_name=message.text[1:], con=db.engine)
    markdown_table = table.to_markdown(tablefmt="simple", index=False)
    await bot.send_message(message.chat.id, markdown_table, reply_markup=keyboard)


@bot.message_handler(chat_id=[FIRST_USER, SECOND_USER], commands=['addMovie', 'addPlace', 'addGrocery', 'addNote'])
async def add_into_table(message):
    """ Adds an entry into the table """

    message = message.text.split(maxsplit=1)
    table_name = message[0]
    with db.Session() as session:
        match message:
            case ['/addMovie', entry]:
                session.add(db.Movies(movie=entry))
            case ['/addPlace', entry]:
                session.add(db.Places(place=entry))
            case ['/addGrocery', entry]:
                session.add(db.Grocery(product=entry))
            case ['/addNote', entry]:
                session.add(db.Notes(note=entry))
        session.commit()

    await bot.send_message(FIRST_USER, NEW_ENTRY_MESSAGE[table_name])
    await bot.send_message(SECOND_USER, NEW_ENTRY_MESSAGE[table_name])


@bot.message_handler(chat_id=[FIRST_USER, SECOND_USER], commands=['delMovie', 'delPlace', 'delGrocery', 'delNote'])
async def delete_from_the_table(message):
    """ Deletes the last entry from the table """

    with db.Session() as session:
        match message.text:
            case '/delMovie':
                entry = session.query(db.Movies).order_by(db.Movies.id)
            case '/delPlace':
                entry = session.query(db.Places).order_by(db.Places.id)
            case '/delGrocery':
                entry = session.query(db.Grocery).order_by(db.Grocery.id)
            case '/delNote':
                entry = session.query(db.Notes).order_by(db.Notes.id)

        if any(entry):
            session.delete(entry[-1])
            session.commit()
            await bot.send_message(message.chat.id, DELETED_MESSAGE)
        else:
            await bot.send_message(message.chat.id, EMPTY_TABLE_MESSAGE)


@bot.message_handler(chat_id=[FIRST_USER, SECOND_USER], commands=['bought'])
async def mark_as_bought(message):
    """ Marks a product from the Grocery table as bought """

    product_id = message.text.removeprefix('/bought')
    with db.Session() as session:
        product = session.query(db.Grocery).filter(db.Grocery.id == product_id).one_or_none()
        if product:
            product.bought = '✅'
            session.commit()
            await bot.send_message(message.chat.id, PRODUCT_BOUGHT_MESSAGE)


@bot.message_handler(chat_id=[FIRST_USER, SECOND_USER], content_types=['text'])
async def handle_text(message):
    """ Handles any other text messages """

    await bot.send_message(message.chat.id, HELP_MESSAGE)


bot.add_custom_filter(asyncio_filters.ChatFilter())
asyncio.run(bot.polling())
