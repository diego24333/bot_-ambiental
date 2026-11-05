from settings import settings
import discord
from bot_logic import *

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

prefix = settings["prefix"]

preguntas_activas = {}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    contenido = message.content

    if not contenido.startswith(prefix) and message.author.id in preguntas_activas:
        canal_id, pregunta_actual = preguntas_activas[message.author.id]
        if message.channel.id == canal_id:
            if not respuesta_valida(pregunta_actual, contenido):
                await message.channel.send(f"{message.author.mention} Responde con **sí** o **no**.")
                return
            del preguntas_activas[message.author.id]
            resultado = procesar_respuesta(message.author.id, pregunta_actual, contenido)
            await message.channel.send(f"{message.author.mention} {resultado}")
        return

    if not contenido.startswith(prefix):
        return

    partes = contenido[len(prefix):].split()
    comando = partes[0].lower() if partes else ""

    if comando == 'hello':
        await message.channel.send('¡Hola! Soy un bot')
    elif comando == 'smile':
        await message.channel.send(gen_emodji())
    elif comando == 'coin':
        await message.channel.send(flip_coin())
    elif comando == 'pass':
        await message.channel.send(gen_pass(10))

    elif comando == 'ayuda':
        await message.channel.send(
            "**Comandos**\n"
            f"`{prefix}pregunta` - recibe una pregunta y responde en el chat\n"
            f"`{prefix}puntos` - mira tus puntos y bonus\n"
            f"`{prefix}ranking` - top 10\n"
            f"`{prefix}tienda` - recompensas disponibles\n"
            f"`{prefix}comprar <item>` - compra una recompensa\n"
            f"`{prefix}hello` `{prefix}smile` `{prefix}coin` `{prefix}pass`"
        )

    elif comando == 'pregunta':
        p = preguntas()
        preguntas_activas[message.author.id] = (message.channel.id, p)
        if p.get("sino"):
            indicacion = "Responde **sí** o **no** en el chat."
        else:
            indicacion = "Escribe tu respuesta en el chat."
        await message.channel.send(f"{message.author.mention} **{p['pregunta']}**\n{indicacion}")

    elif comando == 'puntos':
        pts, escudos, dobles = get_usuario(message.author.id)
        await message.channel.send(
            f"Puntos: **{pts}** | Escudos: **{escudos}** | Usos de doble puntos: **{dobles}**"
        )

    elif comando == 'ranking':
        filas = ranking_top()
        if not filas:
            await message.channel.send("Todavía nadie tiene puntos.")
        else:
            lineas = [f"**{i}.** <@{uid}> - {pts} pts" for i, (uid, pts) in enumerate(filas, 1)]
            await message.channel.send("**Ranking**\n" + "\n".join(lineas))

    elif comando == 'tienda':
        lineas = [
            f"`{clave}` - {i['nombre']} - **{i['precio']} pts**\n{i['desc']}"
            for clave, i in TIENDA.items()
        ]
        await message.channel.send(
            f"**Tienda** (usa `{prefix}comprar <item>`, ej: `{prefix}comprar escudo`)\n\n"
            + "\n\n".join(lineas)
        )

    elif comando == 'comprar':
        if len(partes) < 2 or partes[1].lower() not in TIENDA:
            await message.channel.send(f"Indica qué comprar. Mira las opciones con `{prefix}tienda`.")
            return
        clave = partes[1].lower()
        ok, mensaje = comprar_item(message.author.id, clave)
        await message.channel.send(mensaje)

    else:
        await message.channel.send(f"No puedo procesar este comando, ¡lo siento! Usa `{prefix}ayuda`.")

client.run(settings["TOKEN"])
