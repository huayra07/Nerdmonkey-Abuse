import os
from dotenv import load_dotenv
import discord
import json

load_dotenv(dotenv_path="tokens.env")

intents = discord.Intents.all()
bot = discord.Bot(intents=intents)
big_boi_id = int(os.getenv("ID"))

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.invisible)
    print(f'{bot.user.name}#{bot.user.discriminator} has connected to Discord!')


@bot.event
async def on_message(message: discord.Message):
    with open('data.json', 'r+') as file:
        saves = json.load(file)
        for i in saves['servers']:
            if i["guild_id"] == message.guild.id:
                if i["target_id"] == message.author.id:
                    await message.add_reaction("<nerdmonkey:1287076509219291207>")
                    await message.add_reaction("<nerdmonkey1:1287076496422211595>")
                    await message.add_reaction("<nerdmonkey2:1287076458178810008>")
                    break

@bot.slash_command(name="target")
async def target(ctx: discord.ApplicationContext, target: discord.User):
    if ctx.user.id != big_boi_id:
        await ctx.respond("no")
        return

    if not checker(ctx.guild_id, target.id):
        with open('data.json', 'r+') as file:
            data = json.load(file)
            data["servers"].append({
                "guild_id": ctx.guild_id,
                "target_id": target.id
            })
            file.seek(0)
            json.dump(data, file, indent=4)
            await ctx.respond("<:nerdmonkey:1287076509219291207>")
    else:
        await ctx.respond("no")


@bot.slash_command(name="remove_target")
async def remove_target(ctx: discord.ApplicationContext, target: discord.User):
    if ctx.user.id != big_boi_id:
        await ctx.respond('no')
        return
    if not checker(ctx.guild_id, target.id):
        await ctx.respond('no')
        return

    try:
        with open('data.json', 'r+') as file:
            saves = json.load(file)
            saves['servers'] = [
                entry for entry in saves['servers']
                if not (entry['guild_id'] == ctx.guild_id and entry["target_id"] == target.id)
            ]
            file.seek(0)
            json.dump(saves, file, indent=4)
            file.truncate()
            await ctx.respond(f'<:nerdmonkey:1287076509219291207>')
    except Exception as e:
        await ctx.respond(e)


def checker(guild_id, user_id):
    with open('data.json', 'r') as file:
        saves = json.load(file)
        return any(i["guild_id"] == guild_id and i['target_id'] == user_id for i in saves['servers'])


bot.run(os.getenv("DISCORD_TOKEN"))