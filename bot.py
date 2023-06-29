import discord
import responses
import os
from keep_alive import keep_alive


async def send_message(message, user_message, is_private):
  try:
    response = responses.get_response(user_message)
    if len(response) > 2000:
      with open("result.txt", "wb+") as file:
        file.write(response)
        await message.channel.send("Your maze is:",
                                   file=discord.File(file, "result.txt"))
    else:
      await message.author.send(
        response) if is_private else await message.channel.send(response)
  except Exception as e:
    print(e)


def run_discord_bot():
  TOKEN = os.environ['BOT_TOKEN']
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  @client.event
  async def on_ready():
    print(f'{client.user} is now running!')

  @client.event
  async def on_message(message):
    if message.author == client.user:
      return

    user_message = str(message.content)
    if user_message[0] == '?':
      user_message = user_message[1:]
      await send_message(message, user_message, is_private=True)
    else:
      await send_message(message, user_message, is_private=False)

  keep_alive()
  client.run(TOKEN)
