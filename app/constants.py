

HELP_MESSAGE = 'Hello dear! 😘 Please type /movies, /places, /grocery or /notes to get the tables. \n' \
               'To add into the table use commands: \n' \
               '- /addMovie, /addPlace, /addGrocery, /addNote following with the necessary text. \n' \
               'To delete the last entry from the table: \n' \
               '- /delMovie, /delPlace, /delGrocery, /delNote \n' \
               'To mark a product as bought: \n' \
               '- /bought <product id from the table>'

MOVIE_MESSAGE = '🎬 The Movies table has been updated'

PLACE_MESSAGE = '💃 The Places table has been updated'

GROCERY_MESSAGE = '🛒 The Grocery table has been updated'

NOTE_MESSAGE = '✍️ The Notes table has been updated'

DELETED_MESSAGE = 'The last entry of the table has been deleted'

PRODUCT_BOUGHT_MESSAGE = 'You have just bought something. Hopefully something tasty!😋'

EMPTY_TABLE_MESSAGE = 'The table is already empty!🤷‍♀️'

NEW_ENTRY_MESSAGE = {
    '/addMovie': MOVIE_MESSAGE,
    '/addPlace': PLACE_MESSAGE,
    '/addGrocery': GROCERY_MESSAGE,
    '/addNote': NOTE_MESSAGE,
}
