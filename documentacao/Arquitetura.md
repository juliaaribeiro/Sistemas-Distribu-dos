# 1. Visão Arquitetônica Inicial (Pré-Modelagem de Ameaças)

## 1.1. Introdução
Este documento descreve a visão arquitetônica inicial para o **ConsultAI Ufla Júnior**.
O objetivo do projeto é desenvolver uma solução centralizada, na forma de um chatbot, para responder às dúvidas frequentes de potenciais clientes da **UFLA Júnior – Empresa Júnior de Consultoria em Administração**, que atualmente enfrentam dificuldades para obter informações rápidas e acessíveis sobre os serviços de consultoria oferecidos.

Este documento foca na arquitetura funcional, servindo como base para a posterior análise de riscos e modelagem de ameaças.

---

## 1.2. Solução Proposta e Componentes
A solução consiste em um sistema distribuído composto pelos seguintes elementos:

- **Frontend**: Uma interface de chat web onde o usuário (potencial cliente) pode interagir, inserindo suas dúvidas.
- **Backend (API)**: Um microserviço que recebe as perguntas do frontend, processa-as e orquestra a comunicação com os agentes de IA.
- **Agente de IA (Ollama - Local)**: Um modelo de linguagem rodando em contêiner Docker, treinado com informações sobre a UFLA Júnior e seus serviços de consultoria.
- **Agente de IA (API Externa)**: Um segundo modelo de IA acessado via API (ex.: OpenAI ou Google), que pode ser usado para complementar respostas ou tratar dúvidas mais genéricas de gestão.
- **Base de Conhecimento**: Um repositório estruturado com informações institucionais e procedimentos da UFLA Júnior.

### Tabela 1: Tecnologias e Componentes

| Componente        | Tecnologia/Framework             | Responsabilidade                                                                 |
|-------------------|----------------------------------|---------------------------------------------------------------------------------|
| Frontend          | CSS HTML JAVASCRIPT            | Interface do usuário (UI) e interação com o chat                                |
| Backend           | Python (FastAPI)                | Lógica de negócio, roteamento de requisições e comunicação com os agentes de IA |
| Agente Local      | Ollama + Docker                 | Processamento de linguagem natural (PLN) com dados da UFLA Júnior               |
| Agente Externo    | API de terceiros (OpenAI, etc.) | Capacidades estendidas de PLN                                                   |
| Base de Conhecimento | JSON estruturado | Fonte de dados confiável sobre serviços, prazos e processos internos            |
| Comunicação       | Protocolo A2A (Agent-to-Agent) via APIs REST | Troca de informações entre frontend, backend e agentes                          |

---

## 1.3. Fluxo de Dados Inicial (DFD - Data Flow Diagram)
O fluxo de dados a seguir descreve como a informação se move através do sistema sem a implementação de controles de segurança avançados.

<p align="center">
  <img src="Usuario.png" alt="Usuário" width="1100"/>
</p>


**DFD do Sistema**

1. **Usuário → Frontend**: O cliente digita uma pergunta na interface do chat.  
2. **Frontend → Backend**: A interface envia a pergunta para a API do Backend via requisição HTTP.  
3. **Backend → Agentes de IA**: O Backend decide se a pergunta será respondida pelo agente local, externo ou ambos.
4. **Agentes de IA → Backend**: Os agentes processam a pergunta e retornam a resposta.  
5. **Backend → Frontend**: O Backend formata a resposta e a envia para o chat.  
6. **Frontend → Usuário**: A resposta é exibida ao cliente no chat em tempo real.  

Como a comunicação entre os agentes de IA possui vulnerabilidades semelhantes, sua análise será condensada em uma categoria única denominada **Agentes de IA** para evitar repetição excessiva.

---
