# test_post.py — testes das views do blog.
# Usamos o 'client' do pytest-django: simula requisições HTTP sem precisar subir um servidor real.
# @pytest.mark.django_db libera o acesso ao banco de dados dentro do teste.

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_view(client):
    # reverse('home') gera a URL a partir do name definido em urls.py (evita hardcode de string).
    # client.get() simula uma requisição GET e retorna um objeto de resposta.
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200  # 200 = OK, página carregou com sucesso


@pytest.mark.django_db
def test_post_list_view(client):
    # Verifica se a listagem de posts responde sem erro, mesmo sem posts no banco.
    url = reverse('post_list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_post_list_shows_only_published(client):
    # Garante que a view filtra corretamente: só posts com status=1 aparecem.
    from blog.tests.factories import PostFactory
    PostFactory(status=1)  # post publicado — deve aparecer
    PostFactory(status=0)  # rascunho — NÃO deve aparecer
    url = reverse('post_list')
    response = client.get(url)
    assert response.status_code == 200
    # response.context['posts'] é o queryset passado para o template pela view
    assert len(response.context['posts']) == 1


@pytest.mark.django_db
def test_post_detail_view(client):
    # Verifica se a página de detalhe de um post publicado carrega corretamente.
    from blog.tests.factories import PostFactory
    post = PostFactory(status=1)
    # reverse com kwargs monta a URL: /blog/post/<slug>/
    url = reverse('post_detail', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['post'] == post  # confirma que a view passou o post certo para o template


@pytest.mark.django_db
def test_post_detail_404_for_draft(client):
    # Garante que posts com status=0 (rascunho) retornam 404 e não ficam acessíveis pela URL.
    from blog.tests.factories import PostFactory
    post = PostFactory(status=0)
    url = reverse('post_detail', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 404  # 404 = Not Found
