# Classe de paginação padrão utilizando PageNumberPagination do Django REST framework.
# Define o tamanho padrão da página, permite a consulta do tamanho da página via parâmetro de URL
# e define um tamanho máximo de página.

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
