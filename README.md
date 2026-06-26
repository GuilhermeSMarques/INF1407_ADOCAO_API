# INF1407 — API de Adoção de Pets

API REST para gerenciamento de uma plataforma de adoção de pets, desenvolvida com Django e Django REST Framework.

## Autores

- Guilherme Santos Marques
- Matheus Fonseca Vilella

---

## Tecnologias

- Python 3.12
- Django 6.0
- Django REST Framework
- SimpleJWT (autenticação via tokens JWT)
- drf-spectacular (documentação Swagger/OpenAPI)
- Pillow (upload de fotos)
- WhiteNoise (arquivos estáticos em produção)
- Gunicorn (servidor WSGI para produção)

---

## Instalação local

### Pré-requisitos

- Python 3.12+
- pip

### Passos

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd INF1407_ADOCAO_API

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Copie e configure as variáveis de ambiente
cp .env.example .env
# Edite .env se necessário (DEBUG=True por padrão)

# 5. Aplique as migrações
python manage.py migrate

# 6. (Opcional) Crie um superusuário
python manage.py createsuperuser

# 7. Inicie o servidor de desenvolvimento
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

---

## Execução com Docker

```bash
# 1. Copie e configure o .env
cp .env.example .env
# Edite DEBUG=False, ALLOWED_HOSTS=<seu-dominio>, SECRET_KEY=<chave-segura>

# 2. Build da imagem
docker build -t adocao-api .

# 3. Execute o container
docker run -p 8000:8000 --env-file .env adocao-api
```

---

## Documentação da API (Swagger)

Com o servidor rodando, acesse:

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **ReDoc:** `http://127.0.0.1:8000/api/redoc/`
- **Schema OpenAPI (JSON):** `http://127.0.0.1:8000/api/schema/`

---

## Endpoints principais

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/api/auth/login/` | Login (retorna JWT) | Não |
| POST | `/api/auth/register/` | Cadastro de usuário | Não |
| GET | `/api/auth/me/` | Dados do usuário autenticado | Sim |
| POST | `/api/auth/change-password/` | Alteração de senha | Sim |
| POST | `/api/auth/password-reset/` | Solicitação de recuperação de senha | Não |
| POST | `/api/auth/password-reset/confirm/` | Confirmação de nova senha | Não |
| POST | `/api/auth/token/refresh/` | Renovação do access token | Não |
| GET/POST | `/api/pets/` | Listar e cadastrar pets | Sim |
| GET/PATCH/DELETE | `/api/pets/{id}/` | Detalhe, edição e exclusão de pet | Sim |
| GET/POST | `/api/solicitacoes/` | Listar e criar solicitações de adoção | Sim |
| POST | `/api/solicitacoes/{id}/aprovar/` | Aprovar solicitação (responsável) | Sim |
| POST | `/api/solicitacoes/{id}/recusar/` | Recusar solicitação (responsável) | Sim |
| GET/POST | `/api/favoritos/` | Listar e adicionar favoritos | Sim |
| DELETE | `/api/favoritos/{id}/` | Remover favorito | Sim |
| GET | `/api/dashboard/` | Resumo de métricas por perfil | Sim |
| GET | `/api/health/` | Status da API | Não |

---

## Perfis de usuário

A API suporta dois tipos de usuário, com visões diferentes:

**Adotante**
- Visualiza pets disponíveis
- Solicita, cancela e acompanha suas solicitações de adoção
- Favorita e desfavorita pets
- Vê métricas dos seus próprios registros no painel

**Responsável**
- Cadastra, edita e exclui seus próprios pets
- Aprova ou recusa solicitações de adoção recebidas
- Vê todos os pets e solicitações sob sua responsabilidade no painel

---

## Gerência de senha

O endpoint `POST /api/auth/password-reset/` retorna apenas uma mensagem genérica em produção (para não revelar quais e-mails estão cadastrados). Em modo `DEBUG=True`, a resposta também inclui `uid` e `token` para facilitar testes sem servidor de e-mail configurado.

---

## Telas da aplicação (Frontend)

As imagens abaixo são do frontend que consome esta API:

![Tela de pets disponíveis](docs/screenshot-pets.png)
![Painel de métricas](docs/screenshot-painel.png)
![Swagger UI](docs/screenshot-swagger.png)

---

## O que funcionou

- Autenticação JWT com renovação automática de token
- CRUD completo de pets (com upload de foto)
- Solicitações de adoção com fluxo de aprovação/recusa
- Favoritos por usuário
- Painel com métricas diferenciadas por perfil
- Documentação Swagger via drf-spectacular
- Diferentes visões para adotantes e responsáveis
- Recuperação de senha (uid/token em modo DEBUG)

## O que não funcionou

- Envio de e-mail real para recuperação de senha (não há servidor SMTP configurado; o token é retornado na resposta apenas em DEBUG)
