#
#
#
#

import requests
import os
import discord
from discord import Intents, Client, Message
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_logged = {}

bot = MyBot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    with open("users.txt", "r") as file:
        for username in file.readlines():
            username = username[:-1]
            user_instance = user.User(username)
            diary = user.user_diary(user_instance)
            logged = len(diary['entrys'].keys())
            bot.user_logged[username] = logged
    
    film_refresh.start()

@bot.command()
async def add_user(ctx, arg):
    ''''''

    user_instance = user.User(arg)
    diary = user.user_diary(user_instance)
    logged = len(diary['entrys'].keys())
    try:
        user.User(arg)
        user_exists = True
    except:
        user_exists = False

    if user_exists:
        username = arg.lower()
        print(username)
        with open("users.txt", "a") as infile:
            infile.write(username + "\n")
        await ctx.send(f'{arg} will now be added to the list of letterboxd users!')
        bot.user_logged[username] = logged
    else:
        await ctx.send(f'{arg}\'s account does not exist on letterboxd.')

@bot.command()
async def user_info(ctx, arg):
    ''''''
    user_instance = user.User(arg)
    username = getattr(user_instance, 'username')

    userbio = f'this user does not have a bio'
    if hasattr(user_instance, 'bio'):
        userbio = getattr(user_instance, 'bio')
    userfaves = getattr(user_instance, 'favorites')
    usericon = getattr(user_instance, 'avatar')

    diary = user.user_diary(user_instance)

    recent = list(diary['entrys'].keys())[0]
    recent_film_slug = str(diary['entrys'][recent]['slug'])

    movie_instance = Movie(recent_film_slug)
    movie_name = getattr(movie_instance, 'title')
    movie_poster = getattr(movie_instance, 'poster')
    movie_year = getattr(movie_instance, 'year')

    fave_list = []
    for item in userfaves.items():
        fave_instance = Movie(str(item[1]['slug']))
        fave_year = getattr(fave_instance, 'year')
        fave_list.append(f'{item[1]['name']} *({fave_year})*')

    if fave_list == []:
        fave_list = ["This user has no favorite films"]

    embedVar = discord.Embed(title=f'{username}', description=userbio, color=0x00ff00)
    embedVar.set_thumbnail(url = usericon['url'])

    embedVar.add_field(name=f'{username}\'s favorite films are:', value='\n'.join(fave_list), inline=False)

    embedVar.add_field(name=f'**Most recently watched:**', value=f'{movie_name} *({movie_year})*', inline=False)
    embedVar.set_image(url = movie_poster) 

    await ctx.send(embed = embedVar)

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

        embedVar = discord.Embed(title=f'{'thijmenadam'}', color=0x00ff00)
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