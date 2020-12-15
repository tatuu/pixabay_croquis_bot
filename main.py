# インストールした discord.py を読み込む
import discord
import json
import requests
import random
import aiohttp
import asyncio
from discord.ext import commands


#PixabayのTOKEN
PIXABAY_TOKENURL = 'https://pixabay.com/api/?key=19427820-6d1c3ed4dc68a0f357a5f6c84'

# BotのTOKEN
TOKEN = 'Nzg0NTMwNzQ3MjQ2NjQxMTU0.X8qpMg.ycXchNKGfTmKZANjYL9wl9UH4Cg'

# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix='!')

#クロッキー時間
croquis_sec = 30

#上限枚数
max_sheets = 50

#起動時の動作
@bot.event
async def on_ready():
    print('ログインしました')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

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

    #上限枚数の指定
    per_page = "&per_page=" + str(max_sheets)

    url = PIXABAY_TOKENURL + queries + image_type + per_page

    #urlの確認
    #await ctx.channel.send(url)

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



# メッセージ受信時に動作する処理
@bot.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
        
    await bot.process_commands(message)

# Botの起動とDiscordサーバーへの
# 接続
bot.run(TOKEN)