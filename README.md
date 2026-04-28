# 🚗 Vehicle Infraction API

API REST para consulta e persistência de infrações veiculares, integrada à API do SENATRAN via Infosimples. Desenvolvida com foco em boas práticas de arquitetura, autenticação segura e containerização.

---

## 🛠️ Stack

- **Python 3.11** + **FastAPI**
- **PostgreSQL** + **SQLAlchemy** (ORM síncrono)
- **Alembic** — migrations
- **JWT** — autenticação via HTTPBearer
- **httpx** — chamadas HTTP externas
- **pytest** — testes automatizados com SQLite in-memory
- **Docker** + **Docker Compose**

---

## 🏗️ Arquitetura

O projeto segue arquitetura em camadas com separação clara de responsabilidades:

```
Router → Service → Repository → Model
              ↓
           Gateway (API externa)
              ↓
            DTOs (mapeamento de resposta)
```

```
app/
├── core/           # Configurações, banco, dependências, segurança, logging
├── models/         # Modelos SQLAlchemy (User, Vehicle, Infractions, InfractionQueries)
├── schemas/        # Schemas Pydantic (input/output + APIResponse genérico)
├── repositories/   # Acesso ao banco de dados
├── services/       # Regras de negócio
├── gateways/       # Comunicação com a API do SENATRAN (Infosimples)
├── dtos/           # Mapeamento das respostas externas
├── routers/        # Endpoints FastAPI
├── domain/         # Exceções de domínio
└── api/            # Exception handlers globais
```

Todas as respostas seguem um envelope padronizado:

```json
{
  "success": true,
  "message": "Veículos retornados com sucesso",
  "data": [...]
}
```

---

## 🚀 Como rodar

### Pré-requisitos

- Docker e Docker Compose instalados
- Conta e token na [Infosimples](https://infosimples.com.br) com acesso à API do SENATRAN
- Credenciais GOV.BR para consulta

### 1. Clone o repositório

```bash
git clone https://github.com/paulodsv/vehicle-infraction-api.git
cd vehicle-infraction-api
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais (veja a seção [Variáveis de Ambiente](#-variáveis-de-ambiente)).

### 3. Suba os containers

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`.

### 4. Execute as migrations

```bash
docker-compose exec app alembic upgrade head
```

---

## 💻 Rodando localmente (sem Docker)

### Pré-requisitos

- Python 3.11+
- PostgreSQL rodando localmente

```bash
# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure o .env com DATABASE_URL apontando para localhost

# Execute as migrations
alembic upgrade head

# Suba a aplicação
uvicorn main:app --reload
```

---

## 🧪 Testes

```bash
pytest
```

Os testes utilizam SQLite in-memory com rollback por fixture — nenhuma alteração persiste entre os testes.

---

## 📋 Endpoints principais

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/auth/register` | Cadastro de usuário | ❌ |
| POST | `/auth/login` | Login e geração de token JWT | ❌ |
| GET | `/health` | Status da API e do banco | ❌ |
| POST | `/vehicles/` | Cadastra um veículo | ✅ |
| GET | `/vehicles/` | Lista veículos com filtros | ✅ |
| GET | `/vehicles/{plate}` | Busca veículo por placa | ✅ |
| PATCH | `/vehicles/` | Atualiza um veículo | ✅ |
| GET | `/infractions/{plate}` | Infrações persistidas por placa | ✅ |
| GET | `/infractions/queries/{user_id}` | Consultas realizadas por usuário | ✅ |
| GET | `/infractions/queries/{query_id}/infractions` | Infrações de uma consulta específica | ✅ |
| POST | `/senatran/infractions` | Consulta infrações via SENATRAN | ✅ |
| POST | `/senatran/consult-fleet` | Consulta frota completa | ✅ |
| POST | `/senatran/fetch-details` | Detalhes de uma infração | ✅ |

A documentação interativa completa está disponível em `http://localhost:8000/docs`.

---

## 🔑 Variáveis de Ambiente

```env
# Banco de dados
DATABASE_URL=postgresql://user:password@localhost:5432/vehicle_infraction_db

# JWT
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Infosimples
INFOSIMPLES_TOKEN=seu_token
INFOSIMPLES_INFRACTIONS_URL=https://...
INFOSIMPLES_DETAILS_URL=https://...

# GOV.BR
GOV_CPF=seu_cpf
GOV_SENHA=sua_senha

# Logging
LOG_LEVEL=INFO
```

---

## 📝 Licença

Este projeto está sob a licença MIT.
