import discord
import yaml, os
from draw import get_slots

with open("discord_bot/.env", "r") as stream:
    token = yaml.safe_load(stream)["discord-oauth-token"]

client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("/draw"):
        raw_count = message.content.split(" ")[-1]
        if raw_count.isnumeric():
            count = int(raw_count)
            count = count if count <= 5 else 1
            card_file = get_slots(count)
        else:
            card_file = get_slots(1)

        await message.channel.send("Here's your draw")
        await message.channel.send(file=discord.File(card_file))
        os.remove(card_file)
        # await message.channel.send(files=card_files)


client.run(token)
