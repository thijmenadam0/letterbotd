#
#
#
#

import requests
import os
import discord
from discord import Intents, Client, Message, app_commands
from discord.ext import tasks, commands
from letterboxdpy import user
from letterboxdpy.movie import Movie

# LOAD TOKEN
TOKEN = os.getenv('DISCORD_TOKEN')

# SET UP BOT
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)
channelID = 1247541112445472852

class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_logged = {}

    async def setup_hook(self):
        print("Setting up commands...")
        await self.load_extension('cogs.letterboxd_commands')
        await self.tree.sync()
        print("Commands synced.")


bot = MyBot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    with open("users.txt", "r") as file:
        for username in file.readlines():
            username = username.strip()
            try:
                user_instance = user.User(username)
                diary = user.user_diary(user_instance)
                logged = len(diary['entrys'].keys())
                bot.user_logged[username] = logged
            except AttributeError as e:
                print(f"Failed to load user '{username}': {e}")

    await bot.tree.sync()
    film_refresh.start()


async def film_info(ctx, ui):
    ''''''
    usericon = getattr(ui, 'avatar')
    username = getattr(ui, 'username')

    diary = user.user_diary(ui)
    logged = len(diary['entrys'].keys())
    
    if logged > bot.user_logged[username]:
        recent = list(diary['entrys'].keys())[0]
        recent_film_slug = str(diary['entrys'][recent]['slug'])

        movie_instance = Movie(recent_film_slug)
        movie_name = getattr(movie_instance, 'title')
        movie_poster = getattr(movie_instance, 'poster')
        movie_year = getattr(movie_instance, 'year')

        embedVar = discord.Embed(title=f'{username}', color=0x00ff00)
        embedVar.set_thumbnail(url = usericon['url'])

        rating = diary['entrys'][recent]['actions']['rating'] / 2

        embedVar.add_field(name=f'**JUST WATCHED**', value=f'{movie_name} *({movie_year})*', inline=False)

        if rating.is_integer():
            print(rating)
            embedVar.add_field(name="Rating: ", value=f'{int(rating)}/5')
        else:
            embedVar.add_field(name="Rating: ", value=f'{float(rating)}/5')
        embedVar.set_image(url = movie_poster) 

        await ctx.send(embed = embedVar)
        bot.user_logged[username] = logged


@tasks.loop(seconds=60)
async def film_refresh():
    ctx = bot.get_channel(int(channelID))
    for username in bot.user_logged.keys():
        user_instance = user.User(username)
        await film_info(ctx, user_instance)


def main() -> None:
    bot.run(token="MTI0NzUzOTQwODMxMjMzNjQyNQ.GRY2dF.Tje2QwjZYgTxKDnS1vfIx-XByLB8UKrKrpW8Xo")

    

if __name__ == "__main__":
    main()