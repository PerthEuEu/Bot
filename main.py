import discord
from discord.ext import commands
from openai import OpenAI

# ===== กำหนด TOKEN =====
DISCORD_TOKEN = "MTQyNDAzNDE0MDM5OTA3OTQ1NQ.G8rWJW.QyneSNSb5h5xPTKGoxlYcR9nhy5UxPNHtDeclQ"  # ใส่ Token ของบอท Discord
OPENAI_API_KEY = "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"    # ใส่ API key ของ OpenAI

# ===== สร้าง Client =====
client = OpenAI(api_key=OPENAI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True  # ให้บอทอ่านข้อความในช่องได้
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== เมื่อบอทออนไลน์ =====
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} ออนไลน์แล้ว!")

# ===== คำสั่ง !ask =====
@bot.command()
async def ask(ctx, *, question):
    """ถามคำถามกับ ChatGPT"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # หรือ gpt-4, gpt-3.5-turbo ก็ได้
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        await ctx.reply(answer)
    except Exception as e:
        await ctx.reply(f"เกิดข้อผิดพลาด: {e}")

# ===== เริ่มบอท =====
bot.run(MTQyNDAzNDE0MDM5OTA3OTQ1NQ.G8rWJW.QyneSNSb5h5xPTKGoxlYcR9nhy5UxPNHtDeclQ)
