import asyncio
import os

from telebot.async_telebot import AsyncTeleBot
from telebot import types
import pandas as pd

import database as db
from constants import *

bot = AsyncTeleBot(os.getenv('TOKEN'))
FIRST_USER = int(os.getenv('FIRST_USER'))
SECOND_USER = int(os.getenv('SECOND_USER'))


@bot.message_handler(commands=['movies', 'places', 'grocery', 'notes'])
async def tables(message):
    """ Quick access to the tables """

    if message.chat.id not in (FIRST_USER, SECOND_USER):
        return

    buttons = ['/movies', '/places', '/grocery', '/notes']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    table = pd.read_sql_table(table_name=message.text[1:], con=db.engine)
    markdown_table = table.to_markdown(tablefmt="simple", index=False)
    await bot.send_message(message.chat.id, markdown_table, reply_markup=keyboard)


@bot.message_handler(commands=['addMovie', 'addPlace', 'addGrocery', 'addNote'])
async def add_into_table(message):
    """ Adds an entry into the table """

    if message.chat.id not in (FIRST_USER, SECOND_USER):
        return

    add_table = message.text.split(maxsplit=1)[0]
    entry = message.text.removeprefix(add_table)

    with db.Session() as session:
        if add_table == '/addMovie':
            session.add(db.Movies(movie=entry))
        elif add_table == '/addPlace':
            session.add(db.Places(place=entry))
        elif add_table == '/addGrocery':
            session.add(db.Grocery(product=entry))
        else:
            session.add(db.Notes(note=entry))
        session.commit()

    await bot.send_message(FIRST_USER, NEW_ENTRY_MESSAGE[add_table])
    await bot.send_message(SECOND_USER, NEW_ENTRY_MESSAGE[add_table])


@bot.message_handler(commands=['delMovie', 'delPlace', 'delGrocery', 'delNote'])
async def delete_from_the_table(message):
    """ Deletes the last entry from the table """

    if message.chat.id not in (FIRST_USER, SECOND_USER):
        return

    with db.Session() as session:
        if message.text.startswith('/delMovie'):
            entry = session.query(db.Movies).order_by(db.Movies.id)
        elif message.text.startswith('/delPlace'):
            entry = session.query(db.Places).order_by(db.Places.id)
        elif message.text.startswith('/delGrocery'):
            entry = session.query(db.Grocery).order_by(db.Grocery.id)
        else:
            entry = session.query(db.Notes).order_by(db.Notes.id)

        if any(entry):
            session.delete(entry[-1])
            session.commit()
            await bot.send_message(message.chat.id, DELETED_MESSAGE)
        else:
            await bot.send_message(message.chat.id, EMPTY_TABLE_MESSAGE)


@bot.message_handler(commands=['bought'])
async def mark_as_bought(message):
    """ Marks a product from the Grocery table as bought """

    if message.chat.id not in (FIRST_USER, SECOND_USER):
        return

    product_id = message.text.removeprefix('/bought')
    with db.Session() as session:
        bought_products = session.query(db.Grocery).filter(db.Grocery.id == product_id).all()
        for item in bought_products:
            item.bought = '✅'
        session.commit()
        await bot.send_message(message.chat.id, PRODUCT_BOUGHT_MESSAGE)


@bot.message_handler(content_types=['text'])
async def handle_text(message):
    """ Handles any other text messages """

    if message.chat.id not in (FIRST_USER, SECOND_USER):
        return

    await bot.send_message(message.chat.id, HELP_MESSAGE)


asyncio.run(bot.polling())
