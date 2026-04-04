"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# urls.py (principal) — ponto de entrada de todas as URLs do projeto.
# O Django lê este arquivo quando recebe uma requisição e procura
# qual view deve tratar aquela URL.

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    # Página inicial: usa TemplateView diretamente (sem precisar de uma view customizada)
    # porque só renderiza um template estático sem lógica extra.
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    # Painel de administração do Django (gerado automaticamente)
    path('admin/', admin.site.urls),

    # include() delega todas as URLs que começam com 'blog/' para o arquivo blog/urls.py.
    # Exemplo: /blog/post/meu-post/ → o Django remove o prefixo 'blog/' e passa
    # 'post/meu-post/' para o blog/urls.py resolver.
    path('blog/', include('blog.urls')),
]
