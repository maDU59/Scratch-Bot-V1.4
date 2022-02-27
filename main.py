import requests
import discord
import os
import scratchclient
import time
import asyncio
import re
import string
import random
import threading
import scratchconnect
from datetime import datetime
#from discord.ui import Button
from discord.ext import commands, tasks
from scratchclient import ScratchSession

from keep_alive import keep_alive

keep_alive()

color = 0xFF8F00


login = scratchconnect.ScratchConnect("___Scratch-FR___", 1234567890)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="s!",
                   description="Bot de maDU59_#5352",
                   case_insensitive=True,
                   help_command=None,
                   intents=intents)


def get_scratch_profile(id, content):
    pos1 = content.find(str(id))
    pos1 += len(str(id))
    pos1 += 3
    pos2 = pos1
    x = 0
    while x == 0:
        if content[pos2] == '"':
            x = 1
        else:
            pos2 += 1
    print(pos2)
    name = content[pos1:pos2]
    print(name)
    return name


def get_discord_id_with_scratch_username(username, content):
    pos1 = content.find(str(username))
    pos1 -= 3
    pos2 = pos1
    pos1 = content.rfind('"', 0, pos1 - 3)
    pos1 += 1
    id = content[pos1:pos2]
    print(id)
    return id


def t(text, dest):
    print("translate")
    file = open("Français.txt", "r")
    string = file.read()
    file.close()
    liste = string.split(';')
    file = open("Anglais.txt", "r")
    string2 = file.read()
    file.close()
    liste2 = string2.split(';')
    try:
        original_pos = liste.index(text)
        if dest == "en":
            text = liste2[original_pos]
    except:
        try:
            original_pos = liste2.index(text)
            if dest == "fr":
                text = liste[original_pos]
        except:
            print("There is no translation")
    return (text)


def get_color(guild_id=None):
    if guild_id == None:
        code = 0xFF8F00
        return (code)
    print(guild_id)
    try:
        file = open("embed_color.json", "r")
        content = file.read()
        file.close
        pos1 = content.find(str(guild_id))
        pos1 += len(str(guild_id))
        pos1 += 3
        pos2 = pos1
        i = 0
        while i == 0:
            pos2 += 1
            if content[pos2] == '"':
                i = 1
        code = content[pos1:pos2]
        print(code)
        if "random" in code:
            code = 0xFF8F00
            col = lambda: random.randint(0, 255)
            code = '0x' + '%02X%02X%02X' % (col(), col(), col())
        code = int(hex(int(code.replace("0x", ""), 16)), 0)
        print(code)
    except:
        code = 0xFF8F00
        pass
    return (code)


def get_language(guild_id=None):
    if guild_id == None:
        language = "en"
        return (language)
    print(guild_id)
    file = open("langue.json", "r")
    content = file.read()
    file.close
    print(content)
    try:
        pos1 = content.find(str(guild_id))
        pos1 += len(str(guild_id))
        pos1 += 3
        pos2 = pos1
        i = 0
        while i == 0:
            pos2 += 1
            if content[pos2] == '"':
                i = 1
        code = content[pos1:pos2]
        language = code
        print(code)
    except:
        language = "en"
        pass
    return (language)


def set_status():
    number_of_servers = str(len(bot.guilds))
    return number_of_servers


def get_followers(name):
    headers = {
        "user-agent":
        "Mozilla/5.0 (X11; CrOS x86_64 13982.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.130 Safari/537.36"
    }
    html = requests.get(f"https://scratch.mit.edu/users/{name}/followers",
                        headers=headers).text
    match = re.search("&raquo;\s+Followers \((\d+)\)",
                      html)  # this is kind of crude but it works
    followers = f"{match.groups()[0]}"
    return followers


@bot.event
async def on_ready():
    print("Ready!")
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=f"{set_status()} servers"))
    checkTendances.start()


@tasks.loop(seconds=1)
async def checkTendances():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")

    if (current_time == '19:00:00'):
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching, name=f"{set_status()} servers")
                                  )
        channel = bot.get_channel(912752538212790273)
        messages = await channel.purge(limit=11)
        number = 0
        numberMax = 10
        trendings = login.explore_projects(mode="trending", query="*")
        while number < numberMax:
            try:
                langue = get_language(channel.message.guild.id)
                color = get_color(channel.message.guild.id)
            except:
                print("error")
                langue = "fr"
                color = 0xFFAAAA
            dico=trendings[number]
            id = dico.get("id")
            titleOfTheProject = str(dico.get("title"))
            message = f"Le projet à été réalisé par: {dico.get('author').get('username')}"
            embed = discord.Embed(title=titleOfTheProject, description=message, url= f"https://scratch.mit.edu/projects/{id}", color=color)
            url = f"https://cdn2.scratch.mit.edu/get_image/project/{id}_480x360.png"
            embed.set_thumbnail(url=url)
            await channel.send(embed=embed)
            number += 1


@bot.command()
async def search(ctx, *searched):
    searched = " ".join(searched)
    searched = str(searched)
    numberMax = 5
    number = 0
    search = login.search_projects(mode="popular", search=searched)
    while number < numberMax:
        try:
            color = get_color(ctx.message.guild.id)
            langue = get_language(ctx.message.guild.id)
        except:
            print("error")
            langue = "fr"
            color = 0xFFAAAA
            pass
        dico=search[number]
        id = dico.get("id")
        message = f"Le projet à été réalisé par: {dico.get('author')}"
        titleOfTheProject = dico.get("author")
        embed = discord.Embed(title=titleOfTheProject,
                              description=message,
                              url=f"https://scratch.mit.edu/projects/{id}",
                              color=color)
        url = f"https://cdn2.scratch.mit.edu/get_image/project/{id}_480x360.png"
        project = login.connect_project(project_id=id)
        stats = project.stats()
        love_count = stats.get("loves")
        fave_count = stats.get("favorites")
        view_count = stats.get("views")
        remix_count = stats.get("remixes")
        print(remix_count + "/" + view_count + "/")
        embed.add_field(name="Nombre de loves", value=love_count, inline=True)
        embed.add_field(name="Nombre de favoris",
                        value=fave_count,
                        inline=True)
        embed.add_field(name="Nombre de remix", value=remix_count, inline=True)
        embed.add_field(name="Nombre de vues", value=view_count, inline=True)
        embed.set_thumbnail(url=url)
        await ctx.send(embed=embed)
        number += 1


@bot.command()
async def say(ctx, *to_say):
    if ctx.message.author.id == 809521544706654208:
        try:
            langue = get_language(ctx.message.guild.id)
            color = get_color(ctx.message.guild.id)
        except:
            print("error")
            langue = "fr"
            color = 0xFFAAAA
        print(color)
        message = " ".join(to_say)
        await ctx.message.delete()
        message = t(message, langue)
        embed = discord.Embed(description=message, color=color)
        await ctx.send(embed=embed)


@bot.command()
async def unconnect(ctx):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    ###embed=discord.Embed(title="Vérification", description=f"Êtes vous sur de vouloir délier votre compte Scratch et votre compte Discord?")
    ####await ctx.send(embed=embed)

    ##def check_button(msg):
    #return res.channel == ctx.channel

    #res = await bot.wait_for("button click", check=check_button)
    user_id = ctx.author.id
    print(user_id)
    file = open("connexions.json", "r")
    content = file.read()
    content = content[:-1]
    file.close()
    print(content)
    if str(user_id) in content:
        pos1 = content.find(str(user_id))
        pos2 = pos1
        pos2 += len(str(user_id))
        pos2 += 3
        name = get_scratch_profile(user_id, content)
        pos2 += len(name)
        pos2 += 2
        pos1 -= 1
        to_delete = content[pos1:pos2]
        content = content.replace(to_delete, "")
        print(content)
        file = open("connexions.json", "w")
        file.write(content)
        file.write("}")
        file.close
        embed = discord.Embed(
            title="Délié",
            description=
            f"Votre compte Discord à été delié de votre compte Scratch avec succès",
            color=color)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Pas lié",
            description=
            f"Votre compte Discord n'est pas lié a un compte Scratch",
            color=color)
        await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True, manage_guild=True)
async def embed(ctx, arg, desc, desc_value=None, title=None, title_value=None):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if arg == "color":
        code = desc
        if code.lower() == "red" or code.lower() == "rouge":
            code = "0xFF0000"
        if code.lower() == "green" or code.lower() == "vert":
            code = "0x00FF00"
        if code.lower() == "blue" or code.lower() == "bleu":
            code = "0x0000FF"
        if code.lower() == "orange":
            code = "0xFF8F00"
        if code.lower() == "yellow":
            code = "0xFFFF00"
        if code.lower() == "purple":
            code = "0x8800FF"
        if code.lower() == "pink":
            code = "0xFF00FF"
        if code.lower() == "black":
            code = "0x000000"
        if code.lower() == "white":
            code = "0xFFFFFF"
        if code.lower() == "random":
            code = "0xrandom"
        if len(code) == 6:
            code = f"0x{code}"
        print(code)
        if not "0x" in str(code) or not len(code) == 8:
            color = get_color(ctx.message.guild.id)
            embed = discord.Embed(
                title="Error",
                description=
                "Veuillez rentrer une couleur existante ou un code héxadécimal",
                color=color)
            await ctx.send(embed=embed)
            return
        print("Code is ok")
        file = open("embed_color.json", "r")
        content = file.read()
        content = content[:-1]
        file.close()
        print(content)
        guild_id = ctx.message.guild.id
        if str(guild_id) in content:
            print("remove")
            pos1 = content.find(str(guild_id))
            pos2 = pos1
            pos2 += len(str(guild_id))
            pos1 -= 1
            i = 0
            while not i == 3:
                if content[pos2] == '"':
                    i += 1
                pos2 += 1
            pos2 += 1
            print(content[pos1:pos2])
            to_remove = content[pos1:pos2]
            content = content.replace(to_remove, "")
            print(content)
        file = open("embed_color.json", "w")
        if not "{" in content:
            file.write("{")
        file.write(f'{content}"{guild_id}":"{code}",')
        file.write("}")
        file.close()
        color = get_color(guild_id)
        embed = discord.Embed(
            title="Couleur changée",
            description=f"La couleur des embeds pour ce serveur à été changée",
            color=color)
        await ctx.send(embed=embed)
    if arg == "set":
        if desc == "desc:":
            message = desc_value
        else:
            await ctx.send(
                "Veuillez rentrer une description comme ceci: `s!embed set desc: 'Truc'`"
            )
        if title == "title:":
            await ctx.message.delete()
            embed = discord.Embed(title=title_value,
                                  description=message,
                                  color=color)
        else:
            await ctx.message.delete()
            embed = discord.Embed(description=message, color=color)
        await ctx.send(embed=embed)
    else:
        await ctx.end("Cette commande n'existe pas")


@bot.command()
@commands.has_permissions(administrator=True, manage_guild=True)
async def langue(ctx, arg):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if arg != "en" and arg != "fr":
        embed = discord.Embed(
            title="Error",
            description="Please use a valid language ('fr' or 'en')",
            color=color)
        await ctx.send(embed=embed)
        return
    code = arg
    print("Language is ok")
    file = open("langue.json", "r")
    content = file.read()
    content = content[:-1]
    file.close()
    print(content)
    guild_id = ctx.message.guild.id
    if str(guild_id) in content:
        print("remove")
        pos1 = content.find(str(guild_id))
        pos2 = pos1
        pos2 += len(str(guild_id))
        pos1 -= 1
        i = 0
        while not i == 3:
            if content[pos2] == '"':
                i += 1
            pos2 += 1
        pos2 += 1
        print(content[pos1:pos2])
        to_remove = content[pos1:pos2]
        content = content.replace(to_remove, "")
        print(content)
    file = open("langue.json", "w")
    if not "{" in content:
        file.write("{")
    file.write(f'{content}"{guild_id}":"{code}",')
    file.write("}")
    file.close()
    langue = get_language(ctx.message.guild.id)
    embed = discord.Embed(
        title=t("Langue changée", langue),
        description=t("La langue des messages pour ce serveur à été changée",
                      langue),
        color=color)
    await ctx.send(embed=embed)


@bot.command()
async def connect(ctx):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    user_id = ctx.author.id
    print(user_id)
    file = open("connexions.json", "r")
    content = file.read()
    content = content[:-1]
    file.close()
    print(content)
    user_id = str(user_id)
    if user_id in content:
        name = get_scratch_profile(user_id, content)
        user = login.connect_user(username=name)
        embed = discord.Embed(
            title="Déjà lié",
            description=
            f"Votre compte Discord déjà lié a un compte Scratch ({name})",
            color=color)
        url = f"https://cdn2.scratch.mit.edu/get_image/user/{user.id()}_500x500.png"
        embed.set_thumbnail(url=url)
        await ctx.send(embed=embed)
        return
    length_of_string = 40
    code = ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length_of_string))
    embed = discord.Embed(
        title="Lier un compte",
        description=
        f"Copiez ce texte: ||`{code}`|| \nici: https://scratch.mit.edu/projects/624492915/ pour lier votre compte \nEnsuite, entrez 'Done' sur le serveur ou vous avez fait la commande",
        color=color)
    await ctx.author.send(embed=embed)

    embed = discord.Embed(
        title="Lier un compte",
        description=
        f'Allez voir en message privé les instructions envoyées puis revenez ici et tapez "Done"',
        color=color)
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content == "Done"

    try:
        done = await bot.wait_for("message", timeout=120, check=check)
        stats = requests.get(
            "https://api.scratch.mit.edu/users/___Scratch-FR___/projects/624492915/comments/?limit=1"
        )
        stats = stats.json()
        print(stats)
        print(stats[0]["content"])
        print(stats[0]["author"]["username"])
        content = stats[0]["content"]
        name = stats[0]["author"]["username"]
        try:
            if code == content or ctx.author.id == 809521544706654208:
                user_id = ctx.author.id
                print(user_id)
                file = open("connexions.json", "r")
                content = file.read()
                content = content[:-1]
                file.close()
                print(content)
                user_id = str(user_id)
                if user_id in content:
                    embed = discord.Embed(
                        description=
                        f"Tu as déjà lié ton compte, fait s!unconnect pour te délier avec",
                        color=color)
                    await ctx.send(embed=embed)
                else:
                    file = open("connexions.json", "w")
                    if not "{" in content:
                        file.write("{")
                    file.write(f'{content}"{user_id}":"{name}",')
                    file.write("}")
                    file.close()
                    embed = discord.Embed(
                        description=
                        f"Votre compte Discord et votre compte Scratch ont été liés avec succés!",
                        color=color)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=
                    f"Merci rentrer le code correctement, de rentrer le bon et d'écrire 'Done' après",
                    color=color)
                await ctx.send(embed=embed)
            return
        except:
            embed = discord.Embed(
                description="Désolé, cette commande est en développement",
                color=color)
            await ctx.send(embed=embed)
    except:
        embed = discord.Embed(description=f"Vous avez été trop long!",
                              color=color)
        await ctx.send(embed=embed)


@bot.command()
async def profile(ctx, name=None):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
        pass
    if name == None:
        print("search name")
        file = open("connexions.json", "r")
        print("file opened")
        content = file.read()
        user_id = ctx.author.id
        print(content)
        print(user_id)
        if str(user_id) in content:
            name = get_scratch_profile(user_id, content)
        else:
            embed = discord.Embed(
                title="Compte introuvable",
                description=
                "Veuillez s'il vous plait spécifier un nom d'utilisateur valide ou lier votre compte scratch en utilisant la commande `s!connect`!",
                color=color)
            await ctx.send(embed=embed)
            name = "a"
        file.close()
    else:
        if "<@" in name:
            name = name.replace("<@", "")
            name = name.replace(">", "")
            name = name.replace("!", "")
            user_id = name
            file = open("connexions.json", "r")
            content = file.read()
            file.close
            name = get_scratch_profile(user_id, content)
        elif "`" in name:
            name = name.replace("`", "")
    print(f"Loading {name} profile...")
    user = login.connect_user(username=name)
    id = user.id()
    print(id)
    url = f"https://cdn2.scratch.mit.edu/get_image/user/{id}_500x500.png"
    bio = user.bio()
    print(f"({bio})")
    desc = user.work()
    print(f"({desc})")
    followers = get_followers(name)
    print(followers)
    message = f"Followers: **{followers}**"
    embed = discord.Embed(title=f"`{name}`",
                          description=message,
                          url=f"https://scratch.mit.edu/users/{name}/",
                          color=color)
    embed.set_thumbnail(url=url)
    print("Load bio and desc")
    if not len(bio) < 3:
        embed.add_field(name="A propos de moi", value=bio, inline=True)
    else:
        embed.add_field(name="A propos de moi",
                        value="Données inexistantes",
                        inline=True)
        print("bio inexistante")
    if not len(desc) < 3:
        embed.add_field(name="Ce que je fais", value=desc, inline=True)
    else:
        embed.add_field(name="Ce que je fais",
                        value="Données inexistantes",
                        inline=True)
        print("description inexistante")
    try:
        user = login.connect_user(username=name)
        user.update_data()
        embed.add_field(name="Nombre de messages:",
                        value=user.messages_count(),
                        inline=True)
        liste = user.joined_date().replace('Z', '').replace('T',
                                                            ' à ').split("T")
        string = " ".join(liste)
        embed.add_field(name="A rejoint le:", value=string, inline=True)
        embed.add_field(name="Pays:", value=user.country(), inline=True)
        user = login.connect_user(username=name)
        user.update_data()
        embed.add_field(name="Satut:", value=user.status(), inline=True)
        embed.add_field(name="Nombre de vues:",
                        value=user.total_views_count(),
                        inline=False)
        embed.add_field(name="Nombre de loves:",
                        value=user.total_loves_count(),
                        inline=True)
        embed.add_field(name="Nombre de favoris:",
                        value=user.total_favourites_count(),
                        inline=True)
    except:
        print("ERROR with ScratchConnect")
        pass
    await ctx.send(embed=embed)
    print("Profile loaded!")


@profile.error
async def profile_error(ctx, error):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
        pass
    embed = discord.Embed(
        title="Erreur",
        description=
        "Ce compte Scratch n'existe pas ou l'utilisateur discord n'a pas lier son compte",
        color=color)
    await ctx.send(embed=embed)


@bot.command()
async def follow(ctx, name=None):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if name == None:
        file = open("connexions.json", "r")
        content = file.read()
        user_id = ctx.author.id
        if str(user_id) in content:
            name = get_scratch_profile(user_id, content)
        else:
            embed = discord.Embed(
                title="Compte introuvable",
                description=
                "Veuillez s'il vous plait lier votre compte scratch en utilisant la commande `s!connect`!",
                color=color)
            await ctx.send(embed=embed)
            return
        file.close()
    else:
        embed = discord.Embed(
            title="Impossible",
            description=
            "Vous ne pouvez pas demander que je ne suive plus quelqu'un d'autre que vous",
            color=color)
        await ctx.send(embed=embed)
        return
    
    user = login.connect_user(username=name)
    url = f"https://cdn2.scratch.mit.edu/get_image/user/{user.id()}_500x500.png"
    user.follow_user(username=name)
    if (user.id()):
        if (user.id() > 0):
            embed = discord.Embed(
                title="Vous avez été suivi!",
                description=f"Cet utilisateur ({name}) a bien été suivi",
                color=color)
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Vous avez été suivi!",
                description=f"Cet utilisateur ({name}) n'existe pas",
                color=color)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Vous avez été suivi!",
            description=f"Cet utilisateur ({name}) n'existe pas",
            color=color)
        await ctx.send(embed=embed)


@follow.error
async def follow_error(ctx, error):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    embed = discord.Embed(
        title="Erreur",
        description="Cette commande est en développement, veuillez m'excuser",
        color=color)
    await ctx.send(embed=embed)


@bot.command()
async def unfollow(ctx, name=None):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if name == None:
        file = open("connexions.json", "r")
        content = file.read()
        user_id = ctx.author.id
        if str(user_id) in content:
            name = get_scratch_profile(user_id, content)
        else:
            embed = discord.Embed(
                title="Compte introuvable",
                description=
                "Veuillez s'il vous plait lier votre compte scratch en utilisant la commande `s!connect`!",
                color=color)
            await ctx.send(embed=embed)
            return
        file.close()
    else:
        embed = discord.Embed(
            title="Impossible",
            description=
            "Vous ne pouvez pas demander que je ne suive plus quelqu'un d'autre que vous",
            color=color)
        await ctx.send(embed=embed)
        return

    user = login.connect_user(username=name)
    url = f"https://cdn2.scratch.mit.edu/get_image/user/{user.id()}_500x500.png"
    user.unfollow_user(username=name)
    if (user.id()):
        if (user.id() > 0):
            embed = discord.Embed(
                title="Vous n'êtes plus suivi",
                description=f"Cet utilisateur ({name}) n'est plus suivi",
                color=color)
            embed.set_thumbnail(url=url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Vous n'êtes plus suivi",
                description=f"Cet utilisateur ({name}) n'existe pas",
                color=color)
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Vous n'êtes plus suivi",
            description=f"Cet utilisateur ({name}) n'existe pas",
            color=color)
        await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    try:
        color = get_color(ctx.message.guild.id)
        langue = get_language(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Cette commande n'existe pas")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Il manque un argument")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "Vous n'avez pas les permissions pour utiliser cette commande")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Vous ne pouvez pas utiliser cette commande")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("Désolé, je ne peux pas faire ça")
    elif isinstance(error, commands.UserNotFound):
        await ctx.send("L'utilisateur n'a pas été trouvé")


@bot.command()
async def tendances(ctx):
    number = 0
    numberMax = 10
    trendings = login.explore_projects(mode="trending", query="*")
    while number < numberMax:
        try:
            langue = get_language(ctx.message.guild.id)
            color = get_color(ctx.message.guild.id)
        except:
            print("error")
            langue = "fr"
            color = 0xFFAAAA
        dico=trendings[number]
        id = dico.get("id")
        titleOfTheProject = str(dico.get("title"))
        message = f"Le projet à été réalisé par: {dico.get('author').get('username')}"
        embed = discord.Embed(title=titleOfTheProject, description=message, url= f"https://scratch.mit.edu/projects/{id}", color=color)
        url = f"https://cdn2.scratch.mit.edu/get_image/project/{id}_480x360.png"
        embed.set_thumbnail(url=url)
        await ctx.send(embed=embed)
        number += 1


@bot.command()
async def serverInfo(ctx):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfVoiceChannels = len(server.voice_channels)
    serverDescription = server.description
    numberOfPerson = server.member_count
    serverName = server.name
    if (serverDescription != None):
        embed = discord.Embed(
            description=
            f"Le serveur __**{serverName}**__ contient **{numberOfPerson}** personnes. \nLa description du serveur est: {serverDescription}. \nCe serveur possède {numberOfTextChannels} salons textuels ainsi que {numberOfVoiceChannels} salons vocaux",
            color=color)
    else:
        embed = discord.Embed(
            description=
            f"Le serveur __**{serverName}**__ contient **{numberOfPerson}** personnes. \nCe serveur possède {numberOfTextChannels} salons textuels ainsi que {numberOfVoiceChannels} salons vocaux",
            color=color)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, nombre: int):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    messages = await ctx.channel.purge(limit=nombre + 1)
    if nombre > 1:
        embed = discord.Embed(description=nombre +
                              t(" messages were deleted", langue),
                              color=color)
        print("many messages deleted")
    else:
        embed = discord.Embed(description=nombre +
                              t(" message was deleted", langue),
                              color=color)
        print("1 message deleted")
    await ctx.send(embed=embed, delete_after=5)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *reason):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    reason = " ".join(reason)
    await ctx.guild.kick(user, reason=reason)
    embed = discord.Embed(
        title=user + t(" à été expulsé", langue),
        description=t("L'utilisateur ", langue) + user +
        t(" à été expulsé de ce serveur avec succès", langue),
        color=color)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def bann(ctx, user: discord.User, *reason):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    reason = " ".join(reason)
    embed = discord.Embed(title=user + t(" à été banni", langue),
                          description=t("L'utilisateur ", langue) + user +
                          t(" à été banni de ce serveur avec succès", langue),
                          color=color)
    await ctx.guild.ban(user, reason=reason)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(ban_members=True)
async def unbann(ctx, user, *reason):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    try:
        reason = " ".join(reason)
        userName, userId = user.split("#")
        bannedUsers = await ctx.guild.bans()
        for i in bannedUsers:
            if i.user.name == userName and i.user.discriminator == userId:
                embed = discord.Embed(
                    title=user + t(" à été débanni", langue),
                    description=t("L'utilisateur ", langue) + user +
                    t(" à été débanni de ce serveur avec succès", langue),
                    color=color)
                await ctx.guild.unban(i.user, reason=reason)
                await ctx.send(embed=embed)
                return
    except:
        embed = discord.Embed(
            description=t("L'utilisateur ", langue) + user +
            t(" n'est pas banni, je ne peux pas le débannir", langue),
            color=color)
        await ctx.send(embed=embed)


@bot.command()
async def Leaderboard(ctx, arg=None):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if arg == None:
        arg = "followers"
    arg = arg.lower()
    if arg == "followers" or arg == "views" or arg == "view" or arg == "loves" or arg == "favorites" or arg == "favorite" or arg == "love" or arg == "follower" or arg == "fave" or arg == "faves" or arg == "f" or arg == "v" or arg == "l" or arg == "comments" or arg == "comment" or arg == "c" or arg == "vues" or arg == "favoris" or arg == "commentaires":
        print("Good argument")
        if arg == "follower":
            arg = "followers"
        if arg == "view" or arg == "v" or arg == "vues":
            arg = "views"
        if arg == "love" or arg == "l":
            arg = "loves"
        if arg == "fave" or arg == "faves" or arg == "favorite" or arg == "f" or arg == "favoris":
            arg = "favorites"
        if arg == "comment" or arg == "c" or arg == "commentaires":
            arg = "comments"

    else:
        embed = discord.Embed(
            title=t("Bad argument", langue),
            description=t(
                "Retry with one of the following arguments: followers, views, loves, favorites",
                langue),
            color=color)
        await ctx.send(embed=embed)
        return
    arg = arg.lower()
    id_list = []
    scratch_name_list = []
    value_list = []
    server_id = ctx.message.guild.id
    guild = bot.get_guild(server_id)
    print(server_id)
    print(guild)
    file = open("connexions.json", "r")
    content = file.read()
    file.close()
    dico = {}
    x = 0
    pos1 = 2
    while x == 0:
        i = 0
        pos2 = pos1
        while i == 0:
            if content[pos2] == '"':
                i = 1
            else:
                pos2 += 1
        id = content[pos1:pos2]
        i = 0
        pos1 = pos2
        pos1 += 3
        pos2 = pos1
        while i == 0:
            if content[pos2] == '"':
                i = 1
            else:
                pos2 += 1
        scratch_name = content[pos1:pos2]
        pos1 = pos2
        pos1 += 3
        print(id)
        id = int(id)
        print(scratch_name)
        print(guild.get_member(id))
        if guild.get_member(id) is not None:
            username = scratch_name
            print(username)
            data = requests.get(
                f"https://scratchdb.lefty.one/v3/user/info/{username}")
            data = data.json()
            data = str(data)
            print(data)
            print(arg)
            pos1_1 = data.rfind(arg)
            if pos1_1 == -1:
                print("error")
                count = 0
            else:
                iii = 0
                while iii == 0:
                    pos1_1 += 1
                    if data[pos1_1] == ":":
                        iii = 1
                        pos1_1 += 1
                pos2_1 = pos1_1
                iii = 0
                while iii == 0:
                    pos2_1 += 1
                    if data[pos2_1] == ",":
                        iii = 1
                        pos2 -= 1
                count = int(data[pos1_1:pos2_1])
            if arg == "followers" or arg == "follower":
                followers = int(get_followers(scratch_name))
                print(followers)
                if followers > count:
                    if arg == "followers" or arg == "follower":
                        count = followers
            if count > 1:
                dico[f"{scratch_name}"] = count
                value_list.append(count)
                id_list.append(id)
                scratch_name_list.append(scratch_name)
        if pos1 >= len(str(content)):
            x = 1
    print(id_list)
    print(scratch_name_list)
    print(value_list)
    print(dico)
    sorted_list = list(reversed(sorted(dico.items(), key=lambda t: t[1])))
    if len(sorted_list) > 10:
        del sorted_list[10:len(sorted_list)]
    print(sorted_list)
    i = 0
    count = 0
    scratch_name_list = []
    value_list = []
    id_list = []
    file = open("connexions.json", "r")
    content = file.read()
    file.close()
    while not count == len(sorted_list):
        data = str((sorted_list[count]))
        pos1 = 2
        pos2 = data.rfind("'")
        scratch_name = data[pos1:pos2]
        scratch_name_list.append(data[pos1:pos2])
        pos1 = data.rfind("'")
        pos1 += 3
        pos2 = len(data)
        pos2 -= 1
        value_list.append(data[pos1:pos2])
        user_id = get_discord_id_with_scratch_username(scratch_name, content)
        print(count)
        id_list.append(user_id)
        count += 1
    print(scratch_name_list)
    print(id_list)
    print(value_list)
    arg = arg.upper()
    embed = discord.Embed(title=f"__{arg} LEADERBOARD__", color=color)
    count = 0
    while not count == len(sorted_list):
        url = f"https://scratch.mit.edu/users/{scratch_name_list[count]}"
        user_id = id_list[count]
        if count == 0:
            embed.add_field(
                name=f"🥇",
                value=
                f">>> [{scratch_name_list[count]}]({url}) / <@!{user_id}>: \n {value_list[count]}",
                inline=False)
        elif count == 1:
            embed.add_field(
                name=f"🥈",
                value=
                f">>> [{scratch_name_list[count]}]({url}) / <@!{user_id}>: \n {value_list[count]}",
                inline=False)
        elif count == 2:
            embed.add_field(
                name=f"🥉",
                value=
                f">>> [{scratch_name_list[count]}]({url}) / <@!{user_id}>: \n {value_list[count]}",
                inline=False)
        else:
            embed.add_field(
                name=f"#{count+1}",
                value=
                f">>> [{scratch_name_list[count]}]({url}) / <@!{user_id}>: \n {value_list[count]}",
                inline=False)
        count += 1
    embed.set_footer(text=t(
        "Si ton compte n'apparait pas, n'hésite pas a utiliser s!connect pour qu'il y apparaisse",
        langue))
    await ctx.send(embed=embed)


@bot.command()
async def LoveAndFave(ctx, id):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if "scratch.mit.edu" in id:
        if "projects" in id:
            pos1 = id.find('projects/')
            pos1 += 9
        else:
            pos1 = id.find('project/')
            pos1 += 8
        pos2 = len(id)
        if id[pos2 - 1:pos2] == "/":
            pos2 -= 1
        id = id[pos1:pos2]
        print(id)
    project = login.connect_project(project_id=id)
    project.love()
    project.favourite()
    title = project.title()
    embed = discord.Embed(title=t("Loved and faved", langue),
                          description=t("The project ", langue) + title +
                          t(" has been successfully liked and faved", langue),
                          color=color)
    url = f"https://cdn2.scratch.mit.edu/get_image/project/{id}_480x360.png"
    embed.set_thumbnail(url=url)
    await ctx.send(embed=embed)


@LoveAndFave.error
async def LoveAndFave_error(ctx, error):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(t("There is a missing argument", langue))
    else:
        embed = discord.Embed(description=t(
            "Please type a valid project id/link (ex: s!LoveAndFave 598683067)",
            langue),
                              color=color)
        await ctx.send(embed=embed)


@bot.command()
async def Project(ctx, id):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if "scratch.mit.edu" in id:
        if "project/" in id:
            pos1 = id.find('project/')
            pos1 += 8
        else:
            pos1 = id.find('projects/')
            pos1 += 9
        pos2 = len(id)
        if id[pos2 - 1:pos2] == "/":
            pos2 -= 1
        id = id[pos1:pos2]
        print(id)
    data = requests.get(f"https://scratchdb.lefty.one/v3/project/info/{id}")
    data = data.json()
    print(data)
    url = f"https://cdn2.scratch.mit.edu/get_image/project/{id}_480x360.png"
    project = login.connect_project(project_id=id)
    stats =project.stats()
    love_count = stats.get("loves")
    fave_count = stats.get("favorites")
    view_count = stats.get("views")
    remix_count = stats.get("remixes")
    title = project.title()
    embed = discord.Embed(title=title,
                          description=t("Stats of the project:", langue),
                          url=f"https://scratch.mit.edu/project/{id}",
                          color=color)
    embed.add_field(name=t("Loves count", langue),
                    value=love_count,
                    inline=True)
    embed.add_field(name=t("Faves count", langue),
                    value=fave_count,
                    inline=True)
    embed.add_field(name=t("Remixes count", langue),
                    value=remix_count,
                    inline=True)
    embed.add_field(name=t("Views count", langue),
                    value=view_count,
                    inline=True)
    embed.set_thumbnail(url=url)
    await ctx.send(embed=embed)


@Project.error
async def Project_error(ctx, error):
    try:
        langue = get_language(ctx.message.guild.id)
        color = get_color(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("There is a missing argument")
    else:
        embed = discord.Embed(
            description=
            "Please type a valid project id/link (ex: s!project 598683067)",
            color=color)
        await ctx.send(embed=embed)


@bot.command()
async def help(ctx, arg=None):
    try:
        color = get_color(ctx.message.guild.id)
        langue = get_language(ctx.message.guild.id)
    except:
        print("error")
        langue = "fr"
        color = 0xFFAAAA
    if arg == None:
        embed = discord.Embed(title=t("Menu d'aide", langue),
                              description=t("List of the commands groups",
                                            langue),
                              color=color)
        embed.add_field(name=t("Scratch help", langue),
                        value="s!help scratch",
                        inline=False)
        embed.add_field(name=t("Moderation help", langue),
                        value="s!help mod",
                        inline=False)
        await ctx.send(embed=embed)
    elif arg == "scratch":
        embed = discord.Embed(title=t("Help menu", langue),
                              description=t(
                                  "List of commands related to Scratch",
                                  langue),
                              color=color)
        embed.add_field(
            name="s!connect",
            value=t("Link your Scratch account and your Discord account",
                    langue),
            inline=False)
        embed.add_field(name="s!tendances",
                        value=t("Display the trendings", langue),
                        inline=False)
        embed.add_field(name="s!profile [ScratchPseudo]",
                        value=t("Display a profile", langue),
                        inline=False)
        embed.add_field(name="s!project [Lien]",
                        value=t("Display the stats of a project", langue),
                        inline=False)
        embed.add_field(name="s!follow",
                        value=t("Follow you", langue),
                        inline=False)
        embed.add_field(name="s!unfollow",
                        value=t("Unfollow you", langue),
                        inline=False)
        embed.add_field(name="s!LoveAndFave [Lien]",
                        value=t("Like and fave a project", langue),
                        inline=False)
        embed.add_field(
            name="s!search [Nom]",
            value=t("Display the 5 first scratch results for the search",
                    langue),
            inline=False)
        embed.add_field(
            name="s!leaderboard [Views/Followers/Loves/Favorites/Comments]",
            value=t(
                "Display a list of the first 10 person on the server per category",
                langue),
            inline=False)
        await ctx.send(embed=embed)
    elif arg == "mod":
        embed = discord.Embed(title=t("Help menu", langue),
                              description=t(
                                  "List of commands related to the moderation",
                                  langue),
                              color=color)
        embed.add_field(name="s!clear [Nombre]",
                        value=t("Clear messages", langue),
                        inline=False)
        embed.add_field(name="s!kick [Mention]",
                        value=t("Kick a user of the server", langue),
                        inline=False)
        embed.add_field(name="s!ban [Mention]",
                        value="Ban a user of the server",
                        inline=False)
        embed.add_field(name="s!unban [Identifiant]",
                        value="Unban a user of the server",
                        inline=False)
        embed.add_field(name="s!embed color [Color/hexadecimal code]",
                        value="Change the embed color for the server",
                        inline=False)
        embed.add_field(
            name='s!embed set desc: "[description]" title: "[Title]"',
            value="Create an embed",
            inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Help menu",
                              description="This help menu doesn't exist",
                              color=color)


bot.run("OTExOTU4NTA1Nzk4Mzk3OTcz.YZo9iw.8ijtONIA8_QClbONQUzB6JFDmLU")
