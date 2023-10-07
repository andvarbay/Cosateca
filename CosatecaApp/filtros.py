from django.shortcuts import render
from django.views import View

from CosatecaApp.models import Categoria


class Filtros(View):
    return_url=None

    def get(self, request):
        data = {}
        categorias = Categoria.objects.all().order_by('nombre')
        data['categorias'] = categorias
        return render(request, 'filtros.html', data)
    
    def post(self, request):
        postData = request.POST
        categorias = postData.getlist('categorias')
        disponible = postData.get('disponible')
        