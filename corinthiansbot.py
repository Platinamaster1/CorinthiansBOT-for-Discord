# Corinthians BOT em Python
# Enzo Furegatti Spinella - 19168 - 2021
import os
import random

import discord
from discord.ext import commands
from asyncio import sleep
#from dotenv import load_dotenv

#load_dotenv()
#TOKEN = os.getenv('DISCORD_TOKEN')
#GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='>')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

#@bot.command(name='99')
#async def nine_nine(ctx):
#    brooklyn_99_quotes = [
#        'I\'m the human form of the 💯 emoji.',
#        'Bingpot!',
#        (
#            'Cool. Cool cool cool cool cool cool cool, '
#            'no doubt no doubt no doubt no doubt.'
#        ),
#    ]
#
#    response = random.choice(brooklyn_99_quotes)
#    await ctx.send(response)

@bot.command(name='palmeiras', help='51 é nome de Cachaça :P')
async def palmeiras(ctx):
    response = '🎵🎶O palmeiras não tem mundial\nPalmeiras não tem mundial\nNão tem copinha, não tem mundial\nNão tem copinha, não tem mundial\n\nO palmeiras não tem mundial\nPalmeiras não tem mundial\nNão tem copinha, não tem mundial\nNão tem copinha, não tem mundial🎶🎵'
    canal = ctx.author.voice.channel
    await canal.connect()
    vc = bot.voice_clients[0]
    await ctx.send(response)
    audio = discord.FFmpegPCMAudio('palmeiras.mp4')
    vc.play(audio)
    while vc.is_playing():
        await sleep(1)
    await vc.disconnect()

@bot.command(name='hino', help='Toca-se o Maior e Mais belo hino de todos!')
async def hino(ctx):
    canal = ctx.author.voice.channel
    await canal.connect()
    vc = bot.voice_clients[0]
    audio = discord.FFmpegPCMAudio('hino.mp4')
    vc.play(audio)
    while vc.is_playing():
        await sleep(1)
    await vc.disconnect()
    

#@bot.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.errors.CommandInvokeError):
#        await ctx.send('Você precisa estar em um Canal!')

#@bot.command(name='roll_dice', help='Simulates rolling dice.')
#async def roll(ctx, number_of_dice: int, number_of_sides: int):
#    dice = [
#        str(random.choice(range(1, number_of_sides + 1)))
#        for _ in range(number_of_dice)
#    ]
#    await ctx.send(', '.join(dice))




    #elif message.content == 'raise-exception':
    #    raise discord.DiscordException

#@bot.event
#async def on_error(event, *args, **kwargs):
#    with open('err.log', 'a') as f:
#        if event == 'on_message':
#            f.write(f'Unhandled message: {args[0]}\n')
#        else:
#            raise
#client.run(TOKEN)
bot.run('ODMwNTYyMzYzMDMwNjM0NDk3.YHIfeg.I1U-FfDDkrjRdXlqcx--KwtY85o')
