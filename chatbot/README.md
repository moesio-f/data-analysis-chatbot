# Chatbot Engine

Esse diretório contém o código fonte para o _motor_ do Chatbot usando `LangChaing`. Esse serviço é organizado como uma biblioteca e possui um componente que inicializa a API para comunicação com outros serviços. Para um quickstart, leia o [README do repositório](../README.md).

## Variáveis de Ambiente

O motor permite as seguintes variáveis de ambiente:

| Variável | Descrição | Valor Padrão |
| --- | --- | --- |
| | | |


## Estrutura

- [`chat`](./chat): raiz da biblioteca;
    - [`api`](./chat/api): RESTFul API com `FastAPI`;
    - [`agents`](./chat/agents): definição dos diferentes agentes;
    - [`tools`](./chat/tools): definição das ações que os agentes podem tomar no sistema;
    - [`connectors`](./chat/connectors): conectores para fontes de dados externos;
- [`tests`](./tests): testes da biblioteca usando `pytest`;
    - Testes unitários e de integração;
