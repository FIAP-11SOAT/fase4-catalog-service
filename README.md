# 📗 Catalog Service

Este repositório contém o **Catalog Service**, um serviço backend que pode ser executado localmente para desenvolvimento.

Abaixo estão as etapas necessárias para configurar o ambiente e rodar o projeto na sua máquina.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado:

* **Java** (conforme versão utilizada pelo projeto)
* **Docker** e **Docker Compose**
* **Make**
* **Git**
* **Flyway CLI** (instruções abaixo)

---

## Instalação do Flyway (Linux)

O projeto utiliza o **Flyway** para versionamento e execução das migrations do banco de dados. Siga os passos abaixo para instalar o Flyway localmente:

### 1. Download e extração

```bash
wget -qO- https://download.red-gate.com/maven/release/com/redgate/flyway/flyway-commandline/11.19.0/flyway-commandline-11.19.0-linux-x64.tar.gz | tar -xvz
```

### 2. Criar atalho para o executável

```bash
sudo ln -s `pwd`/flyway-11.19.0/flyway /usr/local/bin
```

### 3. Mover para o diretório padrão

```bash
sudo mv flyway-11.19.0 /opt/flyway
```

### 4. Atualizar variável de ambiente

```bash
echo 'export PATH=$PATH:/opt/flyway' >> ~/.bashrc
source ~/.bashrc
```

### 5. Verificar instalação

```bash
flyway -v
```

---
## Configurando o script para gerar o token JWT

No site https://mkjwk.org/ gere um par de chaves pública e privada utilizando a seguinte configuração:

- **Key Size:** 2048
- **Key Use:** Signature
- **Algorithm:** RS256:RSA
- **Key ID:** Specify (`local-dev-key`)
- **Show X.509:** Yes

No bloco **Public and Private Keypair**, copie o campo `n` (chave pública) e cole no arquivo `application-dev.properties` e `application-test.properties` , dentro da configuração `JWT_JWK`, no campo `n`.

No bloco **Private Key (X.509 PEM Format)**, copie todo o conteúdo e crie um arquivo na raiz do projeto com o nome:

```text
private_key.pem
```

É importante que esse arquivo não seja versionado !

Depois que a aplicação estiver rodando, você pode usar o script generate-jwt.sh para gerar os tokens com as roles desejadas para acessar as rotas autenticadas:

ROLE: CUSTOMERS
```bash
./generate-jwt.sh CUSTOMERS
```

ROLE: EMPLOYEES
```bash
./generate-jwt.sh EMPLOYEES
```

## Subindo o projeto localmente

Com o Flyway instalado, execute os comandos do **Makefile** na raiz do projeto, na ordem abaixo:

### 1. Parar serviços existentes (caso estejam rodando)

```bash
make stop
```

### 2. Subir dependências (ex: banco de dados via Docker)

```bash
make start
```

### 3. Executar migrations do banco de dados

```bash
make migrate
```

### 4. Rodar a aplicação em modo desenvolvimento

```bash
make run-dev
```

---

## Acessando o serviço

Após a execução dos comandos acima, o **Catalog Service** estará disponível em:

```
http://localhost:8080
```

## Swagger UI
👉 http://localhost:8080/swagger-ui.html

## Rotas da API

⚠️ **Todas as rotas requerem autenticação via JWT**

### 📌 Categorias

- **GET** `/categories`  
  👥 Roles permitidas:
  - `EMPLOYEES`
  - `CUSTOMERS`

---

### 📌 Produtos

- **GET** `/products?category=1`  
  👥 Roles permitidas:
  - `EMPLOYEES`
  - `CUSTOMERS`

- **POST** `/products`  
  👥 Roles permitidas:
  - `EMPLOYEES`

---

## Observações

* Certifique-se de que a porta **8080** não esteja sendo utilizada por outro serviço.
* Caso ocorram erros de banco de dados, verifique se os containers Docker estão rodando corretamente.
* As migrations ficam sob controle do Flyway e devem ser executadas sempre que houver mudanças no schema.

---

✅ Pronto! O ambiente local do **Catalog Service** estará configurado e rodando.
