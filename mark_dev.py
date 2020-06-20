# Work with Python 3.6
import discord
import youtube_dl
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
from utils import *
import re
import random
from multiprocessing import Process
import asyncio
import copy
import time

songs = asyncio.Queue()
play_next_song = asyncio.Event()

def add_clients(TOKEN):
    clients = []
    for token in TOKEN:
        client = commands.Bot(command_prefix = ".")
        dec_client(client)
        clients.append(client.start(token))

    return clients

def dec_client(client):
    @client.command(pass_context=True)
    async def join(ctx):
        print("Joining...")
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()

    @client.command(pass_context=True)
    async def leave(ctx):
        channel = ctx.message.author.voice.channel
        voice = get(client.voice_clients, guild=ctx.guild)
        await voice.disconnect()

    @client.command(pass_context=True)
    async def stop(ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.stop()

    @client.command(pass_context=True)
    async def resume(ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.resume()

    @client.command(pass_context=True)
    async def pause(ctx):
        voice = get(client.voice_clients, guild=ctx.guild)
        voice.pause()

    @client.event
    async def on_message(message, *args):

        await client.process_commands(message)
        ctx = await client.get_context(message)
        voice = get(client.voice_clients, guild=ctx.guild)

        try:
            channel = message.author.voice.channel
        except:
            channel = get_max_channel(message.guild)

        if voice != None:
            if channel != voice.channel:
                await voice.disconnect()

        content = str(message.content)
        print(content)

        url = get_fnaf_link(content)
        voice = await play(url, channel, ctx)
        #await queue_songs(url, voice)
        print(url)

    def toggle_next():
        client.loop.call_soon_threadsafe(play_next_song.set)

    async def queue_songs(init_url, voice):
        try:
            init_url = mark_list.index(init_url)
        except:
            init_url = mark_list.index(get_random_link())

        for i in range(len(mark_list)-init_url-1):
            scr = await get_url(mark_list[i+init_url+1])
            await songs.put(voice.play(scr, after= toggle_next()))



    async def play(scr, channel, ctx):

        if scr != None:
            try:
                voice = await channel.connect()
            except:
                voice = get(client.voice_clients, guild=ctx.guild)
                voice.stop()

            url = await get_url(scr)
            scr = discord.FFmpegPCMAudio(url)
            voice.play(scr, after= toggle_next())
        else:
            return ('Failed...')
        return voice

    async def audio_player_task():
        while True:
            play_next_song.clear()
            current = await songs.get()
            current.start()
            await play_next_song.wait()

    @client.event
    async def on_ready():
        print("cummy FUCK")

run_clients = add_clients(TOKEN)

loop = asyncio.get_event_loop()

for i, token in enumerate(TOKEN):
    loop.run_until_complete( asyncio.wait(run_clients) )

#loop.run_forever()