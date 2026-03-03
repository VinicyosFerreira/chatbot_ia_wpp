# Projeto de Chatbot com AI E RAG

Este é um projeto de chatbot usando uma API Flask e uma interface de webhook para WhatsApp. O chatbot é capaz de receber mensagens do WhatsApp, processá-las usando uma IA e responder às mensagens com base no contexto fornecido utilizando RAG(Retreival Augment Generated).

# Tecnologias
Python - Linguagem para executar scripts e processar dados.

Flask API - API para configurar o webhook e comunicação com chatbot em tempo real.

WAHA - API do Whatsapp gratuita usada com Docker.

Docker e Docker Compose - Criar a infraestrutura do projeto e rodar o Waha e Flask.

Langchain, ChormaDB e HuggingFace - Utilizada para comunicação com LLM, geração de embeddings e registro de banco vetorizado.


## Pré-requisitos
Antes de começar, certifique-se de ter as seguintes ferramentas instaladas:

- Python
- Docker
- Docker Compose
- Documentos para RAG

- OBS: `file_path = '/app/rag/data/docs.pdf`. Pode usar a estrutura para colocar e o caminho no file_path do arquivo `rag.py` 

## Instalação

Siga as etapas abaixo para instalar e executar o projeto:

1. Clone este repositório para o seu ambiente local.

    `git clone <link>`

2. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:
Utilize o `.env.example` como base.


3. Instale as dependências do projeto

    Também use o `.venv` se quiser isolamento e consistência.

    `pip install -r requirements.txt`

4. Crie um Dockerfile na raiz do projeto e adicione o código que está no arquivo `Dockerfile.api` ou modifique
conforme necessário.
 
5. Execute o seguinte comando para construir e iniciar os contêineres:

    `docker-compose up -d`

6. Inserindo RAG para o chatbot. Entre no container via exec

    `docker exec -it <container-name-or-id> /bin/bash`
    
    Caso não esteja na pasta app, rode esse 3 comandos, se estiver ja na pasta `app` rode os 2 últimos

    `cd app`
    `cd rag`
    `python rag.py`

    Para sair do modo exec digite: `exit`

    Ele gerára um chroma-data com binários e um sql vetorizado.

7. Agora rode acesse o Waha na porta localhost:3000 e termine a configuração use como guia a doc: `https://waha.devlike.pro/`. O servidor em Flask estará rodando na porta 5000.

## Como testar
O processo é bem simples no .env.example eu usei dois números particulares para teste, mas pode usar apenas um ou não definir eu usei para controle de mensagens para evitar que o bot envie mensagens apenas para os números permitidos.
- `PHONE_NUMBER1 = 999999999999@c.us`
- `PHONE_NUMBER2 = 888888888888@c.us`

Ao rodar o servidor e configurar o Waha e ele aparecer **IN_WORKING**, mande mensagem para o bot com número configurado e veja o resultado.
