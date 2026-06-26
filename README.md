# INF1407 - API de Adocao de Pets

Backend da plataforma academica de adocao de pets para a disciplina INF1407 - Programacao para Web.

## Autores

- Guilherme Santos Marques
- Matheus Fonseca Vilella

## Descricao

Esta API REST gerencia usuarios, pets, solicitacoes de adocao, favoritos e um painel resumido. O backend e independente do frontend e nao contem HTML, CSS ou JavaScript da aplicacao.

## Funcionalidades

- Cadastro de usuarios.
- Login com JWT.
- Refresh de token.
- Consulta do usuario autenticado.
- Alteracao de senha.
- Recuperacao de senha.
- CRUD de pets.
- Filtros e busca de pets.
- Upload de foto de pet.
- Solicitacao de adocao.
- Cancelamento de solicitacao pendente.
- Aprovacao e recusa de solicitacoes por responsavel.
- Favoritos por usuario.
- Painel resumido com dados diferentes por perfil.
- Documentacao Swagger/OpenAPI.
- Controle de acesso no backend.

## Tecnologias

- Python
- Django
- Django REST Framework
- Simple JWT
- django-cors-headers
- drf-spectacular
- Pillow
- python-dotenv
- SQLite em desenvolvimento

## Estrutura

```text
config/       configuracao do projeto Django
usuarios/    usuario customizado e endpoints de autenticacao
pets/        cadastro e gerenciamento de pets
adocoes/     solicitacoes de adocao, favoritos e painel
```

## Variaveis de ambiente

Crie um arquivo `.env` na raiz do projeto usando `.env.example` como base:

```env
SECRET_KEY=troque-esta-chave-em-desenvolvimento
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Nao versionar `.env`.

## Instalacao local

No Windows PowerShell:

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Se o PowerShell bloquear scripts, ative o ambiente com:

```bash
.\venv\Scripts\activate.bat
```

## Execucao

Servidor local:

```bash
python manage.py runserver
```

API local:

```text
http://127.0.0.1:8000/api/
```

## Documentacao

```text
GET /api/schema/
GET /api/docs/
GET /api/redoc/
```

## Endpoints principais

### Autenticacao

```text
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/
GET  /api/auth/me/
POST /api/auth/change-password/
POST /api/auth/password-reset/
POST /api/auth/password-reset/confirm/
```

### Pets

```text
GET    /api/pets/
POST   /api/pets/
GET    /api/pets/{id}/
PATCH  /api/pets/{id}/
DELETE /api/pets/{id}/
```

Filtros:

```text
?especie=
?porte=
?sexo=
?status=
?search=
```

### Solicitacoes

```text
GET    /api/solicitacoes/
POST   /api/solicitacoes/
GET    /api/solicitacoes/{id}/
DELETE /api/solicitacoes/{id}/
POST   /api/solicitacoes/{id}/aprovar/
POST   /api/solicitacoes/{id}/recusar/
```

### Favoritos

```text
GET    /api/favoritos/
POST   /api/favoritos/
DELETE /api/favoritos/{id}/
```

### Painel

```text
GET /api/dashboard/
```

## Regras de acesso

- Adotantes visualizam pets disponiveis.
- Adotantes visualizam somente suas proprias solicitacoes.
- Adotantes visualizam somente seus proprios favoritos.
- Responsaveis visualizam e gerenciam somente seus proprios pets.
- Responsaveis visualizam solicitacoes relacionadas aos seus pets.
- Responsaveis aprovam ou recusam solicitacoes relacionadas aos seus pets.
- Staff visualiza os dados gerais.

Essas regras sao aplicadas no backend.

## Testes

Executar a suite:

```bash
python manage.py test
```

Verificacao do Django:

```bash
python manage.py check
```

Geracao do schema OpenAPI:

```bash
python manage.py spectacular --file schema.yml
```

## Status atual

Funcionando:

- Autenticacao JWT.
- Cadastro e consulta do usuario atual.
- Alteracao e recuperacao de senha.
- CRUD de pets.
- Solicitacoes de adocao.
- Favoritos.
- Painel resumido.
- Swagger e Redoc.
- Testes automatizados principais.

Limitacoes conhecidas:

- Recuperacao de senha ainda nao envia email real; em desenvolvimento, o fluxo pode ser testado com token gerado pela API em `DEBUG=True`.
- Banco configurado para SQLite local em desenvolvimento.
- Publicacao em producao ainda nao configurada neste repositorio.
