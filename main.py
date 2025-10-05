import discord
from discord.ext import commands

# ======== CONFIG ==========
TOKEN = "YOUR_BOT_TOKEN"  # 🔒 ใส่โทเคนบอทของนายตรงนี้
CHANNEL_ID = 1424404081144758422  # ✅ ช่องที่ให้บอทอยู่ประจำ
# ==========================

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# --------------------------
# ข้อมูลแมตช์ (นายจะใส่เองได้ในภายหลัง)
# --------------------------
matches = {
    "premier_league": {
        "Arsenal vs Chelsea": "📅 วันที่แข่ง: 12 ต.ค.\n⏰ เวลา: 21:00\n🏟 สนาม: Emirates Stadium",
        "Liverpool vs Man City": "📅 วันที่แข่ง: 13 ต.ค.\n⏰ เวลา: 22:30\n🏟 สนาม: Anfield"
    },
    "laliga": {
        "Barcelona vs Real Madrid": "📅 วันที่แข่ง: 15 ต.ค.\n⏰ เวลา: 23:00\n🏟 สนาม: Camp Nou",
        "Atletico vs Valencia": "📅 วันที่แข่ง: 16 ต.ค.\n⏰ เวลา: 02:00\n🏟 สนาม: Wanda Metropolitano"
    }
}

# --------------------------
# UI: เมนูเลือกลีก
# --------------------------
class LeagueSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Premier League", value="premier_league", emoji="🏴"),
            discord.SelectOption(label="La Liga", value="laliga", emoji="🇪🇸"),
        ]
        super().__init__(placeholder="เลือกลีกที่ต้องการดู ⚽", options=options)

    async def callback(self, interaction: discord.Interaction):
        league = self.values[0]
        view = MatchListView(league)
        embed = discord.Embed(
            title=f"📅 แมตช์ใน {self.values[0].replace('_', ' ').title()}",
            description="เลือกแมตช์ที่ต้องการดูข้อมูลได้เลย 👇",
            color=0x1E90FF
        )
        await interaction.response.edit_message(embed=embed, view=view)

# --------------------------
# UI: รายชื่อแมตช์
# --------------------------
class MatchListView(discord.ui.View):
    def __init__(self, league):
        super().__init__(timeout=None)
        self.league = league
        for match_name in matches[league]:
            self.add_item(MatchButton(match_name, league))

class MatchButton(discord.ui.Button):
    def __init__(self, match_name, league):
        super().__init__(label=match_name, style=discord.ButtonStyle.primary)
        self.match_name = match_name
        self.league = league

    async def callback(self, interaction: discord.Interaction):
        info = matches[self.league][self.match_name]
        embed = discord.Embed(
            title=f"📊 {self.match_name}",
            description=info,
            color=0x00FF99
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# --------------------------
# UI: หน้าหลัก
# --------------------------
class LeagueView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LeagueSelect())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)

    if channel:
        embed = discord.Embed(
            title="⚽ Football Match Info",
            description="เลือกลีกที่ต้องการดูข้อมูลแมตช์จากเมนูด้านล่าง 👇",
            color=0xFFD700
        )
        view = LeagueView()
        await channel.send(embed=embed, view=view)
        print(f"📢 Bot started in #{channel.name}")
    else:
        print("❌ ไม่พบ Channel ID ตรวจสอบว่าใส่ถูกและบอทมีสิทธิ์เข้าช่องนั้นหรือไม่")

bot.run(TOKEN)
