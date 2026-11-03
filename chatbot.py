import discord
import os
from discord.ext import commands
# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()

# Activar el privilegio de lectura de mensajes
intents.message_content = True

# Crear el cliente del bot
bot = commands.Bot(command_prefix='$', intents=intents)

from logic import preguntas
@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$natural'):
        pregunta_seleccionada=preguntas()
        await message.channel.send(pregunta_seleccionada)
        
    

    
    
  

bot.run("")