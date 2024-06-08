import discord
from discord.ext import commands
from letterboxdpy import user
from letterboxdpy.movie import Movie

class LetterboxdCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name='add_user', description='Add a user to the list of Letterboxd users')
    async def add_user(self, interaction: discord.Interaction, username: str):
        ''''''
        # await interaction.response.defer(thinking=True)
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
            await interaction.response.send_message(f'{username} will now be added to the list of letterboxd users!')
            self.bot.user_logged[username] = logged
        else:
            await interaction.response.send_message(f'{username}\'s account does not exist on letterboxd.')

    @discord.app_commands.command(name="user_info", description="Gets the user information from a user from letterboxd by adding the username.")
    async def user_info(self, interaction: discord.Interaction, username: str):
        ''''''
        await interaction.response.defer(thinking=True)
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

        embedVar = discord.Embed(title=f'{username}', description=userbio, color=0x00ff00)
        embedVar.set_thumbnail(url = usericon['url'])

        embedVar.add_field(name=f'{username}\'s favorite films are:', value='\n'.join(fave_list), inline=False)

        embedVar.add_field(name=f'**Most recently watched:**', value=f'{movie_name} *({movie_year})*', inline=False)
        embedVar.set_image(url = movie_poster) 

        await interaction.followup.send(embed = embedVar)

async def setup(bot):
    await bot.add_cog(LetterboxdCommands(bot))