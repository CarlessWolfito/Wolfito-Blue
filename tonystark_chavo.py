import discord

async def enviar_mensaje(client, canal_id, mensaje):
    canal = client.get_channel(canal_id)
    await canal.send(mensaje)
