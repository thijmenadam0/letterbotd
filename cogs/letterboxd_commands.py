import discord
from discord.ext import commands
from letterboxdpy import user
from letterboxdpy.movie import Movie
import random
import os

class LetterboxdCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='add_user', description='Add a user to the list of Letterboxd users')
    async def add_user(self, interaction: discord.Interaction, username: str):
        ''''''
        await interaction.response.defer(thinking=True)
        user_instance = user.User(username)
        diary = user.user_diary(user_instance)
        logged = len(diary['entrys'].keys())
        try:
            user.User(username)
            user_exists = True
        except:
            user_exists = False

        if user_exists:
            with open("users.txt", "a") as infile:
                infile.write(username.lower() + "\n")
            await interaction.followup.send(f'{username} will now be added to the list of letterboxd users!')
            self.bot.user_logged[username] = logged
        else:
            await interaction.followup.send(f'{username}\'s account does not exist on letterboxd.')


    @discord.app_commands.command(name='remove_user', description='Removes a user from the list of letterboxd users')
    async def remove_user(self, interaction: discord.Interaction, username: str):
        ''''''
        await interaction.response.defer(thinking=True)
        with open("users.txt", "w") as infile:
            for line in infile:
                if line.strip("\n") != username:
                    infile.write(line)
                    await interaction.followup.send(f'{username} will now be removed from the list of letterboxd users!')
                    del self.bot.user_logged[username]
                else:
                     await interaction.followup.send(f'{username} does not exist in the list of letterboxd users.')
        await interaction.followup.send(f'{username}\'s account does not exist on letterboxd.')
        print(self.bot.user_logged[username])


    @discord.app_commands.command(name="user_info", description="Gets the user information from a user from letterboxd by adding the username.")
    async def user_info(self, interaction: discord.Interaction, username: str):
        ''''''
        await interaction.response.defer(thinking=True)
        colors = [(255,128,0), (0,224,84), (64,188,244)]

        try:
            user.User(username)
            user_exists = True
        except:
            user_exists = False
        
        if user_exists:
            user_instance = user.User(username)
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

            color_set = random.choice(colors)

            embedVar = discord.Embed(title=f'{username}', description=userbio, color=discord.Color.from_rgb(color_set[0], color_set[1], color_set[2]))
            embedVar.set_thumbnail(url = usericon['url'])

            embedVar.add_field(name=f'{username}\'s favorite films are:', value='\n'.join(fave_list), inline=False)

            embedVar.add_field(name=f'**Most recently watched:**', value=f'{movie_name} *({movie_year})*', inline=False)
            embedVar.set_image(url = movie_poster) 

            await interaction.followup.send(embed = embedVar)
        else:
            await interaction.followup.send(f'{username} has not been found on letterboxd.')


    @discord.app_commands.command(name="initiate", description="Initiates the bot in the right channel so it can start refreshing for films!")
    async def initiate(self, interaction: discord.Interaction):
        ''''''
        await interaction.response.defer(thinking=True)
        channelID = interaction.channel.id

        if os.path.exists("channel.txt"):
            await interaction.followup.send("You have already initiated this elsewhere")
        else:
            with open("channel.txt", "w") as infile:
                infile.write(f'{channelID}')
    
            await interaction.followup.send(f'{interaction.channel.name} has been initiated as the channel where updates about films get sent.')


    @discord.app_commands.command(name="remove_initiation", description="Removes the initiation of the channel. This means that no updates will be sent.")
    async def remove_initiation(self, interaction: discord.Interaction):
        ''''''
        await interaction.response.defer(thinking=True)

        if os.path.exists("channel.txt"):
            os.remove("channel.txt")
            await interaction.followup.send(f'Your original initiation has been removed.')
        else:
            await interaction.followup.send(f'You have not initiated a channel before.')


async def setup(bot):
    await bot.add_cog(LetterboxdCommands(bot))