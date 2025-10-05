import os
import requests
from discord.ext import commands
import discord

DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
HF_API_KEY = os.environ["HF_API_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def ask_huggingface(prompt):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data[0]['generated_text']
    else:
        return f"เกิดข้อผิดพลาด: {response.status_code}"

@bot.event
async def on_ready():
    print(f"บอทออนไลน์! ชื่อ: {bot.user}")

@bot.command()
async def ask(ctx, *, question):
    answer = ask_huggingface(question)
    await ctx.send(answer)

bot.run(DISCORD_TOKEN)
