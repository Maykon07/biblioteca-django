from django_filters import rest_framework as filters
from .models import Livro

class LivroFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='icontains')
    autor = filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')
    categoria = filters.AllValuesFilter(field_name='categoria__nome')

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria']

# Implemente filtros de busca para o atributo nome, utilizando o prefixo ^ (inicia com), para Categoria e Livro.

from django_filters import rest_framework as filters
from .models import Categoria, Livro

class CategoriaFilter(filters.FilterSet):
    nome = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Categoria
        fields = ['nome']

class LivroFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='icontains')
    autor = filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')
    categoria = filters.AllValuesFilter(field_name='categoria__nome')
    pulicado_em = filters.DateFilter()

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria', 'publicado_em']