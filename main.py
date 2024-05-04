import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
from task_utils import deadline_format, time_format, saveTask, showTask, count_deadline
import os
import pandas as pd
from datetime import datetime, timedelta
import os
import pandas as pd
import discord

# Load file .env 
load_dotenv()

# Ambil token dari env
token = os.getenv('BOT_TOKEN')

answer = []
isStarting = False
isNew = True

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event 
async def on_ready(): 
    print(f"Logged in as {bot.user.name}")
    
# Fungsi untuk mengirim pesan ke pengguna berdasarkan ID-nya
async def send_message_to_user(user_id, message):
    user = await bot.fetch_user(user_id)
    await user.send(message)
    
# Fungsi dijalankan setiap jam 9 pagi
async def scheduled_notif(): 
    while True: 
        now = datetime.now()
        # disini tambahkan tugas 

@bot.command()
# Fungsi utama start()
async def start(ctx): 
    global isStarting
    if isNew:
        await ctx.send(f"Hai {ctx.author.mention}, saya merupakan bot yang dapat membantu mengingatkan tugas-tugasmu berdasarkan tenggat waktu yang kamu berikan. Silakan pilih menu dibawah!\n:point_right: **!new** : tambahkan tugas baru\n:point_right: **!show**: tampilkan semua tugas")
        isStarting = True

@bot.command()
async def new(ctx): 
    global isNew, isStarting

    if isNew:
        isNew = False
        # List pertanyaan
        task = [
            "Masukkan nama tugasmu!",
            "Tanggal berapa tenggatnya? (Format: DD-MM-YYYY)",
            "Jam berapa tenggatnya? (Format: HH:MM)"
        ]
        
        global answer
        
        if isStarting:
            isStarting = False
            for pertanyaan in task: 
                await ctx.send(f"{pertanyaan} {ctx.author.mention}")
                response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                
                while response.content.startswith("!"): 
                    await ctx.send("Format salah, masukkan input dengan tanpa karakter ! diawal")
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                
                # Validasi format deadline
                while pertanyaan.startswith("Tanggal") and not deadline_format(response.content) :
                    await ctx.send("Format tanggal tidak valid atau sudah lewat. Silakan masukkan tanggal dengan format DD-MM-YYYY.")
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                    
                # Validasi format jam
                while pertanyaan.startswith("Jam") and not time_format(response.content, answer[1]): 
                    await ctx.send("Format jam tidak valid atau sudah lewat. Silakan masukkan jam dengan format HH:MM")
                    response = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
                
                answer.append(response.content)
                
            # Mengembalikan isStarting menjadi True setelah selesai pertanyaan
            isStarting = True
            isNew = True
        else: 
            await ctx.send("Gunakan perintah **!start** terlebih dahulu")
         
    task_name = answer[0]
    deadline = answer[1]
    time = answer[2]
    day, hour = count_deadline(deadline, time)
    await ctx.send(f"Tugas yang baru diinputkan {ctx.author.mention} :point_down: :point_down:\n:scroll:: **{task_name}**\n:calendar_spiral:: {deadline}, {time} \n:hourglass_flowing_sand:: **{day} hari {hour} jam**\n\u200B")
    
    # Menggunakan ctx.author sebagai nama pengguna
    author_id = ctx.author.id
    answer = []
    
    saveTask(task_name, deadline, time, author_id)

@bot.command()
async def show(ctx): 
    if isStarting:
        all_tasks = showTask(ctx.author.id)
        if all_tasks is not None: 
            await ctx.send(f"List Tugas {ctx.author.mention} :point_down: :point_down:")
            for index, task in all_tasks.iterrows(): 
                task_name = task['task_name']
                deadline = task['deadline']
                time = task['time']
                day, hour = count_deadline(deadline, time)
                await ctx.send(f":scroll:: **{task_name}**\n:calendar_spiral:: {deadline}, {time} \n:hourglass_flowing_sand:: **{day} hari {hour} jam**\n\u200B") 
        else: 
            await ctx.send("Tidak ada tugas")
    else: 
        await ctx.send("Gunakan perintah **!start** terlebih dahulu")

bot.run(token)
