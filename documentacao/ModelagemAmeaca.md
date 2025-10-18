# 2. Modelagem de Ameaças e Estratégias de Mitigação

## 2.1. Metodologia de Análise

Para a identificação e categorização de ameaças, este projeto adota o modelo **STRIDE**, uma metodologia que foca em seis categorias de ameaças à segurança.

- **S**poofing (Falsificação de Identidade): Fingir ser algo ou alguém que não é.
- **T**ampering (Violação de Dados): Modificar dados sem autorização.
- **R**epudiation (Negação de Ações): Negar ter realizado uma ação.
- **I**nformation Disclosure (Exposição de Informações): Expor informações a quem não tem permissão.
- **D**enial of Service (Negação de Serviço): Derrubar ou degradar um serviço para usuários legítimos.
- **E**levation of Privilege (Elevação de Privilégio): Obter capacidades ou acesso sem a devida autorização.

## 2.2. Superfície de Ataque

A superfície de ataque do sistema **ConsultAI Ufla Júnior** inclui os seguintes pontos de interação:

- A interface web do chatbot (Frontend).
- A API pública do Backend (FastAPI).
- O agente de IA local executado via Docker (Ollama).
- O agente de IA externo acessado via API.
- A Base de Conhecimento utilizada para compor respostas.
- A comunicação entre os componentes internos (A2A).

## 2.3. Matriz de Análise de Ameaças STRIDE

### Tabela 2: Matriz de Análise de Ameaças STRIDE

| Componente | Spoofing | Tampering | Repudiation | Information Disclosure | Denial of Service | Elevation of Privilege |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Frontend (Chat Web)** | Criação de página falsa para capturar interações. | Injeção de scripts maliciosos (XSS). | - | Exposição de respostas com dados sensíveis. | - | - |
| **Backend API (FastAPI)** | Requisições forjadas (CSRF ou request spoofing). | Manipulação de parâmetros e rotas. | Usuário nega ter enviado requisição por falta de logs. | Acesso indevido a dados ou respostas de outros usuários. | Sobrecarga por requisições automáticas (DDoS). | Obtenção de privilégios administrativos. |
| **Agente Local (Ollama / Docker)** | - | Alteração não autorizada do modelo ou do prompt. | - | Extração de informações internas via prompt injection. | Sobrecarga com prompts pesados. | Escalada de privilégios no host via container. |
| **Agente Externo (LLM via API)** | Uso indevido de credenciais de API. | Manipulação de respostas por ataque intermediário. | - | Vazamento de informações sensíveis enviadas ao provedor. | Indisponibilidade causada por abuso. | - |
| **Base de Conhecimento (JSON / Arquivos)** | - | Alteração não autorizada das informações exibidas aos usuários. | - | Exposição de informações internas ou dados incorretos. | - | - |
| **Comunicação (Backend ↔ IA / A2A)** | Serviço malicioso se passando por agente legítimo. | Alteração de respostas em trânsito (Man-in-the-Middle). | - | Vazamento por tráfego não criptografado. | Interrupção da comunicação entre serviços. | - |

## 2.4. Matriz de Risco

### Tabela 3: Matriz de Risco

| ID | Componente | Ameaça (STRIDE) | Descrição da Ameaça | Probabilidade (Score) | Impacto (Score) | Pontuação de Risco |
| :-- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | Backend API | Denial of Service | Ataques de sobrecarga (DDoS) na API. | Alta (15) | Médio (10) | **150** |
| **02** | Agente Local | Denial of Service | Sobrecarga do modelo com requisições complexas. | Alta (15) | Médio (10) | **150** |
| **03** | Comunicação (A2A) | Tampering | Interceptação e alteração das respostas. | Média (10) | Alto (15) | **150** |
| **04** | Backend API | Spoofing | Requisições forjadas (CSRF ou ataques externos). | Alta (15) | Médio (10) | **150** |
| **05** | Base de Conhecimento | Tampering | Alteração não autorizada do conteúdo exibido aos usuários. | Média (10) | Médio (10) | **100** |
| **06** | Frontend | Tampering | Injeção de scripts maliciosos (XSS). | Média (10) | Baixo (5) | **50** |
| **07** | Agente Local | Information Disclosure | Extração de informações sensíveis via prompt injection. | Média (10) | Médio (10) | **100** |
| **08** | Backend API | Repudiation | Usuário/serviço nega ter enviado requisição. | Alta (15) | Baixo (5) | **75** |
| **09** | Backend API | Elevation of Privilege | Obter acesso administrativo por falhas na API. | Baixa (5) | Alto (15) | **75** |
| **10** | Comunicação | Denial of Service | Interrupção da comunicação entre serviços. | Baixa (5) | Médio (10) | **50** |

## 2.5. Sumário dos Riscos Críticos

Com base na análise realizada, os riscos mais críticos para o sistema são:

1. **Prompt Injection e manipulação de respostas nos agentes de IA.**
2. **Vazamento de informações durante a comunicação entre os serviços.**
3. **Negação de serviço (DoS) na API ou nos agentes de IA.**
4. **Alteração não autorizada da Base de Conhecimento, impactando a confiabilidade das respostas.**

