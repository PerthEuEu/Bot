import os
import discord
from discord.ext import commands
import requests

# ===== Secrets =====
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
HF_API_KEY = os.environ["HF_API_TOKEN"]

# ===== Bot setup =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== Hugging Face query =====
def ask_hf(prompt):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": prompt}
    r = requests.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        return r.json()[0]["generated_text"]
    else:
        return f"เกิดข้อผิดพลาด: {r.status_code}"

# ===== Bot ready =====
@bot.event
async def on_ready():
    print(f"✅ Bot ออนไลน์แล้ว! ชื่อ: {bot.user}")

# ===== Command !ask =====
@bot.command()
async def ask(ctx, *, question):
    print("Received:", question)  # ตรวจสอบว่า bot ได้รับข้อความ
    answer = ask_hf(question)
    await ctx.send(answer)

# ===== Run bot =====
bot.run(DISCORD_TOKEN)
