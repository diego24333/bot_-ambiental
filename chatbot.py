import discord
import os
from discord.ext import commands
# La variable intents almacena los privilegios del bot
intents = discord.Intents.default()

# Activar el privilegio de lectura de mensajes
intents.message_content = True

# Crear el cliente del bot
bot = commands.Bot(command_prefix='$', intents=intents)

from logic import gen_pass

@bot.event
async def on_ready():
    print(f'Hemos iniciado sesión como {bot.user}')



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send("Hi!")

    elif message.content.startswith('$bye'):
        await message.channel.send("Tu contraseña: " + gen_pass(10))

    elif message.content.startswith('$adivinanza'):
        await message.channel.send(
            "¿Qué tiene agujas, pero no cose?"
        )
    elif message.content.lower().strip() == "reloj":
        await message.channel.send(
            "¡Correcto! 🎉 Has acertado la adivinanza."
        )
    
  

bot.run("")