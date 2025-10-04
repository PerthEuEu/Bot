import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from openai import OpenAI

# ===== โหลดค่า Environment Variables =====
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ===== สร้าง Client OpenAI =====
client = OpenAI(api_key=OPENAI_API_KEY)

# ===== ตั้งค่า Discord Bot =====
intents = discord.Intents.default()
intents.message_content = True  # ต้องเปิดเพื่ออ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== เมื่อบอทออนไลน์ =====
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} ออนไลน์แล้ว!")

# ===== คำสั่ง !ask =====
@bot.command()
async def ask(ctx, *, question):
    """ถามคำถามกับ ChatGPT"""
    print(f"Received question: {question}")  # debug ว่าคำสั่งมาถึงบอทหรือไม่
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # หรือ gpt-4, gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        await ctx.reply(answer)
        print(f"Sent answer: {answer}")  # debug ว่าส่งข้อความกลับแล้ว
    except Exception as e:
        await ctx.reply(f"เกิดข้อผิดพลาด: {e}")
        print(f"Error: {e}")

# ===== เริ่มบอท =====
bot.run(DISCORD_TOKEN)
