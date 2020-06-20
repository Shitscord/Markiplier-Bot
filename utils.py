import asyncio
import functools
import itertools
import math
import random
import re
import youtube_dl
from async_timeout import timeout

def get_random_link():
    return random.choice(mark_list)

mark = {('fnaf 1',): {'part 1': 'https://www.youtube.com/watch?v=iOztnsBPrAA&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=2&t=0s',
                   'part 2': 'https://www.youtube.com/watch?v=YT1NhLTwwEg&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=3&t=860s',
                   'part 3': 'https://www.youtube.com/watch?v=VXtVrNdD3YA&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=4&t=0s',
                   'part 4': 'https://www.youtube.com/watch?v=l1gQ8VvRszs&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=5&t=0s',
                   '20/20/20': 'https://www.youtube.com/watch?v=s5GfhGFVCFE&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=6&t=0s'},

        ('fnaf 2',): {'part 1': 'https://www.youtube.com/watch?v=60wLvPWXCCc&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=7&t=0s',
                   'part 2': 'https://www.youtube.com/watch?v=_1jDjx089Uw&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=8&t=0s',
                   'part 3': 'https://www.youtube.com/watch?v=9qSJWDK3v8E&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=9&t=0s',
                   'part 4': 'https://www.youtube.com/watch?v=8oeailv2B00&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=10&t=0s',
                   'part 5': 'https://www.youtube.com/watch?v=z3kMFPNELA0&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=11&t=0s',
                   'part 6': 'https://www.youtube.com/watch?v=66sNL_2ztnw&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=12&t=0s',
                   '10/20': 'https://www.youtube.com/watch?v=A9qPj-YJcN8&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=13&t=0s'},

        ('fnaf 3',): {'part 1': 'https://www.youtube.com/watch?v=BB_4BnQe-qc&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=14&t=0s',
                   'part 2': 'https://www.youtube.com/watch?v=a6zmIvT7WZw&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=15&t=0s',
                   'part 3': 'https://www.youtube.com/watch?v=VpQhGsOdHw4&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=16&t=0s',
                   'part 4': 'https://www.youtube.com/watch?v=yR7tP8VgI3M&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=17&t=0s',
                   'part 5': 'https://www.youtube.com/watch?v=YLWfSUG5SNk&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=18&t=0s',
                   'part 6': 'https://www.youtube.com/watch?v=4b0S0S9wUxk&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=19&t=0s',
                   'part 7': 'https://www.youtube.com/watch?v=Av5zGnNPqSo&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=20&t=0s'},

        ('fnaf 4',): {'part 1': 'https://www.youtube.com/watch?v=dlSw0OicMII&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=30&t=0s',
                   'part 2': 'https://www.youtube.com/watch?v=ibCoLMjwJ1g&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=31&t=0s',
                   'part 3': 'https://www.youtube.com/watch?v=7PeDk9LD_Xg&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=32&t=0s',
                   'part 4': 'https://www.youtube.com/watch?v=M7WgoBhF7gc&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=33&t=0s',
                   'part 5': 'https://www.youtube.com/watch?v=AZgnZSmbYn0&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=34&t=0s',
                   'part 6': 'https://www.youtube.com/watch?v=qKlr8NlaQcM&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=35&t=0s',
                   'part 7': 'https://www.youtube.com/watch?v=6AYIfV3JaQk&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=36&t=0s',
                   'part 8': 'https://www.youtube.com/watch?v=vBnw7Ht6gDE&list=PL3tRBEVW0hiDL09lO0xjKEix84OY27xet&index=37&t=0s'},
        }

other = {

        'random': {('fnaf', 'markiplier') : get_random_link},

        'music': {('femmcumming',): 'https://www.youtube.com/watch?v=MwooEU7gn7w', #Bonnie's lullaby
                  ('fix',): 'https://www.youtube.com/watch?v=kXMwZNRiPe0',         #I can't fix you
                  ('michael', '@!420700764223307776', 'mike'): 'https://www.youtube.com/watch?v=Bk_z96dHSPw', #Hallway ambience
                  ('bad',): 'https://www.youtube.com/watch?v=EG757bPPXZQ', #Bad ending
                  ('sissy',): 'https://www.youtube.com/watch?v=598IirIr3rU', #BO1 Monkey
                  ('bite','cum'): 'https://www.youtube.com/watch?v=rLeQSd7R-jU', #Join us for a bite
                  ('sad',): 'https://www.youtube.com/watch?v=cfCRpxklSMQ',
                  ('nigga','nigger'): 'https://www.youtube.com/watch?v=Xb-fH9jLacE'},



        'secret': {('chris',): 'https://www.youtube.com/watch?v=lB2r78KIdsQ',
                   ('brap','fem'): 'https://www.youtube.com/watch?v=fYVLdEKYY2c', #Brap sound
                   ('nightmare',): 'https://www.youtube.com/watch?v=h4JyR7erePw',
                   ('scream', 'scary', 'you won\'t die', 'you wont die'): 'https://www.youtube.com/watch?v=eKyQEbR9tCI'}

        }

def to_list(dict):
    items = []
    for key in list(dict.keys()):
        for item in list(dict[key].items()):
            items.append(item[1])
    return items

def get_max_channel(guild):
    channels = guild.voice_channels

    maxi = [0, None]
    for channel in channels:
        if len(channel.members) > maxi[0]:
            maxi[0] = len(channel.members)
            maxi[1] = channel

    print(maxi[1])
    print(maxi[0])
    return maxi[1]

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

async def get_url(search: str, *, loop: asyncio.BaseEventLoop = None):
    loop = loop or asyncio.get_event_loop()

    partial = functools.partial(ytdl.extract_info, search, download=False, process=False)
    data = await loop.run_in_executor(None, partial)

    if data is None:
        raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

    if 'entries' not in data:
        process_info = data
    else:
        process_info = None
        for entry in data['entries']:
            if entry:
                process_info = entry
                break

        if process_info is None:
            raise YTDLError('Couldn\'t find anything that matches `{}`'.format(search))

    webpage_url = process_info['webpage_url']
    partial = functools.partial(ytdl.extract_info, webpage_url, download=False)
    processed_info = await loop.run_in_executor(None, partial)

    if processed_info is None:
        raise YTDLError('Couldn\'t fetch `{}`'.format(webpage_url))

    if 'entries' not in processed_info:
        info = processed_info
    else:
        info = None
        while info is None:
            try:
                info = processed_info['entries'].pop(0)
            except IndexError:
                raise YTDLError('Couldn\'t retrieve any matches for `{}`'.format(webpage_url))

    return info['url']

def gen_clients(tokens):
    clients = []
    for token in tokens:
        clients.append(commands.Bot(command_prefix = "."))

def get_fnaf_link(message):
    url = None
    for series in list(mark.keys()):
        for keyword in series:
            if re.search(keyword, message, re.IGNORECASE):
                url = list(mark[series].items())[0][1]
                for part in list(mark[series].keys()):
                    if re.search(part, message, re.IGNORECASE):
                        url = mark[series][part]
                        break

    if url != None:
        return url

    else:
        for category in list(other.keys()):
            for keywords in list(other[category].keys()):
                for keyword in keywords:
                    if re.search(keyword, message, re.IGNORECASE):
                        url = other[category][keywords]
                        break
    if callable(url):
        return url()
    else:
        return url



mark_list = to_list(mark)
