# urls.py (blog) — define as rotas da aplicação blog.
# Este arquivo é incluído pelo urls.py principal com o prefixo /blog/.
# Resultado final das rotas:
#   /blog/                 → PostListView  (lista de posts)
#   /blog/post/<slug>/     → PostDetailView (detalhe de um post)

from django.urls import path
from .views import PostDetailView, PostListView

urlpatterns = [
    # path(rota, view, name) → 'name' permite referenciar a URL no template com {% url 'post_list' %}
    path('', PostListView.as_view(), name='post_list'),

    # <slug:slug> é um conversor de URL: aceita apenas letras, números e hífens.
    # O valor capturado é passado para a view como parâmetro 'slug'.
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
