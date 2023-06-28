import discord
import os

client = discord.Client(intents=discord.Intents.default())

TOKEN = os.environ['BOT_TOKEN']


@client.event
async def on_ready():
  print(f'we have logged in as {client}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')


client.run(TOKEN)
