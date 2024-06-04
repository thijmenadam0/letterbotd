#
#
#
#

import requests
import os
import discord
from discord import Intents, Client, Message
from discord.ext import commands
from responses import get_response
from letterboxdpy import user


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

    userbio = "This user has no bio"
    if hasattr(user_instance, 'bio'):
        userbio = getattr(user_instance, 'bio')
    userfaves = getattr(user_instance, 'favorites')
    usericon = getattr(user_instance, 'avatar')

    fave_list = []
    for item in userfaves.items():
        fave_list.append(item[1]['name'])
    
    if fave_list == []:
        fave_list = ["This user has no favorite films"]

    embedVar = discord.Embed(title=f'Letterboxd user: {username}', description=f'bio: {userbio}', color=0x00ff00)
    embedVar.set_thumbnail(url = usericon['url'])

    embedVar.add_field(name="This users favorite films are:", value='\n'.join(fave_list), inline=False)
    embedVar.add_field(name="Field2", value="hi2", inline=False)

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