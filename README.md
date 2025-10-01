# Agent Swarm

## Descrição
Multi-agent system em FastAPI com Router Agent, Knowledge Agent (RAG) e Support Agent.
Integrado com Google Gemini API (via variável de ambiente).
Agente conversacional que responde perguntas sobre os produtos e serviços da InfinitePay.

## Deploy
- CI/CD via GitHub Actions
- Hospedado no Render
- Docker multi-stage

## Segurança
- A chave GEMINI_API_KEY é armazenada como Secret (GitHub Actions e Render).

## Passos principais
1. Secrets configurados no GitHub (`GEMINI_API_KEY`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`, `RENDER_API_KEY`, `RENDER_SERVICE_ID`).
2. Configurada `GEMINI_API_KEY` no Render em Environment Variables.
3. Rode o workflow para buildar e deployar.

## Endpoints
- `POST /api/message` -> processa mensagens pelo Agent Swarm.



## 🚀 Rodando localmente com Docker

### 1️⃣ Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- Chave da API Gemini (`GEMINI_API_KEY`)
- Clonar este repositório:


git clone https://github.com/umsimplesjogador/agent-swarm-infinitypay.git
cd agent-swarm-infinitypay



---

## 🛠 Instruções para rodar o projeto localmente sem Docker

### Instal as dependências

pip install -r requirements.txt


### Criar arquivo `.env`

Na raiz do projeto, crie o arquivo `.env` com sua chave da Gemini API:

GEMINI_API_KEY=sua_chave_aqui


### Execute a aplicação

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


### Acesse a aplicação:

Frontend chat: http://localhost:8000/chat

Swagger UI: http://localhost:8000/docs


## Rodar com Docker

1- Construir a imagem
2- Na raiz do projeto, execute: docker build -t agent-swarm .
3- Execute o container: docker run -p 10000:8000 --env GEMINI_API_KEY="sua_chave_aqui" agent-swarm
4- Acessar a aplicação em: Frontend chat: http://localhost:8000/chat e Swagger UI: http://localhost:8000/docs


### Encerrar o container

docker ps          # lista containers em execução
docker stop <ID>   # encerra container


## CI/CD (GitHub Actions + DockerHub + Render)


O projeto possui workflow deploy.yml configurado:

Executa testes com pytest

Constrói a imagem Docker

Faz push para DockerHub

Realiza deploy no Render

Secrets necessários:

DOCKER_USERNAME → usuário DockerHub

DOCKER_PASSWORD → senha DockerHub

RENDER_SERVICE_ID → ID do serviço no Render

RENDER_API_KEY → API key do Render


## Dicas

Sempre use variáveis de ambiente para proteger sua chave da Gemini API.

Para atualizar o agente, reconstrua a imagem Docker.

Para acompanhar logs em tempo real: docker logs -f <CONTAINER_ID>

O chat HTML consome o endpoint /process.

Teste endpoints rapidamente pelo Swagger UI /docs.


