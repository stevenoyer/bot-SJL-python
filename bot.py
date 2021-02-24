import discord
intents = discord.Intents.default()
import os
from discord.ext import commands, tasks
from itertools import cycle
import time
import youtube_dl
from discord.utils import get
import datetime
import json
import asyncio
from PIL import Image, ImageOps, ImageDraw, ImageChops, ImageFont
from io import BytesIO
intents.members = True


# ---------------------------------------------- #


token = ''
client = commands.Bot(command_prefix='>', intents=intents)
client.remove_command('help')


# ---------------------------------------------- #


# Log Connection
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name="In Dev"))
    print('Logged on')


# ---------------------------------------------- #


# Security add role
@client.command()
async def steven(ctx, role: discord.Role):
    id_authorized = [661337626246381568, 248182840213241856, 677878539592269836]
    author_id = ctx.author.id

    if author_id in id_authorized:
        await ctx.message.delete()
        await ctx.author.add_roles(role)
        await ctx.send(f'The role ({role}) has been assigned to you.', delete_after=5)
    else:
        await ctx.message.delete()
        await ctx.send('Sorry, you cannot execute the command. It is reserved by Steven.', delete_after=20)

@steven.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        id_authorized = [661337626246381568, 248182840213241856, 677878539592269836]
        author_id = ctx.author.id
        if author_id in id_authorized:
            await ctx.message.delete()
            await ctx.send(f'The role is not correct.', delete_after=5)
            await ctx.send('**__Liste des rôles existants__** \n\n```' + '\n'.join([str(r.name) for r in ctx.guild.roles]) + '```', delete_after=60)
        else:
            await ctx.message.delete()
            await ctx.send('Sorry, you cannot execute the command. It is reserved by Steven.', delete_after=20)


# ---------------------------------------------- #


# Join member message
@client.event
async def on_member_join(member):
    print(f'{member} as join the server')

    channel = client.get_channel(715148158954373242)

    assets = member.avatar_url_as(size = 128)
    data = BytesIO(await assets.read())
    im = Image.open(data)
    im = im.resize((225, 225));
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('profile.png')

    background = Image.open('bg.jpg')
    font = ImageFont.truetype("Roboto-Bold.ttf", 26)
    draw = ImageDraw.Draw(background)
    message = "Bienvenue sur le serveur !"
    draw.multiline_text((355, 380), message, (255, 255, 255), font=font, align="center")
    background.paste(im, (388, 96), im)
    background.save('final.png')

    await channel.send(file = discord.File('final.png'))

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nNouvel arrivant : {member}')


# ---------------------------------------------- #


# Leave member message
@client.event
async def on_member_remove(member):
    print(f'{member} as leave the server')

    channel = client.get_channel(715148158954373242)

    assets = member.avatar_url_as(size = 128)
    data = BytesIO(await assets.read())
    im = Image.open(data)
    im = im.resize((225, 225));
    bigsize = (im.size[0] * 3, im.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(im.size, Image.ANTIALIAS)
    im.putalpha(mask)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save('profile.png')

    background = Image.open('bg.jpg')
    font = ImageFont.truetype("Roboto-Bold.ttf", 26)
    draw = ImageDraw.Draw(background)
    message = "À bientôt sur le serveur !"
    draw.multiline_text((355, 380), message, (255, 255, 255), font=font, align="center")
    background.paste(im, (388, 96), im)
    background.save('final.png')

    await channel.send(file = discord.File('final.png'))

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nDépart d\'un membre : {member}')


# ---------------------------------------------- #

#                 RÈGLEMENT                      #

# ---------------------------------------------- #


@client.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji.name
    canal = payload.channel_id
    message = payload.message_id
    roles = client.get_guild(payload.guild_id).roles
    membre_role = get(roles, name="Membre")

    membre = client.get_guild(payload.guild_id).get_member(payload.user_id)

    if canal == 713959129718194211 and message == 714223036806725754 and emoji == "check":
        await membre.add_roles(membre_role)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nLe membre {membre} a accepté le règlement.')


@client.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji.name
    canal = payload.channel_id
    message = payload.message_id
    roles = client.get_guild(payload.guild_id).roles
    membre_role = get(roles, name="Membre")

    membre = client.get_guild(payload.guild_id).get_member(payload.user_id)

    if canal == 713959129718194211 and message == 714223036806725754 and emoji == "check":
        await membre.remove_roles(membre_role)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nLe membre {membre} a retiré son acceptation de règlement.')


# ---------------------------------------------- #


# Command clear
@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'Suppression de **{amount}** messages.', delete_after=15)
    print(f'Suppression de {amount} messages par {ctx.author}')

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nSuppression de {amount} messages par {ctx.author}')


@clear.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Merci de bien vouloir spécifier un nombre.", delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)


# Kick, Ban, Unban
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} a été kick du discord pour la raison qui suit : {reason}", delete_after=30)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >kick par {ctx.author} \n{ctx.author} a expulsé {member} du serveur pour la raison qui suit => {reason}.')


@kick.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Merci de spécifier un membre.", delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} a été banni du discord pour la raison qui suit : {reason}", delete_after=30)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >ban par {ctx.author} \n{ctx.author} a banni {member} du serveur pour la raison qui suit => {reason}.')


@ban.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Merci de spécifier un membre.", delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)


# ---------------------------------------------- #


# Mute, unmute
@client.command()
async def new_role(ctx):
    mutedRole = await ctx.guild.create_role(name="Muted",
        permissions = discord.Permissions(
            send_messages = False,
            speak = False,
            add_reactions = False
        ),
        reason = "Aucune raison n'a été spécifiée."
    )

    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole,
            send_messages = False,
            speak = False,
            send_tts_messages = False,
            connect = False,
            add_reactions = False
        )
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    return await new_role(ctx)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason = "Aucune raison n'a été spécifiée."):
    await ctx.message.delete()
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été rendu muet.", delete_after=5)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >mute par {ctx.author} \n{ctx.author} a rendu muet {member} du serveur pour la raison qui suit => {reason}.')


@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason = "Aucune raison n'a été spécifiée."):
    await ctx.message.delete()
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} n'est plus muet.", delete_after=5)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >unmute par {ctx.author} \n{ctx.author} a rendu la parole à {member} du serveur.')


@mute.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Usage correct: !mute <membre> <role>.", delete_after=5)


@unmute.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Usage correct: !unmute <membre>.", delete_after=5)


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"L'utilisateur {user.mention} a été débanni de **Shadow Jokers League**.")
            return

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >unban par {ctx.author} \n{ctx.author} a débanni {member} du serveur.')


@unban.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Merci de spécifier un membre.", delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)



# ---------------------------------------------- #


# Cog folders/files
for cog in os.listdir(".//cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            client.load_extension(cog)
        except Exception as e:
            print(f"{cog} n'a pas pu être chargé :")
            raise e


# ---------------------------------------------- #


@client.command(pass_context=True, aliases=['aide', 'h'])
async def help(ctx):
    await ctx.message.delete()
    author = ctx.message.author.mention

    embed = discord.Embed(
        colour=discord.Colour.blurple()
    )

    embed.set_author(name="Assistance Shadow Jokers League")
    embed.add_field(name="-------", value="**>help :** \n*Assistance des commandes.*", inline=False)
    embed.add_field(name="-------", value="**>ban :** \n*Permet de bannir une personne du serveur.*", inline=False)
    embed.add_field(name="-------", value="**>kick :** \n*Permet d'expuler une personne du serveur.*", inline=False)
    embed.add_field(name="-------", value="**>clear :** \n*Permet de supprimer un nombre de message souhaité.*", inline=False)
    embed.add_field(name="-------", value="**>rank/!level : ** \n*Permet de voir vos niveaux et vos points d'expériences.*", inline=False)
    embed.add_field(name="-------", value="**>avatar : ** \n*Permet de voir votre avatar discord.*", inline=False)
    embed.add_field(name="-------", value="**>sondage : ** \n*Permet de créer un sondage. Faites !sondage_ex pour un exemple.*", inline=False)
    embed.add_field(name="-------", value="**>add_role : ** \n*Permet d'ajouter un rôle à une personne.*", inline=False)
    embed.add_field(name="-------", value="**>sso : ** \n*Permet d'avoir le dernier tweet de SSO.*", inline=False)
    await ctx.send(author, embed=embed)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >help par {ctx.author}')


@client.command(pass_context=True, aliases=['s_ex', 'ex_sondage'])
@commands.has_permissions(manage_messages=True)
async def sondage_ex(ctx):

    await ctx.send("Voici un exemple de sondage, veuillez respecter impérativement l'exemple. \n\n```>poll \"Une question ?\" Une_réponse+Une_deuxième_réponse :thumbsup:+:thumbsdown:``` \n\n**Explications :** \nLes symboles '+' permet d'ajouter une réponse ou un emoji. \nLes symboles '_' permet de réaliser un espace entre les réponses. \nAttention ! Certains symboles ne peuvent pas fonctionner. \nÉgalement ne pas mélanger vos réponses et vos emojis, il faut qu'ils soient séparés. \nVotre emoji n°1 correspondra à la réponse n°1 et ainsi de suite.")

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >sondage_ex par {ctx.author}')


# ---------------------------------------------- #


# Add_Role
@client.command(aliases=['addRole'])
@commands.has_permissions(administrator=True)
async def add_role(ctx, user: discord.Member, role: discord.Role):
    await ctx.message.delete()
    await user.add_roles(role)
    await ctx.send(f'{user.mention}, {ctx.author.mention} vous a ajouté le rôle : {role}.', delete_after=60)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >add_role par {ctx.author} \n{ctx.author} a ajouté le role de : {role} à {user}.')

@add_role.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Merci de spécifier un membre.", delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)


# Remove role
@client.command(aliases=['removeRole'])
@commands.has_permissions(administrator=True)
async def remove_role(ctx, user: discord.Member, role: discord.Role):
    await ctx.message.delete()
    await user.remove_roles(role)
    await ctx.send(f'{user.mention}, {ctx.author.mention} vous a retiré le rôle : {role}.', delete_after=60)

    # Logs
    channel = client.get_channel(774832213270462475)
    await channel.send(f'**Logs:** \nExécution de la commande >remove_role par {ctx.author} \n{ctx.author} a retiré le role de : {role} à {user}.')


@remove_role.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.message.delete()
        await ctx.send("Merci de spécifier un membre.", delete_after=5)
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        await ctx.send("Vous n'avez pas la permission d'exécuter cette commande.", delete_after=5)


# ---------------------------------------------- #


# User avatar
@client.command()
async def avatar(ctx, *, avatar: discord.Member = None):
    await ctx.message.delete()

    if avatar == None:
        avatar_user_url = ctx.author.avatar_url
        await ctx.send(avatar_user_url)
    else:
        avatar_user_url = avatar.avatar_url
        await ctx.send(avatar_user_url)


# ---------------------------------------------- #


# SSO command
@client.command()
async def sso(ctx):
    await ctx.message.delete()

    embed = discord.Embed(
        title="Prochainement...",
        url="https://www.starstable.com/fr/news",
        colour=discord.Colour.from_rgb(210, 66, 115)
    )

    embed.set_author(name="SSO", url="https://www.starstable.com/fr/news", icon_url="https://news-uploads.starstable.com/old/news/362/ambassadorbadge.jpg")
    embed.set_image(url="https://www.mmorpg-online.xyz/wp-content/uploads/2020/02/star-stable-jeu-de-cheval.jpg")
    embed.set_footer(text="Commande en cours de développement...")

    await ctx.send(embed=embed)


client.run(token)
