# admin.py — registra os modelos no painel de administração do Django.
# Após registrar, os modelos ficam acessíveis em http://127.0.0.1:8000/admin/
# onde é possível criar, editar e deletar registros sem escrever código extra.

from django.contrib import admin
from .models import Post, Category, Tag, Comment

# admin.site.register(Modelo) faz o modelo aparecer no painel admin.
# É possível passar uma classe ModelAdmin como segundo argumento para customizar
# campos exibidos, filtros, campos de busca, etc. (não implementado aqui ainda).
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)
