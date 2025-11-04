# Catálogo Fase 4 – Microsserviço de Categorias (Python + FastAPI)

Este repositório contém um microsserviço em Python que implementa o CRUD de categorias.

Endpoints expostos:

- GET `/categories` – Lista categorias; retorna 404 e `[]` se vazio
- GET `/categories/{id}` – Busca por ID; retorna 404 e `[]` se não existir
- POST `/categories` – Cria categoria (requer cabeçalho `X-Role: admin`)
- PUT `/categories/{id}` – Atualiza categoria (requer `X-Role: admin`)
- DELETE `/categories/{id}` – Remove categoria (requer `X-Role: admin`)
- GET `/health` – Healthcheck simples

Observação: A API usa Postgres via SQLAlchemy e aplica o schema/dados iniciais a partir de arquivos SQL em `migrations/`.

## Rodando localmente (sem Docker)

Recomendado para desenvolvimento rápido.

1. Crie e ative um virtualenv (Windows, cmd.exe):

```cmd
py -3 -m venv .venv
.\.venv\Scripts\activate
```

1. Instale dependências mínimas (usado em produção / deploy):

```cmd
.\.venv\Scripts\pip install -r requirements.app.txt
```

1. Configure a variável de conexão ao Postgres. Se quiser usar um Postgres local, informe a URL:

```cmd
set DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/nomebd
```

1. Rode a aplicação com Uvicorn:

```cmd
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

1. Teste o health:

```cmd
curl -s http://localhost:8000/health
```

Se quiser usar um Postgres em container só para o banco (opção): suba um Postgres com Docker separadamente e aponte `DATABASE_URL` para ele; mas o repositório **não** usa Docker para deploy — apenas para conveniência local se você desejar.

### Migrations

- Os scripts em `migrations/*.sql` são aplicados automaticamente pela aplicação em startup (idempotente). Para garantir aplicação completa do schema, gerencie o banco ou recrie o schema conforme necessário.

## Deploy na AWS (Terraform + Lambda ZIP)

O deploy na AWS é feito via Terraform: a pipeline empacota dependências e código num `.zip`, envia para um bucket S3 de artefatos e configura a Lambda (runtime Python 3.11) apontando para esse artefato. Um API Gateway (HTTP API) faz proxy das requisições para a Lambda.

Arquivos relevantes:

- `infra/` – Terraform que cria o bucket de artefatos, role IAM, função Lambda (ZIP), API Gateway HTTP API, permissões e Log Group.
- `.github/workflows/deploy.yml` – pipeline que empacota as dependências + código, carrega para S3 e aplica o Terraform.

Pré-requisitos:

1. AWS account e permissões adequadas para criar recursos.
2. GitHub Actions com OIDC (recomendado) ou secrets AWS (alternativa menos segura).

Setup rápido (push para `main`):

1. Configure secrets no GitHub (Settings > Secrets and variables > Actions):
   - `AWS_ROLE_TO_ASSUME` (ARN de uma role com permissões para o repo, se usar OIDC)
   - `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASS`
   - Opcional VPC: `VPC_SUBNET_IDS_CSV`, `VPC_SECURITY_GROUP_IDS_CSV`

2. Faça push no branch configurado (`main`) ou dispare o workflow manualmente.

3. O workflow fará:
   - `terraform apply -target=aws_s3_bucket.artifacts -target=aws_s3_bucket_versioning.artifacts` para garantir o bucket
   - empacotar dependências + app em `artifact.zip` e subir para S3 (key `releases/${sha}.zip`)
   - aplicar Terraform com `artifact_key` e `artifact_object_version` para atualizar a Lambda

4. Ao final, o job imprime `api_url` (endpoint do API Gateway). Teste:

```cmd
curl -s https://SEU_API_URL/health
```

Observações:

- A Lambda precisa conseguir acessar o banco (RDS). Em produção, associe a função a uma VPC com subnets e security groups que permitam acesso ao RDS.
- O `requirements.app.txt` inclui `mangum`, `SQLAlchemy` e `psycopg2-binary`.
- O Terraform por padrão usa estado local em `infra/terraform.tfstate`. Para equipes, recomendo configurar backend S3 + DynamoDB para lock.

## Estrutura relevante

- `app/` – código da aplicação (FastAPI)
- `infra/` – código Terraform para provisionamento na AWS
- `requirements.app.txt` – dependências usadas no deploy da Lambda

## Próximos passos sugeridos

- Configurar backend remoto do Terraform (S3 + DynamoDB)
- Armazenar segredos sensíveis no AWS Secrets Manager e fazer a Lambda acessar via IAM
- Se preferir, posso adicionar a criação da role OIDC via Terraform e um `backend.tf` para o estado remoto

---

Se quiser que eu remova fisicamente os arquivos Docker do repositório (git rm), eu posso fazer esse commit também — preferi deixar mensagens de deprecated nos arquivos por enquanto. Quer que eu os remova totalmente do repo?

