# views.py — recebe a requisição HTTP, busca dados e retorna uma resposta (HTML renderizado).
# Usamos Class-Based Views (CBVs): classes prontas do Django que já implementam
# o fluxo padrão (dispatch → get → render). Só sobrescrevemos o que precisamos customizar.

from django.views.generic import DetailView, ListView
from django.http import HttpResponse

from .models import Post, PostStatus


def post_view(request):
	return HttpResponse('Minha view de Post')


class PostListView(ListView):
	# ListView é uma CBV do Django para listar objetos de um modelo.
	# Fluxo: recebe GET /blog/ → chama get_queryset() → renderiza o template com a lista.

	model = Post                          # modelo que será listado
	template_name = 'blog/post_list.html' # template HTML que será renderizado
	context_object_name = 'posts'         # nome da variável disponível no template ({{ posts }})

	def get_queryset(self):
		# Sobrescrevemos get_queryset() para filtrar apenas posts publicados.
		# select_related('author')              → faz JOIN com a tabela User (evita N+1 queries)
		# prefetch_related('categories', 'tags') → busca M2M em queries separadas otimizadas
		return (
			Post.objects.filter(status=PostStatus.PUBLISHED)
			.select_related('author')
			.prefetch_related('categories', 'tags')
		)


class PostDetailView(DetailView):
	# DetailView é uma CBV para exibir UM objeto específico.
	# Fluxo: recebe GET /blog/post/<slug>/ → busca o post pelo slug → renderiza o template.

	model = Post
	template_name = 'blog/post_detail.html'
	context_object_name = 'post'  # variável {{ post }} no template
	slug_field = 'slug'           # campo do modelo usado para buscar o objeto
	slug_url_kwarg = 'slug'       # nome do parâmetro na URL (ver urls.py)

	def get_queryset(self):
		# Filtra apenas posts publicados. Se o slug existir mas for rascunho, retorna 404.
		return (
			Post.objects.filter(status=PostStatus.PUBLISHED)
			.select_related('author')
			.prefetch_related('categories', 'tags', 'comments__author')
		)

	def get_context_data(self, **kwargs):
		# get_context_data() adiciona variáveis extras ao contexto do template.
		# super() executa o comportamento padrão da DetailView (já coloca 'post' no contexto).
		context = super().get_context_data(**kwargs)

		# Adicionamos 'comments' ao contexto: apenas comentários aprovados do post atual.
		# self.object é o Post que foi buscado pelo get_queryset().
		context['comments'] = (
			self.object.comments.filter(is_approved=True).select_related('author')
		)
		return context
