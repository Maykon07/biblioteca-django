'''
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from .models import Livro
from .serializers import LivroSerializer
from rest_framework.decorators import api_view
'''

# reimplemente as views utilizando class-based views em vez de function-based views.

from rest_framework import generics

from biblioteca.core.filters import LivroFilter
from .models import Livro
from .serializers import LivroSerializer
from .models import Autor
from .serializers import AutorSerializer
from .models import Categoria
from .serializers import CategoriaSerializer
from django_filters import rest_framework as filters

# Implemente filtros de busca para o atributo nome, utilizando o prefixo ^ (inicia com), para Categoria e Livro.

class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-list"
    filterset_fields = ('titulo', 'autor', 'categoria', 'publicado_em')
    search_fields = (
        '^titulo',
        '^autor__nome',
        '^categoria__nome',
        '^publicado_em'
    )
    ordering_fields = ('titulo', 'autor', 'categoria', 'publicado_em')
#A view LivroList deve permitir a ordenação por titulo, autor, categoria, publicado_em.


class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"

#devem ser replicados também para Categoria e Autor.
#Possibilite a ordenação a partir do atributo nome para Categoria e Livro.

class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-list"
    filterset_fields = ('nome',)
    search_fields = (
        '^nome',
    )
    ordering_fields = ('nome',)

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"



class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-list"
    filterset_fields = ('nome',)
    search_fields = (
        '^nome',
    )
    ordering_fields = ('nome',)

class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"



'''
# Create your views here.
@api_view(['GET','POST'])
@csrf_exempt
def livro_list_create(request):
    if request.method == 'GET':
        livros = Livro.objects.all()
        serializer = LivroSerializer(livros, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = LivroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@csrf_exempt
def livro_detail(request, pk):
    livro = Livro.objects.get(pk=pk)
    if request.method == 'GET':
        serializer = LivroSerializer(livro)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = LivroSerializer(livro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        livro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''