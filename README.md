Hello! 😊
This is a telegram-bot for couples to store various information for later use. 
I'm sure you've ever sent your significant one a name of a movie that you should watch or a place you want to visit together. And spent a lot of time scrolling through your chat to find notes when you are finally together, ready to enjoy the weekend.
So this bot is supposed to help you with that! It allows you to add, delete any text in the tables such as:

- Movies
- Grocery (Shopping list)
- Places
- Notes (for casual notes, preferably something nice)

It is private for just two users so only certain people can have an access to the lists.

Here you can see some examples of bot's work:

<img width="530" alt="Screenshot 2022-12-21 at 17 46 22" src="https://user-images.githubusercontent.com/96263809/208932560-cef81615-e4db-4827-bbb1-7a8d78104bd4.png">

<img width="526" alt="Screenshot 2022-12-21 at 17 46 55" src="https://user-images.githubusercontent.com/96263809/208932592-81ca762a-a9b3-45e8-ad73-a871d5c81458.png">


To start your own bot based on this logic you should do the following:

- Download the repository;
- Create a file .env with the variables such as: 

    >- DATABASE_URL=postgresql://username:password@db:5432/tables_db
    >- TOKEN (get it from https://t.me/BotFather)
    >- FIRST_USER (this is a message.chat.id which you can find in https://t.me/RawDataBot)
    >- SECOND_USER (message.chat.id for another person)

- to deploy the app from the root folder:

  docker-compose up -d --build
  
- to launch the bot:

  docker-compose run --rm -d --name bot app /app/telegram_bot.py
  
- to stop the bot:

  docker stop bot
  
- to switch containers off:

  docker-compose down
