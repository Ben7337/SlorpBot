import asyncio
import datetime
import discord
import random
import re
import time
from discord.ext import commands
from SlorpData import Emotes1
from SlorpData import Emotes2
from SlorpData import FerretList
from SlorpData import TwitchClips
from twitch import TwitchClient
bot = commands.Bot(command_prefix = '$')
role_id = 275412935931723777
role_id2 = 281239235493756928
trash_id = 376542189175570434
ben_id = 198318980321116169
Tclient = TwitchClient(client_id='TWITCH_TOKEN')
myid=82183613
weestid=130924701
global G
G = ""
#--------Bot Start Up--------------
@bot.event
async def on_ready():
    global G
    print('Bot is ready as {}'.format(bot.user))
    G = "Slorping Water"
    game = discord.Game(G)
    await bot.change_presence(status=discord.Status.online, activity=game)
#--------Message responses---------
@bot.event
async def on_message(message):
    channel = message.channel
    if bot.user.id != message.author.id:
        author = message.author        
        if message.content.lower() in Emotes1:            
            with open(Emotes1[message.content.lower()],'rb') as f:
                await channel.send(file=discord.File(f))
        if message.content.lower() in Emotes2:        
            await channel.send(Emotes2.get(message.content.lower()))
        await bot.process_commands(message) #on message fix
#--------$commands---------------------
"""@bot.command() #Rename or just use $help
#async def commands(ctx):
#    com = '$game $updategame [game name]\n $staff $ping $today \n $clips $topclips $date $logout'
#    embed=discord.Embed(title='**Command List **', description=com)        
#    await ctx.send(embed=embed)
"""
#--------Show the Game playing right now------
@bot.command()
async def game(ctx):
    global G
    await ctx.send("Playing: "+G)
#--------Ferret Thing People Wanted---
@bot.command()
@commands.cooldown(1, 3, commands.BucketType.channel)
async def ferret(ctx):
    RandFerret = random.choice(FerretList)
    embed=discord.Embed(title="Here's a ferret!")
    await ctx.send(embed=embed)
    await ctx.send(RandFerret)
#--------Update Game name-------------
@bot.command()
async def updategame(ctx, *args):
    global G
    msg = ctx.message
    author = msg.author
    if role_id in [y.id for y in author.roles]:        
        G = '{}'.format(' '.join(args))
        game = discord.Game(G)
        await bot.change_presence(status=discord.Status.online, activity=game)
        await ctx.send(msg.author.name + ' updated the game to: '+ G)
#---------Staff Test---------------
@bot.command()
async def staff(ctx):
    msg = ctx.message
    if bot.user.id != msg.author.id:
        author = msg.author       
        if role_id2 in [z.id for z in author.roles]:
            await ctx.send("*Admin Test Successful!*")
        elif role_id in [y.id for y in author.roles]:
            await ctx.send("*Mod Test Successful!*")
        else:
            await ctx.send("*Error:* *__Not A Staff Member!__*")
#----------Bot Latency Ping-----------
@bot.command(pass_context=True)
async def ping(ctx):
    embed=discord.Embed(title='**Pong **', description=str(round(bot.latency*1000)), color=0xff5900)        
    await ctx.send(embed=embed)
#----------Clips in History-----------
@bot.command()
async def today(ctx):
    currentDT = datetime.datetime.now()
    Date = currentDT.strftime("%m/%d")
    FullDate = currentDT.strftime("%b %d")
    if Date in TwitchClips:
        embed=discord.Embed(title='**Today In History**', description=FullDate)
        await ctx.send(embed=embed)
        await ctx.send(TwitchClips.get(Date))
    else:
        embed=discord.Embed(title='**Today In History**', description= '*Nothing Here Yet Make Sure Clip Today!* ')
        await ctx.send(embed=embed)
#----------Search up clips by date----
@bot.command()
async def clips(ctx, arg):
    currentDT = datetime.datetime.now()
    if arg in TwitchClips:
        embed=discord.Embed(title='**Clips In History**', description='Date: '+arg)
        await ctx.send(embed=embed)
        await ctx.send(TwitchClips.get(arg))
    else:
        Date = currentDT.strftime("%m/%d")
        embed=discord.Embed(title='**Clips In History**', description= '*Incorrect input.*\n Example for today: '+ Date)
        await ctx.send(embed=embed)
#----------Top Clips Using Twitch Api-
@bot.command()
async def topclip(ctx, arg):
    ClipNum = 1
    if(arg=='day' or arg=='week' or arg=='month' or arg=='all'):
        GetClips = Tclient.clips.get_top('weesterner',None,None,None,ClipNum,arg)
        Found = re.findall(r"https://clips.twitch.tv/[A-z]{6,}", str(GetClips))
        embed=discord.Embed(title='**Top Clip: **'+ arg)
        await ctx.send(embed=embed)
        await ctx.send(' '.join(Found))
    else:
        embed=discord.Embed(title='**Top Clip: **' +arg, description= '*Incorrect input.*\n Use: day, week, month or all')
        await ctx.send(embed=embed) 
#----------Local Date-----------------
@bot.command()
async def date(ctx):
    currentDT = datetime.datetime.now()
    CurrentDate = currentDT.strftime("%A, %B %d, %Y")
    LocalTime = currentDT.strftime("%I:%M %p")
    embed=discord.Embed(title='***Local Date & Time***', description= CurrentDate+'\n'+LocalTime)
    await ctx.send(embed=embed)
#----------Bot kill command-----------
@bot.command(pass_context=True)
async def logout(ctx):
    msg = ctx.message
    if bot.user.id != msg.author.id:
        author = msg.author
        if ben_id == msg.author.id:
            embed=discord.Embed(description='Good Night Chat, I sleep <3')
            await ctx.send(embed=embed)
            await bot.logout()
        else:
            await ctx.send('***Nice try retard***')
bot.run("TOKEN")
