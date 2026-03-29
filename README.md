# 📝 Mysite - Django Personal Blog

Um blog pessoal moderno construído com **Django 6.0** com suporte completo a posts, categorias, tags e comentários.

## 🎯 Funcionalidades

### ✅ Implementado
- **Modelos de Dados**
  - `Post` - Artigos de blog com título, slug, conteúdo, autor e status (Draft/Publicado)
  - `Category` - Categorias para organizar posts (ManyToMany)
  - `Tag` - Tags para classificação adicional de posts (ManyToMany)
  - `Comment` - Sistema de comentários com aprovação

- **Admin Dashboard**
  - Interface Django admin completa para gerenciar posts, categorias, tags e comentários
  - Suporte para criar, editar e deletar conteúdo

- **Testes & Qualidade**
  - Testes automatizados com pytest + pytest-django
  - Factories para dados de teste
  - Configuração de teste completa

### ⏳ A Fazer
- Views para listar, detalhar e criar posts
- Templates HTML frontend
- Sistema de autenticação de usuários
- API REST (opcional)
- Busca e filtros avançados

---

## 📁 Estrutura do Projeto

```
mysite/
├── manage.py                 # CLI do Django
├── requirements.txt          # Dependências do projeto
├── requirements-dev.txt      # Dependências de desenvolvimento
├── README.md                 # Este arquivo
│
├── config/                   # Configurações do Django
│   ├── settings.py           # Configurações do projeto
│   ├── urls.py               # URLs principais
│   ├── wsgi.py               # WSGI para deploy
│   └── asgi.py               # ASGI para WebSockets
│
└── blog/                     # App principal do blog
    ├── models.py             # Modelos (Post, Category, Tag, Comment)
    ├── admin.py              # Configuração do admin
    ├── views.py              # Views (a implementar)
    ├── urls.py               # URLs (a implementar)
    ├── apps.py              # Configuração da app
    │
    ├── migrations/           # Migrações do banco de dados
    │   ├── 0001_initial.py
    │   └── 0002_category_tag_post_categories_comment_post_tags.py
    │
    └── tests/                # Testes automatizados
        ├── conftest.py       # Config do pytest
        ├── factories.py      # Factories para testes
        ├── test_models.py    # Testes dos modelos
        └── test_factories.py # Testes das factories
```

---

## 🚀 Como Começar

### 1️⃣ Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### 2️⃣ Instalação

**Clone ou entre no diretório do projeto:**
```bash
cd "c:\Users\digui\Desktop\My site\mysite"
```

**Ative o ambiente virtual (se existir):**
```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**Instale as dependências:**
```bash
pip install -r requirements.txt
```

**Para desenvolvimento (testes + extras):**
```bash
pip install -r requirements-dev.txt
```

### 3️⃣ Configuração do Banco de Dados

**aplique as migrações:**
```bash
python manage.py migrate
```

**Crie um superusuário (admin):**
```bash
python manage.py createsuperuser
```

Você será pedido para:
- Nome de usuário
- Email
- Senha (digitada 2x)

### 4️⃣ Rode o Servidor

```bash
python manage.py runserver
```

Acesse em seu navegador:
- **Website:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

---

## 📊 Modelos de Dados

### Post
```python
Post(
    title: str                      # Título único (max 200 chars)
    slug: str                       # URL-friendly (auto-gerado do title)
    author: User                    # FK -> Quem escreveu
    categories: Category[]          # M2M -> Categorias do post
    tags: Tag[]                     # M2M -> Tags do post
    content: str                    # Conteúdo do artigo
    status: int                     # 0=Draft, 1=Publicado
    created_on: datetime            # Auto-preenchido
    updated_on: datetime            # Auto-atualizado
)
```

### Category
```python
Category(
    name: str                       # Nome único (max 100)
    description: str                # Descrição (opcional)
    created_on: datetime            # Auto-preenchido
)
```

### Tag
```python
Tag(
    name: str                       # Nome único (max 50)
)
```

### Comment
```python
Comment(
    post: Post                      # FK -> Em qual post
    author: User                    # FK -> Quem comentou
    content: str                    # Texto do comentário
    is_approved: bool               # Aprovado? (default: False)
    created_on: datetime            # Auto-preenchido
    updated_on: datetime            # Auto-atualizado
)
```

---

## 🛠️ Como Usar

### Usando o Admin Dashboard

1. Acesse: http://127.0.0.1:8000/admin/
2. Faça login com o superusuário criado
3. Crie suas primeiras categorias e tags
4. Escreva seus primeiros posts
5. Modere comentários dos visitantes

### Exemplo: Criar um Post

1. Clique em "Posts" no admin
2. Clique em "Add Post"
3. Preencha:
   - **Title:** "Meu Primeiro Post"
   - **Author:** Você (seu usuário)
   - **Content:** Seu artigo
   - **Status:** Publish (1)
   - **Categories:** Selecione [Ctrl+Click para múltiplas]
   - **Tags:** Selecione
4. Clique em "Save"

---

## 🧪 Rodando Testes

Execute os testes para garantir que tudo funciona:

```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=blog

# Verbose (mais detalhes)
pytest -v

# Apenas um arquivo
pytest blog/tests/test_models.py
```

**Estrutura dos testes:**
- `test_models.py` - Testes dos modelos Django
- `test_factories.py` - Testes das factories (geração de dados de teste)
- `conftest.py` - Configuração global do pytest
- `factories.py` - Factories para criar objetos de teste

---

## 📝 Próximas Etapas

Para fazer o blog totalmente funcional:

### 1. Views & Templates
```bash
# Criar as views em blog/views.py
- post_list()         # Listar todos os posts
- post_detail()       # Detalhar um post
- post_create()       # Criar novo post
- comment_create()    # Adicionar comentário

# Criar templates em blog/templates/blog/
- post_list.html      # Lista de posts
- post_detail.html    # Página do post
- post_form.html      # Formulário de novo post
```

### 2. URLs
```bash
# Adicionar rotas em blog/urls.py e config/urls.py
Pattern geral:
/               → Lista de posts
/post/<slug>/   → Detalhe do post
/post/new/      → Criar novo post
```

### 3. Autenticação
```bash
# Implementar login/logout
- Sistema de registro de usuários
- Restrição de acesso para criar posts
```

### 4. Filtros & Busca
```bash
# Filtrar posts por:
- Categoria
- Tag
- Busca por título
- Data (mais recentes, mais antigos)
```

---

## 📦 Dependências Principais

- **Django 6.0.3** - Framework web
- **pytest** - Framework de testes
- **pytest-django** - Plugin Django para pytest
- Outras bibliotecas opcionais (LangChain, Google AI, FastAPI) não são usadas no blog básico

---

## 📚 Documentação

- [Django Docs](https://docs.djangoproject.com/)
- [Pytest Docs](https://docs.pytest.org/)
- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)

---

## 💡 Dicas

- Use `python manage.py shell` para experimentar com models interativamente
- Use `python manage.py dbshell` para acessar o banco de dados diretamente
- Use `python manage.py createsuperuser` novamente para adicionar mais admins
- Sempre rode `python manage.py migrate` após alterar models

---

## 🐛 Troubleshooting

**Erro: "Table does not exist"**
```bash
python manage.py migrate
```

**Erro: "ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Quer resetar o banco de dados?**
```bash
# ⚠️ Isso deleta TODOS os dados!
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
```

---

Desenvolvido com ❤️ usando Django.
