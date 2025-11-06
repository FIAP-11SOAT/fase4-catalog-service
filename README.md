# Catálogo Fase 4 – Microsserviço de Categorias (Python + FastAPI)

Este repositório contém um microsserviço em Python que implementa o CRUD de categorias.

## Endpoints

- GET `/categories` – Lista categorias; retorna 404 e `[]` se vazio
- GET `/categories/{id}` – Busca por ID; retorna 404 e `[]` se não existir
- POST `/categories` – Cria categoria (requer cabeçalho `X-Role: admin`)
- PUT `/categories/{id}` – Atualiza categoria (requer `X-Role: admin`)
- DELETE `/categories/{id}` – Remove categoria (requer `X-Role: admin`)
- GET `/health` – Healthcheck simples

## Rodando localmente

Recomendado para desenvolvimento rápido.

1. Crie e ative um virtualenv (Windows):

```cmd
py -3 -m venv .venv
.\.venv\Scripts\activate
```

2. Instale dependências:

```cmd
.\.venv\Scripts\pip install -r requirements.app.txt
```

3. Configure a variável de conexão ao Postgres:

```cmd
set DATABASE_URL=postgresql+psycopg2://usuario:senha@host:5432/nomebd
```

4. Rode a aplicação com Uvicorn:

```cmd
.\.venv\Scripts\python -m uvicorn app.main:app --reload
```

5. Teste o health:

```cmd
curl http://localhost:8000/health
```

### Migrations

Os scripts em `migrations/*.sql` são aplicados automaticamente pela aplicação em startup (idempotente).

## Deploy na AWS

### Deploy Automático via GitHub Actions (Recomendado)

#### Pré-requisitos

1. **Configure o secret no GitHub**:
   - Vá em: `Settings > Secrets and variables > Actions`
   - Clique em "New repository secret"
   - Nome: `AWS_ROLE_TO_ASSUME`
   - Valor: Execute `terraform output github_actions_role_arn` no diretório `infra/`
   - Exemplo: `arn:aws:iam::ACCOUNT_ID:role/github-actions-deploy-role`

#### Como fazer deploy

1. Faça suas mudanças no código
2. Commit e push:

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feat/catalog-service
```

3. O GitHub Actions vai automaticamente:
   - Instalar dependências Python
   - Criar pacote ZIP
   - Upload para S3
   - Executar Terraform Apply
   - Atualizar Lambda

4. Acompanhe o progresso em: `Actions` tab no GitHub

### Deploy Manual (Desenvolvimento Local)

#### Pré-requisitos

- AWS CLI configurado
- Python 3.11
- Terraform instalado

#### Passo a passo

```bash
# 1. Build do pacote Lambda
python -m pip install --upgrade pip
pip install -r requirements.app.txt -t build/package
cp -R app build/package/
cp -R migrations build/package/
cd build/package
zip -r ../../lambda-package.zip .
cd ../..

# 2. Upload para S3 (ajuste o bucket name)
aws s3 cp lambda-package.zip s3://fase4-catalog-service-ACCOUNT_ID-us-east-1-artifacts/releases/manual.zip

# 3. Aplicar Terraform
cd infra
terraform apply -var="artifact_key=releases/manual.zip"
```

### Verificar Deploy

```bash
# Ver informações da Lambda
aws lambda get-function --function-name fase4-catalog-service

# Obter URL da API
cd infra && terraform output api_url

# Testar
curl https://SUA_API_URL/health
```

### Troubleshooting

**Erro: "Value '' at 'code.s3Key' failed to satisfy constraint"**

- **Causa**: Tentou criar a Lambda sem ter feito upload do ZIP para o S3
- **Solução**: Execute o passo de build e upload primeiro, ou faça push no GitHub

**Erro: "AccessDenied" no GitHub Actions**

- **Causa**: Secret `AWS_ROLE_TO_ASSUME` não configurado ou inválido
- **Solução**: Execute `terraform output github_actions_role_arn` e configure o secret no GitHub

### Estrutura do Deploy

```
GitHub Push → GitHub Actions → Build ZIP → Upload S3 → Terraform Apply → Lambda Updated
```

## Arquitetura

- **Lambda Function**: Runtime Python 3.11, empacotada como ZIP no S3
- **API Gateway**: HTTP API fazendo proxy para a Lambda
- **RDS PostgreSQL**: Banco de dados gerenciado
- **VPC**: Lambda e RDS em VPC privada com security groups
- **S3**: Bucket de artefatos com versionamento habilitado
- **IAM**: Roles com OIDC para GitHub Actions

## Estrutura do Projeto

```
fase4-catalog-service/
├── app/                         # Código da aplicação
│   ├── main.py                 # Handler da Lambda
│   ├── models.py               # Modelos SQLAlchemy
│   ├── schemas.py              # Schemas Pydantic
│   ├── db.py                   # Conexão com banco
│   ├── security.py             # Middleware de autenticação
│   ├── core/                   # Configurações
│   └── routes/                 # Endpoints
├── infra/                       # Terraform
│   ├── main.tf                 # Lambda, API Gateway
│   ├── rds.tf                  # RDS PostgreSQL
│   ├── networking.tf           # VPC, Subnets, SGs
│   ├── iam-oidc.tf             # IAM Roles com OIDC
│   ├── variables.tf
│   └── outputs.tf
├── migrations/                  # SQL scripts
│   └── 0001_create_product_categories.sql
├── .github/workflows/
│   └── deploy.yml              # CI/CD automático
├── requirements.app.txt         # Dependências Lambda
└── README.md
```

## Próximos Passos

- [ ] Configurar backend remoto do Terraform (S3 + DynamoDB)
- [ ] Armazenar segredos no AWS Secrets Manager
- [ ] Adicionar testes automatizados
- [ ] Configurar monitoramento com CloudWatch Alarms

