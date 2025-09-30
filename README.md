# Agent Swarm

## Descrição
Multi-agent system em FastAPI com Router Agent, Knowledge Agent (RAG) e Support Agent.
Integrado com Google Gemini API (via variável de ambiente).

## Deploy
- CI/CD via GitHub Actions
- Hospedado no Render
- Docker multi-stage

## Segurança
- A chave GEMINI_API_KEY é armazenada como Secret (GitHub Actions e Render).

## Passos principais
1. Configure Secrets no GitHub (`GEMINI_API_KEY`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `RENDER_API_KEY`, `RENDER_SERVICE_ID`).
2. Configure `GEMINI_API_KEY` no Render em Environment Variables.
3. Rode o workflow para buildar e deployar.

## Endpoints
- `POST /api/message` -> processa mensagens pelo Agent Swarm.
