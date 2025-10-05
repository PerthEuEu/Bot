import os
import discord
import requests
from discord.ext import commands

# ===== Discord Token จาก Replit Secrets =====
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]  # ใส่ Discord bot token ใน Secrets

# ===== Hugging Face Token =====
HUGGINGFACE_API_KEY = os.environ["HF_API_TOKEN"]

# ===== สร้าง Bot =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== ฟังก์ชันถาม Hugging Face =====
def ask_huggingface(prompt):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data[0]['generated_text']
    else:
        return f"เกิดข้อผิดพลาด: {response.status_code}"

# ===== Event: บอทออนไลน์ =====
@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้ว! ชื่อ: {bot.user}")

# ===== Command: !ask =====
@bot.command()
async def ask(ctx, *, question):
    """ถาม Hugging Face AI"""
    answer = ask_huggingface(question)
    await ctx.send(answer)

# ===== เริ่ม Bot =====
bot.run(DISCORD_TOKEN)
