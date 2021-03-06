import discord
from discord.ext import commands
import datetime
import json
import asyncio


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.loop.create_task(self.save_users())

        with open(r"users.json", 'r') as f:
            self.users = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):
        print("File Levels.py loaded")

    async def save_users(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            with open(r"users.json", 'w') as f:
                json.dump(self.users, f, indent=4)

            await asyncio.sleep(5)

    def lvl_up(self, author_id):
        cur_xp = self.users[author_id]['exp']
        cur_lvl = self.users[author_id]['level']

        if cur_xp >= round((4 * (cur_lvl ** 3)) / 5):
            self.users[author_id]['level'] += 1
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        author_id = str(message.author.id)

        if not author_id in self.users:
            self.users[author_id] = {}
            self.users[author_id]['level'] = 0
            self.users[author_id]['exp'] = 0

        self.users[author_id]['exp'] += 1

        if self.lvl_up(author_id):
            await message.channel.send(f"{message.author.mention} tu as atteint le niveau {self.users[author_id]['level']} !")


    @commands.command(aliases=['level', 'levels', 'r', 'l'])
    async def rank(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = str(member.id)

        if not member_id in self.users:
            await ctx.send("Tu n'as pas encore de niveau !")
        else:
            embed = discord.Embed(color=member.color)

            embed.set_author(name=f"Level - {member}", icon_url=member.avatar_url)
            embed.add_field(name="Level", value=self.users[member_id]['level'])
            embed.add_field(name="XP", value=self.users[member_id]['exp'])
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Levels(bot))
