#
#
#
#

import requests
import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands
from letterboxdpy import user
from letterboxdpy.movie import Movie



# LOAD TOKEN
TOKEN = os.getenv('DISCORD_TOKEN')

# SET UP BOT
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def user_info(ctx, arg):
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

# MESSAGE FUNCTIONALITY
# async def send_message(message, user_message) -> None:
#     if not user_message:
#         print("Message was empty because intents were not enabled")
#         return
#     
#     try:
#         response = get_response(user_message)
#         await message.channel.send(response)
#     except Exception as e:
#         print(e)

# HANDLE STARTUP FOR BOT
# @client.event
# async def on_ready() -> None:
#     print("f'{client.user} is now running")


# @client.event
# async def on_message(message) -> None:
#     if message.author == client.user:
#         return
    
#     username = str(message.author)
#     user_message = message.content
#     channel = str(message.channel)

#     print(f'[{channel}], {username}: "{user_message}"')
#     await send_message(message, user_message)

def main() -> None:
    bot.run(token="MTI0NzUzOTQwODMxMjMzNjQyNQ.GRY2dF.Tje2QwjZYgTxKDnS1vfIx-XByLB8UKrKrpW8Xo")

    #thijmen = user.User("thijmenadam")
    #print(user.user_diary(thijmen))

    #print("Movie: ", user.user_diary(thijmen)[0]['movie'])
    #print("Watched on: ", user.user_diary(thijmen)[0]['date'])
    #print("Rating: ", user.user_diary(thijmen)[0]['rating'])
    #print("Review: ", user.user_reviews(thijmen)[0]['review'])
    

if __name__ == "__main__":
    main()