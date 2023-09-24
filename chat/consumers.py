import datetime
import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from CosatecaApp.models import Chat, Mensaje, Usuario

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f"chat_{self.chat_id}"

        # Unirse a un chat
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        # Salir de un chat
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensaje = text_data_json["mensaje"]
        nombreUsuario = text_data_json["usuarioId"]
        chat = text_data_json["chatId"]
        usuario = await self.getUsuario(nombreUsuario)
        idChat = await self.getChat(chat)

        nuevo_mensaje = await self.crear_mensaje(mensaje, usuario, idChat)
        fechaMensaje = nuevo_mensaje.fechaHora.strftime('%d/%m/%Y %H:%M')
        # Enviar el mensaje a la sala
        await self.channel_layer.group_send(
            self.chat_group_name, {"type": "chat_mensaje", "mensaje": mensaje, "nombreUsuario": nombreUsuario, "fechaMensaje": fechaMensaje}
        )

    async def chat_mensaje(self, event):
        mensaje = event["mensaje"]
        nombreUsuario = event["nombreUsuario"]
        fechaMensaje = event["fechaMensaje"]

        # Enviar los parametros al WebSocket
        await self.send(text_data=json.dumps({"mensaje": mensaje, "nombreUsuario": nombreUsuario, "fechaMensaje": fechaMensaje}))

    @sync_to_async
    def crear_mensaje(self, mensaje, usuario, chat) :
        mensaje = Mensaje(texto=mensaje, idEmisor=usuario, idChat=chat, fechaHora = datetime.datetime.now())
        mensaje.save()

        return mensaje

    @database_sync_to_async
    def getUsuario(self, nombreUsuario) :
        return Usuario.objects.get(nombreUsuario=nombreUsuario)
    
    @database_sync_to_async
    def getChat(self, chat) :
        return Chat.objects.get(idChat=chat)
