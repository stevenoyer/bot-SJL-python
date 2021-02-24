import discord
import asyncio
from discord.ext import commands
import random

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=['poll'])
    async def sondage(self, ctx, question, options: str, emojis: str):
        await ctx.message.delete()

        author = ctx.message.author
        server = ctx.message.guild

        extract_options = options.replace("+", " ")
        option = extract_options.split(" ")

        extract_emojis = emojis.replace("+", " ")
        emoji = extract_emojis.split(" ")

        if len(options) <= 1:
            await ctx.send("Erreur, vous devez avoir plusieurs options.")
            return

        if len(emojis) <= 1:
            await ctx.send("Erreur, vous devez avoir le même nombre d'options.")

        if len(options) > 2:
            if len(emojis) > 2:
                reactions = emoji
                # print(reactions)

        description = []
        for x, extract_options in enumerate(option):
            description += '\n {} {}'.format(reactions[x], option[x].replace("_", " "))

        embed = discord.Embed(title = question, colour=discord.Colour.from_rgb(210, 66, 115), description = ''.join(description))
        react_message = await ctx.send(embed = embed)

        for reaction in reactions[:len(option)]:
            await react_message.add_reaction(reaction)

        embed.set_footer(text=f'ID Sondage : {react_message.id} \nAuteur du sondage : {author}')

        await react_message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Poll(bot))
