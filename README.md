# AgendaReino

Sistema web de gerenciamento de eventos para uma igreja local.

---

## Projeto de Extensão Universitária

**AgendaReino** é um projeto desenvolvido como atividade extensionista do Curso Superior em Tecnologia em Análise e Desenvolvimento de Sistemas (CST ADS), alinhado ao **Programa de Contexto à Comunidade** e à metodologia **PDCA** (Plan, Do, Check, Act).

Este desenvolvimento está fundamentado na **Resolução CNE/CES nº 7/2018**, que estabelece as diretrizes curriculares para cursos de educação superior, destacando a importância de atividades extensionistas que articulem saberes com a comunidade, promovendo transformação social e transferência de conhecimento.

---

## Problema & Solução

**Problema:** A comunidade da igreja local enfrentava falhas críticas de comunicação, com membros e líderes não sendo informados adequadamente sobre eventos, causando baixa participação e desorganização.

**Solução:** Plataforma web centralizada que permite cadastro, visualização e gerenciamento integrado de eventos, garantindo comunicação eficiente entre todos os níveis da organização.

---

## Visão Geral

A **AgendaReino** centraliza todas as informações de eventos em um único lugar, resolvendo a comunicação deficiente entre membros, líderes e pastores. O backend fornece APIs RESTful para criar, ler, atualizar e excluir eventos, além de gerar automaticamente ocorrências de eventos recorrentes com suporte completo a exceções. O frontend oferece uma experiência de usuário funcional com visualização em calendário (redesign visual completo em desenvolvimento para versões futuras).

---

## Tecnologias

### Backend
- **Framework Web**: Flask 3.1.3
- **ORM**: SQLAlchemy 2.0.49
- **Banco de Dados**: PostgreSQL (com psycopg2-binary 2.9.10)
- **Migrations**: Alembic 1.13.2
- **Autenticação**: JWT (PyJWT 2.12.1) – tokens 24h, papéis `admin` e `membro`
- **Validação**: Marshmallow 3.21.3
- **Segurança**: bcrypt 4.2.1
- **CORS**: Flask-CORS 6.0.2
- **Testes**: pytest 9.0.3, pytest-cov 7.1.0
- **Containerização**: Docker & Docker Compose

### Frontend
- **Framework**: Vue.js 3.5.32
- **Roteamento**: Vue Router 5.0.4
- **Gerenciamento de Estado**: Pinia 3.0.4
- **Build Tool**: Vite 8.0.8
- **Linguagem**: TypeScript 6.0.0
- **HTTP Client**: Axios 1.16.1
- **Calendário**: FullCalendar 5.11.5 (com daygrid, timegrid e interaction plugins)
- **Ícones**: Heroicons 2.2.0
- **Testes Unitários**: Vitest 4.1.4
- **Testes E2E**: Playwright 1.59.1
- **Linting**: ESLint 10.2.1, Oxlint 1.60.0
- **Formatação**: Prettier 3.8.3

> **Nota**: O visual do frontend é funcional e operacional no momento. Um **redesign visual completo** está planejado para versões futuras, trazendo melhorias de UX/UI alinhadas ao brand da aplicação.

---

## Estrutura de Diretórios

```
app/
  ├─ config/            # Configurações da aplicação (settings, variáveis de ambiente)
  ├─ controllers/       # Blueprints Flask (rotas e endpoints)
  ├─ db/                # Inicialização e configuração do SQLAlchemy
  ├─ models/            # Definições de tabelas e relacionamentos
  ├─ repositories/      # Camada de acesso ao banco de dados (queries)
  ├─ schemas/           # Serializadores e validação (Marshmallow)
  ├─ services/          # Regras de negócio e lógica de domínio
  └─ utils/             # Funções auxiliares (autenticação, recorrência, validação)

migrations/             # Scripts Alembic para versionamento do banco
tests/                  # Testes unitários e de integração

frontend/
  ├─ src/
  │  ├─ components/     # Componentes Vue reutilizáveis
  │  ├─ views/          # Páginas (rotas principais)
  │  ├─ stores/         # Pinia stores (estado global)
  │  ├─ services/       # Serviços HTTP e utilitários
  │  ├─ router/         # Configuração de rotas
  │  ├─ composables/    # Composables Vue reutilizáveis
  │  └─ assets/         # Estilos globais e temas
  ├─ e2e/               # Testes end-to-end (Playwright)
  ├─ public/            # Assets estáticos
  └─ vite.config.ts     # Configuração do build e dev server
```

---

## Funcionalidades Implementadas

- **Infraestrutura**: Dockerizada com Docker Compose, PostgreSQL em container, Alembic com todas as migrations
- **Models Completos**: `usuarios`, `eventos_normais`, `eventos_recorrentes`, `eventos_excecoes`
- **CRUDs RESTful**: Todas as rotas implementadas com validação via Marshmallow
- **Motor de Recorrência**: Geração dinâmica e inteligente de ocorrências; suporte completo a exceções (cancelamento e remarcação)
- **Agenda Unificada**: Endpoint `GET /agenda` público, ordenado cronologicamente, com exceções aplicadas
- **Autenticação JWT**: Tokens com validade 24h, papéis `admin`/`membro` com autorização por endpoint
- **Testes**: Cobertura de CRUDs, recorrência e integração com banco
- **Frontend Funcional**: Interface em Vue 3 com visualização em calendário, autenticação e gerenciamento de eventos
- **Type Safety**: TypeScript no frontend para maior segurança em tempo de desenvolvimento

---

## Acesso ao Sistema

O sistema está implantado e operacional em ambiente de produção na plataforma Railway.

---

## Licença

Este projeto está licenciado sob a **Licença MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## Contato & Suporte

Para dúvidas, sugestões ou relatos de bugs, abra uma **Issue** no repositório ou entre em contato com a equipe de desenvolvimento.
