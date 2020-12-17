# インストールした discord.py を読み込む
import discord
import json
import requests
import random
import aiohttp
import asyncio
from discord.ext import commands


#PixabayのURL
PIXABAY_URL = 'https://pixabay.com/api/?key=19427820-6d1c3ed4dc68a0f357a5f6c84'

# BotのTOKEN
TOKEN = 'Nzg0NTMwNzQ3MjQ2NjQxMTU0.X8qpMg.ycXchNKGfTmKZANjYL9wl9UH4Cg'

bot = commands.Bot(command_prefix='!')

#クロッキー時間
croquis_sec = 30

#取得枚数
max_sheets = 200

#起動時の動作
@bot.event
async def on_ready():
    print('ログインしました')

#クロッキー秒数変更
@bot.command()
async def sec(ctx, arg):
    croquis_sec = arg
    await ctx.send("クロッキーの制限時間を {} 秒に変更しました".format(arg))

#上限枚数の変更
""" @bot.command()
async def page(ctx, arg):
    max_sheets = arg
    await ctx.send("上限枚数を {} 枚に変更しました".format(arg)) """

#クロッキーの実行
@bot.command()
async def start(ctx, *args):
    #検索キーワードの追加
    queries = "&q="
    if len(args) != 0:
        for word in args:
            queries = queries + word + "+"

    #イメージタイプの指定
    image_type = "&image_type=photo"

    #取得枚数の指定
    per_page = "&per_page=" + str(max_sheets)

    url = PIXABAY_URL + queries + image_type + per_page

    #合計取得数の取得
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js_tmp = await r.json()
                total = js_tmp["total"]

    #表示ページ数の指定
    rand_page = random.randrange(int(total / max_sheets))
    page = "&page=" + str(rand_page)

    url = PIXABAY_URL + queries + image_type + per_page + page

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                js = await r.json()
                js_hits = js["hits"]
                random.shuffle(js_hits) #画像をランダムに並び替え
                for img in js_hits:
                    await ctx.channel.send(img["pageURL"])
                    await ctx.channel.send(img["largeImageURL"])
                    await asyncio.sleep(croquis_sec)

                await ctx.channel.send("上限枚数に到達した為、動作を停止します")


# Botの起動とDiscordサーバーへの
# 接続
bot.run(TOKEN)