import discord
import requests 
import os

# クライアント接続
intents = discord.Intents.none()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

# 起動時の処理（無くても問題ない）
@client.event
async def on_ready():
    print('ログインしました')

# Bot が所属しているチャンネルにメッセージがされた時に動作する処理
@client.event
async def on_message(message):
# Bot からのメッセージは無視
    if message.author.bot:
        return
# @everyone の場合、LINE に通知する
    if message.mention_everyone:
# メッセージの投稿主
        author = message.author
# メッセージの内容
        msg = message.content
# メッセージ内容の整形
        msg = msg.replace('@everyone','')
        msg = f'From:{author}\nMessage:{msg}'
        send_notify(msg)
        return
# メンションじゃない場合は無視
    if not message.mentions:
        return
# メンションされたユーザ名を取得
    for mention in message.mentions:
        name = mention.name
# メンションされたユーザ名が自分だったら LINE に通知する
# Discord のユーザ名に置き換えて下さい。Discord 左下の"#数字列"の前部分
    if name == NAME:
        author = message.author
        msg = message.content
        id = DISCORD_ID
        msg = msg.replace('<@' + id + '>','')
        msg = f'From:{author}\nMessage:{msg}'
        send_notify(msg)

def send_notify(message):
    api_url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {LINE_TOKEN}'}
    data = {'message': f'{message}'}
    requests.post(api_url,headers=headers,data=data)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LINE_TOKEN = os.getenv("LINE_TOKEN")
DISCORD_ID = os.getenv("DISCORD_ID")
NAME = os.getenv("MY_NAME")

client.run(DISCORD_TOKEN)
