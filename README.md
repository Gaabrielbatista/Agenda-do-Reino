# AgendaReino

Sistema web de gerenciamento de eventos para uma igreja local.

## Visão Geral
A **AgendaReino** resolve a falha de comunicação de eventos entre membros, líderes e pastores, centralizando todas as informações em um único lugar. O backend fornece APIs para criar, ler, atualizar e excluir eventos, além de gerar automaticamente ocorrências de eventos recorrentes com suporte a exceções.

## Tecnologias
- **Backend**: Flask
- **ORM**: SQLAlchemy (puro)
- **Banco de Dados**: PostgreSQL (Docker)
- **Migrations**: Alembic
- **Autenticação**: JWT (24 h, papéis `admin` e `membro`)
- **Validação**: Marshmallow
- **Containerização**: Docker & Docker‑Compose

## Estrutura de Diretórios
```
app/
  ├─ config/            # Configurações da aplicação
  ├─ controllers/       # Blueprints Flask (rotas)
  ├─ db/                # Inicialização do SQLAlchemy
  ├─ models/            # Definições das tabelas
  ├─ repositories/      # Acesso ao banco
  ├─ schemas/           # Serializadores/validação (Marshmallow)
  ├─ services/          # Regras de negócio
  └─ utils/             # Funções auxiliares (auth, recurrence, etc.)

migrations/            # Scripts Alembic
tests/                 # Testes unitários e de integração
```

## Funcionalidades Implementadas ✅
- **Infraestrutura**: Docker, PostgreSQL, Alembic com todas as migrations
- **Models**: `usuarios`, `eventos_normais`, `eventos_recorrentes`, `eventos_excecoes`
- **CRUDs completos**: todas as rotas com validação via Marshmallow
- **Motor de recorrência**: geração dinâmica de ocorrências; suporte a exceções (cancelamento e remarcação)
- **Agenda unificada**: `GET /agenda` pública, ordenada, aplicando exceções
- **Autenticação JWT**: tokens de 24 h, papéis `admin`/`membro`
- **Testes**: cobertura de CRUDs e recorrência

## Próxima Feature
- **Frontend** – será desenvolvido em breve para consumir a API.

## Como Executar Localmente
```bash
# Copie as variáveis de ambiente
cp .env.example .env
# Edite .env com as credenciais do PostgreSQL

# Suba a infraestrutura
docker compose up -d --build

# Aplique as migrations
docker compose exec web alembic upgrade head

# Rode a aplicação
docker compose exec web python -m app.app
```

## Testes
```bash
# Dentro do container
docker compose exec web pytest -vv
```

## Contribuição
1. Fork o repositório
2. Crie uma branch para sua feature ou correção
3. Siga o padrão de commits (feat:, fix:, chore:, etc.)
4. Abra um Pull Request

## Licença
Este projeto está licenciado sob a licença MIT.