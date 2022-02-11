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

    @client.command(pass_content=True)
    async def spam(ctx, member):
        member = int(member.replace('<@!', "").replace('>', ""))
        print(member)
        # members = guild.members
        # rand = random.choice(members)
        rand = client.get_user(member)
        dm_channel = await rand.create_dm()
        rand_cont = random.choice(ha)
        await dm_channel.send(rand_cont)

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
        if re.search('kyle', content, re.IGNORECASE):
            print("Sending kyle pic...")
            dm = await message.author.create_dm()
            await dm.send(random.choice(kyle_links))


        url = get_fnaf_link(content)
        voice = await play(url, channel, ctx)

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
            if url == None:
                channel = ctx.message.channel
                await channel.send('I can\'t play fnaf right now')
            else:
                scr = discord.FFmpegPCMAudio(url)

                try:
                    voice.play(scr)
                except:
                    await channel.connect()

    @client.command(pass_context=True)
    async def check_perm(ctx, guild_id: int):
        if ctx.message.channel.type == ChannelType.private:
            guild = client.get_guild(guild_id)
            channels = guild.channels
            user_id = ctx.message.author.id
            user = guild.get_member(user_id)

            dm = ctx.message.channel

            all_access = True
            for channel in channels:
                perm = user.permissions_in(channel)
                if perm.view_channel != True:
                    all_access = False
                    await dm.send("You are not able to view " + str(channel.name))

            if all_access:
                await dm.send("You have access to all channels")

    async def audio_player_task():
        while True:
            play_next_song.clear()
            current = await songs.get()
            current.start()
            await play_next_song.wait()

    @client.event
    async def on_ready():
        print("I'm ready!")

run_clients = add_clients(TOKEN)

loop = asyncio.get_event_loop()

loop.run_until_complete( asyncio.wait(run_clients) )

#markiplier .shit