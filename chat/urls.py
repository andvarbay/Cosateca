from django.urls import path
from chat import views

app_name = 'chat'

urlpatterns = [
    path('<str:chat_id>/', views.chat_view, name='chat_view'),
]