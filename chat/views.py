import datetime
from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.http import HttpResponseRedirect, JsonResponse
from CosatecaApp.models import Mensaje, Chat, Usuario

def chat_view(request, chat_id):
    data= {}
    chat = Chat.objects.get(idChat=chat_id)
    mensajes = Mensaje.objects.filter(idChat=chat)
    nombreUsuario = request.session.get('usuario')
    if (chat.idUsuarioArrendador.nombreUsuario == nombreUsuario):
        otroNombreUsuario = chat.idUsuarioArrendatario.nombreUsuario
    else :
        otroNombreUsuario = chat.idUsuarioArrendador.nombreUsuario
    usuario = Usuario.getUsuarioPorNombreUsuario(nombreUsuario)
    otroUsuario = Usuario.getUsuarioPorNombreUsuario(otroNombreUsuario)
    data['chat'] = chat
    data['mensajes'] = mensajes
    data['usuario'] = usuario
    data['otroUsuario'] = otroUsuario
    return render(request, 'chat/chat.html', data)