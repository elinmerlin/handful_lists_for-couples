import os

from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import pandas as pd

import data.database as db
from constants import *

bot = AsyncTeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['movies', 'places', 'grocery', 'notes'])
async def tables(message):
    """ Quick access to the tables """

    buttons = ['/movies', '/places', '/grocery', '/notes']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)

    table = pd.read_sql_table(table_name=message[1:], con=db.engine)
    await bot.send_message(message.chat.id, table, reply_markup=keyboard)


@bot.message_handler(commands=['addMovie', 'addPlace', 'addGrocery', 'addNote'])
async def add_into_table(message):
    """ Adds an entry into the table """

    async with db.Session() as session:
        if message.text.startswith('/addMovie'):
            entry = message.text.removeprefix('/addMovie')
            session.add(db.Movies(movie=entry))
            await bot.send_message(message.chat.id, MOVIE_MESSAGE)

        elif message.text.startswith('/addPlace'):
            entry = message.text.removeprefix('/addPlace')
            session.add(db.Places(place=entry))
            await bot.send_message(message.chat.id, PLACE_MESSAGE)

        elif message.text.startswith('/addGrocery'):
            entry = message.text.removeprefix('/addGrocery')
            session.add(db.Grocery(product=entry))
            await bot.send_message(message.chat.id, GROCERY_MESSAGE)

        else:
            entry = message.text.removeprefix('/addNote')
            session.add(db.Notes(note=entry))
            await bot.send_message(message.chat.id, NOTE_MESSAGE)

        session.commit()


@bot.message_handler(commands=['delMovie', 'delPlace', 'delGrocery', 'delNote'])
async def delete_from_the_table(message):
    """ Deletes the last entry from the table """

    async with db.Session() as session:
        if message.startswith('/delMovie'):
            entry = session.query(db.Movies).order_by(db.Movies.id)[-1]
            await bot.send_message(message.chat.id, MOVIE_DEL_MESSAGE)
        elif message.startswith('/delPlace'):
            entry = session.query(db.Places).order_by(db.Places.id)[-1]
            await bot.send_message(message.chat.id, PLACE_DEL_MESSAGE)
        elif message.startswith('/delGrocery'):
            entry = session.query(db.Grocery).order_by(db.Grocery.id)[-1]
            await bot.send_message(message.chat.id, GROCERY_DEL_MESSAGE)
        else:
            entry = session.query(db.Notes).order_by(db.Notes.id)[-1]
            await bot.send_message(message.chat.id, NOTES_DEL_MESSAGE)
        session.delete(entry)
        session.commit()


@bot.message_handler(commands=['bought'])
async def mark_as_bought(message):
    """ Marks a product from the Grocery table as bought """

    product = message.removeprefix('/bought')
    async with db.Session() as session:
        bought_products = session.query(db.Grocery).filter(db.Grocery.product == product).all()
        for item in bought_products:
            item.bought = '✅'
        session.commit()
        await bot.send_message(message.chat.id, PRODUCT_BOUGHT_MESSAGE)


@bot.message_handler(content_types=['text'])
async def handle_text(message):
    """ Handles any other text messages """

    await bot.send_message(message.chat.id, HELP_MESSAGE)


asyncio.run(bot.polling())
