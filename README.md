# Catálogo Fase 4 – Microsserviço de Categorias (Python + FastAPI)

Este repositório agora contém um microsserviço em Python que implementa o CRUD de categorias conforme o documento da Fase 4 e os handlers/rotas em Go no diretório `docs/`.

Endpoints expostos:

- GET `/categories` – Lista categorias; retorna 404 e `[]` se vazio
- GET `/categories/{id}` – Busca por ID; retorna 404 e `[]` se não existir
- POST `/categories` – Cria categoria (requer cabeçalho `X-Role: admin`)
- PUT `/categories/{id}` – Atualiza categoria (requer `X-Role: admin`)
- DELETE `/categories/{id}` – Remove categoria (requer `X-Role: admin`)
- GET `/health` – Healthcheck simples

Observação: Implementação inicial usa armazenamento em memória para simplificar. É fácil trocar por um banco (ex.: SQLite/Postgres) depois.

## Rodando com Docker

Foi adicionado um `Dockerfile` que usa apenas as dependências necessárias através do arquivo `requirements.app.txt` (evita os pacotes do Anaconda do `requirements.txt`).

Passos (Windows, cmd.exe):

1. Build da imagem
   - opcional
   - docker build -t fase4-catalog:latest .

2. Executar o container
   - opcional
   - docker run --rm -p 8000:8000 fase4-catalog:latest

Após subir, a API ficará em: `http://localhost:8000`.

## Rodando com Docker Compose

Suba app + Postgres com um único comando:

- opcional
- docker compose up -d --build

Isso vai disponibilizar:

- API: <http://localhost:8000>
- Postgres: localhost:5432 (db: `catalogdb`, user: `app_user`, senha: `app_password`)
  
Nota: o `docker-compose.yml` do projeto expõe o Postgres na porta host `5432` e cria o usuário `app_user` com senha `app_password` para o banco `catalogdb`.

Para ver logs:

- opcional
- docker compose logs -f

Para parar e remover containers (mantendo os dados no volume `pgdata`):

- opcional
- docker compose down

Variáveis de ambiente (BD Postgres):

- `DATABASE_URL` (opcional, default local): `postgresql+psycopg2://usuario:senha@host:5432/nomebd`

Exemplo (definindo a URL do BD no run):

- opcional
- docker run --rm -p 8000:8000 -e DATABASE_URL="postgresql+psycopg2://postgres:postgres@seu-host:5432/postgres" fase4-catalogo:latest
 - opcional
 - docker run --rm -p 8000:8000 -e DATABASE_URL="postgresql+psycopg2://app_user:app_password@host.docker.internal:5432/catalogdb" fase4-catalogo:latest

Observação: ao rodar o container da aplicação isoladamente no Windows e querer conectar ao Postgres que está na máquina host, use `host.docker.internal` como hostname (ou a rede/host apropriada). Se estiver usando o Postgres em outro container na mesma rede (docker compose), prefira executar via `docker compose up`.

Segurança: não comite senhas em texto plano no repositório. Para ambientes reais, use um arquivo `.env` (adicionado ao `.gitignore`) ou variáveis de ambiente no provedor/CI.

## Exemplos de uso (via curl)

Os comandos abaixo são apenas exemplos opcionais para testar localmente:

1. Healthcheck
   - opcional
   - curl -s <http://localhost:8000/health>

2. Listar categorias (vazio retorna 404 e [])
   - opcional
   - curl -i <http://localhost:8000/categories>

3. Criar categoria (requer papel admin)
   - opcional
   - curl -i -X POST <http://localhost:8000/categories> -H "Content-Type: application/json" -H "X-Role: admin" -d "{\"name\": \"Lanches\"}"

4. Buscar por ID
   - opcional
   - curl -i <http://localhost:8000/categories/1>

5. Atualizar
   - opcional
   - curl -i -X PUT <http://localhost:8000/categories/1> -H "Content-Type: application/json" -H "X-Role: admin" -d "{\"name\": \"Bebidas\"}"

6. Deletar
   - opcional
   - curl -i -X DELETE <http://localhost:8000/categories/1> -H "X-Role: admin"

## Estrutura relevante

- `app/main.py` – FastAPI com CRUD de categorias
- `Dockerfile` – Container da aplicação
- `requirements.app.txt` – Dependências mínimas do container
- `docs/` – Referência dos handlers/rotas em Go utilizados como base

## Notas e próximos passos

- Caso deseje persistência real, podemos adicionar SQLite/SQLAlchemy (ou Postgres) e um `docker-compose.yml` com banco.
- A autorização foi simplificada via header `X-Role: admin` para espelhar o `RequireAdminRole()` utilizado em Go.

