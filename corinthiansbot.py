# Corinthians BOT em Python
# Enzo Furegatti Spinella - 19168 - 2021
import os

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests

import json
import asyncio
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta

import discord
from discord.ext import commands
from asyncio import sleep


bot = commands.Bot(command_prefix='>')
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game('>help'))


@bot.command(pass_context=True)
async def help(ctx):
    async with ctx.channel.typing():
        author = ctx.message.author

        embed = discord.Embed(
            title = "Comandos - CorinthiansBOT",
            color = 0x23272a
        )
        embed.set_thumbnail(url='https://logodownload.org/wp-content/uploads/2016/11/corinthians-logo-02.png')
        embed.add_field(name='>palmeiras', value='"51 é nome de Cachaça" - Toca a FAMIGERADA música que causa pesadelos aos Palmeirenses')
        embed.add_field(name='>hino', value='Toca-se o mais belo e glorioso hino de todos!')
        embed.add_field(name='>elenco', value='Elenco da Temporada atual do Corinthians')
        embed.add_field(name='>ultimas', value='Últimas Notícias do Corinthians')
        desenvolvedor = await bot.fetch_user(307965469653073922)
        embed.set_footer(text=f'Feito por: {desenvolvedor.name}#{desenvolvedor.discriminator}', icon_url=desenvolvedor.avatar_url)
        await ctx.send(embed=embed)


@bot.command(name='palmeiras')
async def palmeiras(ctx):
    if not ctx.message.author.voice:
        await ctx.send("Você não está conectado a um canal de voz!")
    else:
        async with ctx.channel.typing():
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
    if not ctx.message.author.voice:
        await ctx.send("Você não está conectado a um canal de voz!")
    else:
        canal = ctx.author.voice.channel
        await canal.connect()
        vc = bot.voice_clients[0]
        audio = discord.FFmpegPCMAudio('hino.mp4')
        vc.play(audio)
        while vc.is_playing():
            await sleep(1)
        await vc.disconnect()

@bot.command(name='elenco', help='Elenco Atual do Corinthians')
async def elenco(ctx):
    buttons = [u"\u23EA", u"\u25C0", u"\u25B6", u"\u23E9"]
    j_atual = 0
    bot.help_pages = []
    cores = [0xFFFAF0, 0x000000]
    c_indice = 0

    async with ctx.channel.typing():
        p_atual = 1
        p_total = 0
        while True:
            url = f"https://api.promptapi.com/football/players?team=131&season=2021&page={p_atual}"
            payload = {}
            headers= {
                "apikey": "F2nijQKThdYkjTYbYFHEjD5pUicJ8srd"
            }
            response = requests.request("GET", url, headers=headers, data = payload)
            status_code = response.status_code
            data = response.json()
            jogadores = data['response']
            p_total = data['paging']['total']
            for jogador in jogadores:
                
                apelido = jogador['player']['name']
                embedVar = discord.Embed(title=apelido, description="", color=cores[c_indice])
                nome = jogador['player']['firstname'] + ' ' + jogador['player']['lastname']
                idade = jogador['player']['age']
                nacionalidade = jogador['player']['nationality']
                altura = jogador['player']['height']
                peso = jogador['player']['weight']
                foto = jogador['player']['photo']
                posicao = jogador['statistics'][0]['games']['position']

                embedVar.add_field(name="Nome", value=nome, inline=True)
                embedVar.add_field(name="Idade", value=idade, inline=True)
                embedVar.add_field(name="Nacionalidade", value=nacionalidade, inline=True)
                embedVar.add_field(name="Altura", value=altura, inline=True)
                embedVar.add_field(name="Peso", value=peso, inline=True)
                embedVar.add_field(name="Posição", value=posicao, inline=True)
                embedVar.set_image(url=foto)
                embedVar.set_author(name='API-Football - PromptAPI', icon_url='https://assets.promptapi.com/apis/football.png', url='https://promptapi.com/marketplace/description/football-api')
                embedVar.set_thumbnail(url='https://logodownload.org/wp-content/uploads/2016/11/corinthians-logo-02.png')

                embedVar.set_footer(text=f'Responding to: {ctx.message.author.nick}', icon_url=ctx.message.author.avatar_url)
                bot.help_pages.append(embedVar)

                if c_indice == 0:  
                    c_indice = 1
                else:
                    c_indice = 0

            if p_atual == p_total:
                break
            p_atual += 1
            
        msg = await ctx.send(embed=bot.help_pages[j_atual])
        
        for button in buttons:
            await msg.add_reaction(button)
        
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=120.0)

        except asyncio.TimeoutError:
            return await ctx.send("Acabou o Tempo!")

        else:
            j_anterior = j_atual
            if reaction.emoji == u"\u23EA":
                j_atual = 0
                
            elif reaction.emoji == u"\u25C0":
                if j_atual > 0:
                    j_atual -= 1
                    
            elif reaction.emoji == u"\u25B6":
                if j_atual < len(bot.help_pages)-1:
                    j_atual += 1

            elif reaction.emoji == u"\u23E9":
                j_atual = len(bot.help_pages)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if j_atual != j_anterior:
                await msg.edit(embed=bot.help_pages[j_atual])

@bot.command(name='ultimas')
async def ultimas_noticias(ctx):
    async with ctx.channel.typing():
        root = "google.com"
        link = "https://www.google.com/search?q=corinthians&client=opera-gx&hs=ans&source=lnms&tbm=nws&sa=X&ved=2ahUKEwicuN32xIPwAhUqJ7kGHZhtCOAQ_AUoAXoECAEQAw&biw=1639&bih=909"

        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        with requests.Session() as c:
            soup = BeautifulSoup(webpage, 'html5lib')
            for item in soup.find_all('div', attrs={'class': 'ZINbbc xpd O9g5cc uUPGi'}):
                raw_link = (item.find('a', href=True)['href'])
                link = (raw_link.split('/url?q=')[1]).split('&sa=u&')[0]

                title = (item.find('div', attrs={'class': 'BNeawe vvjwJb AP7Wnd'}).get_text())
                description = (item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text())
                author = (item.find('div', attrs={'class': 'BNeawe UPmit AP7Wnd'}).get_text())
                time = description.split("·")[0]
                description = description.split("·")[1]
                #Fazendo o Embed:
                embed = discord.Embed(title=title, description=description, color=discord.Color.orange(), url=link)
                embed.set_author(name=author)
                embed.set_footer(text=time)
                await ctx.send(embed=embed)

@bot.command(name='proximos')
async def proximos_jogos(ctx, proximos):
    async with ctx.channel.typing():
        url = f"https://api.promptapi.com/football/fixtures?team=131&status=NS&season=2021&next={proximos}"
        payload = {}
        headers= {
            "apikey": "F2nijQKThdYkjTYbYFHEjD5pUicJ8srd"
        }
        response = requests.request("GET", url, headers=headers, data = payload)
        status_code = response.status_code
        data = response.json()
        print(data)
        jogos = data['response']
        for jogo in jogos:
            # Jogo
            data = jogo['fixture']['date']
            data = data.split('T')[0]
            data = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')
            arbitro = jogo['fixture']['referee']
            estadio = f"{jogo['fixture']['venue']['city']} - {jogo['fixture']['venue']['name']}"

            # Liga
            logoLiga = jogo['league']['logo']
            nomeLiga = jogo['league']['name']
            rodada = jogo['league']['round']
            temporada = jogo['league']['season']

            # Times
            # Visitante
            nomeTimeV = jogo['teams']['away']['name']
            logoTimeV = jogo['teams']['away']['logo']
            # Mandante
            nomeTimeM = jogo['teams']['home']['name']
            logoTimeM = jogo['teams']['home']['logo']

            # Formatar pro link: url=f'https://futebolplayhd.com/assistir-{nomeTimeM}-x-{nomeTimeV}-ao-vivo-{data}-hd/'
            embedVar = discord.Embed(title=f'{nomeTimeM} x {nomeTimeV}', description="", color=0x000000)
            embedVar.set_author(name='API-Football - PromptAPI', icon_url='https://assets.promptapi.com/apis/football.png', url='https://promptapi.com/marketplace/description/football-api')
            if nomeTimeM == 'Corinthians':
                embedVar.set_thumbnail(url=logoTimeM)
                embedVar.set_image(url=logoTimeV)
            else:
                embedVar.set_thumbnail(url=logoTimeV)
                embedVar.set_image(url=logoTimeM)
            embedVar.set_footer(text=f'{nomeLiga} - {rodada} - {temporada}', icon_url=logoLiga)
            embedVar.add_field(name="Data e Local", value=f'{data} | Local: {estadio}')
            embedVar.add_field(name="Árbitro(a)", value=arbitro)
            await ctx.send(embed=embedVar)
    

   
#bot.run(YOUR_BOT_TOKEN)
