import discord
import schedule
import time
import asyncio
import os
from datetime import datetime
import pytz
from tonystark_chavo import enviar_mensaje
from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return '''<body style="margin: 0; padding: 0;">
    <iframe width="100%" height="100%" src="https://axocoder.vercel.app/" frameborder="0" allowfullscreen></iframe>
  </body>'''

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():  
    t = Thread(target=run)
    t.start()

keep_alive()
print("Server Running Because of Axo")

# Lee el token de la variable de entorno
token = os.getenv("DISCORD_BOT_TOKEN")
if not token:
    raise ValueError("El token del bot de Discord no está configurado en la variable de entorno DISCORD_BOT_TOKEN")

canal_id = 1241942595106766900  # Reemplaza con tu ID de canal

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def enviar_mensaje_buenos_dias():
    asyncio.run_coroutine_threadsafe(enviar_mensaje(client, canal_id, "Buenos días"), client.loop)

def enviar_mensaje_vecindad():
    asyncio.run_coroutine_threadsafe(enviar_mensaje(client, canal_id, "Ya casi se viene la vecindad, ¡qué emoción!"), client.loop)

def enviar_mensaje_buenas_tardes():
    asyncio.run_coroutine_threadsafe(enviar_mensaje(client, canal_id, "Buenas tardes, gente"), client.loop)

def enviar_mensaje_coleccion():
    asyncio.run_coroutine_threadsafe(enviar_mensaje(client, canal_id, "¡Va a ser la bomba esta colección!"), client.loop)

def enviar_mensaje_feliz_noche():
    asyncio.run_coroutine_threadsafe(enviar_mensaje(client, canal_id, "Feliz noche"), client.loop)

# Definir la zona horaria de México
tz = pytz.timezone('America/Mexico_City')

def schedule_task(hour, minute, task):
    now = datetime.now(tz)
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time < now:
        target_time += timedelta(days=1)
    schedule_time = target_time.strftime("%H:%M")
    schedule.every().day.at(schedule_time).do(task)

schedule_task(9, 13, enviar_mensaje_buenos_dias)
schedule_task(12, 16, enviar_mensaje_vecindad)
schedule_task(16, 48, enviar_mensaje_buenas_tardes)
schedule_task(21, 27, enviar_mensaje_coleccion)
schedule_task(2, 13, enviar_mensaje_feliz_noche)

@client.event
async def on_ready():
    print("¡Bot listo!")

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(client.start(token))
    loop.run_in_executor(None, run_schedule)
    loop.run_forever()
