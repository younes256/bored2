import discord
from discord.ext import commands
import os

# الحصول على رمز البوت من المتغير البيئي
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
if TOKEN is None:
    raise ValueError("No DISCORD_BOT_TOKEN found in environment variables")

# إعداد intents للحصول على الأذونات المناسبة
intents = discord.Intents.default()
intents.messages = True  # تمكين خاصية الرسائل
intents.voice_states = True
intents.guilds = True

# إعداد البوت مع بادئة الأوامر و intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None or not ctx.voice_client.is_connected():  # التحقق من أن البوت غير متصل بالفعل أو فصلته من القناة الصوتية
            voice_client = await channel.connect()
            await ctx.send(f'Joined {channel}')
            await voice_client.guild.change_voice_state(channel=channel, self_deaf=True)  # تفعيل وضع "deafen"
        else:
            await ctx.send('I am already connected to a voice channel!')
    else:
        await ctx.send('You are not in a voice channel!')

@bot.command()
async def leave(ctx):
    if ctx.voice_client and ctx.voice_client.is_connected():  # التحقق من أن البوت متصل بالفعل بالقناة الصوتية
        await ctx.voice_client.disconnect()
        await ctx.send('Left the voice channel')
    else:
        await ctx.send('I am not in a voice channel!')

bot.run(TOKEN)
