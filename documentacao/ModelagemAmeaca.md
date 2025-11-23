MODELAGEM DE AMEAÇAS – ConsultAI UFLA Júnior
1. Introdução

Este documento apresenta a modelagem de ameaças do sistema ConsultAI UFLA Júnior, chatbot desenvolvido para auxiliar potenciais clientes da UFLA Júnior – Empresa Júnior de Consultoria em Administração – fornecendo respostas rápidas e confiáveis sobre seus serviços, prazos e processos internos.

A modelagem segue a metodologia STRIDE, amplamente utilizada em sistemas distribuídos, e tem como objetivo:

Identificar vulnerabilidades presentes no fluxo de dados e nos componentes do sistema.

Avaliar probabilidade, impacto e risco das ameaças.

Propor medidas de mitigação.

Calcular risco residual após as medidas implementadas.

Esta análise complementa a visão arquitetônica inicial e auxilia na definição de controles de segurança mais adequados ao ecossistema do projeto.

2. Metodologia Utilizada – STRIDE

A metodologia STRIDE classifica ameaças em seis categorias:

Categoria	Significado	Exemplos
S – Spoofing	Falsificação de identidade	Roubo de sessão, uso indevido de API key
T – Tampering	Manipulação de dados	Alteração do JSON da base de conhecimento
R – Repudiation	Negação de ações	Falta de logs ou auditoria
I – Information Disclosure	Divulgação indevida	Vazamento para API externa
D – Denial of Service	Negação de Serviço	Travamento do Ollama por carga excessiva
E – Elevation of Privilege	Elevação de privilégio	Escape do container Docker

A análise é aplicada aos fluxos do DFD (Data Flow Diagram) e aos componentes da arquitetura:

Frontend

Backend (FastAPI)

Agente Local (Ollama)

Agente Externo (API de terceiros)

Base de Conhecimento

Comunicação A2A

3. Fluxo de Dados Considerado (DFD Resumido)

O DFD utilizado como base representa o fluxo de comunicação entre o usuário, o frontend, o backend e os agentes de IA. Ele é essencial para identificar pontos onde podem ocorrer:

Interceptações

Alterações

Abusos de funcionalidade

Vazamentos

Falhas de integridade

O fluxo considerado é:

Usuário → Frontend: Envia pergunta

Frontend → Backend: Envia requisição HTTP

Backend → Agentes de IA (Local/Externo): Processamento

Agentes → Backend: Resposta processada

Backend → Frontend

Frontend → Usuário

A modelagem de ameaças foi construída analisando cada ponto deste fluxo.

4. Processo de Modelagem

O processo seguiu as etapas:

Identificação dos ativos

Informações da UFLA Júnior

Base de Conhecimento

Respostas geradas pelo modelo

Sessões de usuário

API Keys

Logs do sistema

Identificação dos componentes do sistema

Frontend (UI do chat)

Backend

Agente Local (Ollama + Docker)

Agente Externo

Base de Conhecimento

Canal de comunicação A2A

Mapeamento do DFD
– Identificação dos fluxos de dados, limites de confiança e interações críticas.

Análise STRIDE por componente
– Ameaças foram identificadas em cada fluxo e parte do sistema.

Cálculo de risco (Prob. × Impacto)
– Matriz de risco fornecida pelo professor.

Proposição de controles de mitigação
– Focados na redução de probabilidade e impacto.

Cálculo do risco residual
– Após medidas aplicadas.

5. Tabela de Ameaças (Completa – STRIDE)

A tabela abaixo contém toda a modelagem solicitada:

| ID | Vulnerabilidade                         | Fluxo DFD                             | Classe STRIDE              | Descrição da Ameaça                                                                 | Prob. | Impacto | Risco | Medida de Mitigação                                                                                 | Prob. Residual | Impacto Residual | Risco Residual |
|----|------------------------------------------|----------------------------------------|----------------------------|---------------------------------------------------------------------------------------|-------|---------|--------|-------------------------------------------------------------------------------------------------------|----------------|-------------------|-----------------|
| 1  | Prompt Injection                         | Frontend → Backend → Agentes IA        | Tampering                  | Usuário manipula prompt para quebrar regras ou revelar informações internas.         | 15    | 15      | 225    | Sanitização; filtros; prompts seguros; pós-validação.                                                 | 5              | 10                | 50              |
| 2  | Vazamento para API externa               | Backend → Agente Externo               | Information Disclosure     | Backend envia informações não-anonimizadas ao provedor de IA.                        | 10    | 15      | 150    | Anonimização; criptografia; envio mínimo de dados; política de não retenção.                          | 5              | 10                | 50              |
| 3  | XSS (injeção no chat)                    | Frontend                                | Tampering / Info Disclosure| Scripts maliciosos inseridos na UI do chat.                                           | 15    | 10      | 150    | Escapagem de HTML; CSP; sanitização; bibliotecas seguras.                                            | 5              | 5                 | 25              |
| 4  | Sequestro de Sessão                      | Frontend → Backend                      | Spoofing                   | Atacante usa token/cookie roubado para se passar por outro usuário.                  | 10    | 15      | 150    | Cookies HttpOnly/Secure; expiração curta; MFA para admins.                                           | 5              | 10                | 50              |
| 5  | DoS no Agente Local (Ollama)             | Frontend → Backend → Agentes IA         | DoS                        | Requisições excessivas travam o container.                                            | 10    | 15      | 150    | Rate limiting; filas; circuit breaker; limitar CPU/RAM via Docker.                                   | 5              | 10                | 50              |
| 6  | Escape de Container                      | Agentes IA (Docker)                     | Elevation of Privilege     | Vulnerabilidade no container concede acesso ao host.                                 | 10    | 15      | 150    | Seccomp; AppArmor; usuário não-root; atualização de imagens.                                          | 5              | 10                | 50              |
| 7  | Alteração indevida da Base de Conhecimento| Backend → Base de Conhecimento         | Tampering                  | JSON alterado causa respostas incorretas.                                             | 5     | 15      | 75     | Controle de versão; ACL; assinatura; auditoria.                                                        | 5              | 10                | 50              |
| 8  | Acesso não autorizado à base             | Backend → Base de Conhecimento          | Info Disclosure            | Acesso não permitido a dados internos.                                                | 10    | 10      | 100    | Criptografia; controle de acesso; logs.                                                               | 5              | 5                 | 25              |
| 9  | Vazamento de API Key                     | Backend → API Externa                   | Spoofing/Tampering         | Chaves expostas permitem uso indevido ou ataques.                                     | 10    | 10      | 100    | Secrets Manager; rotacionamento; variáveis de ambiente seguras.                                      | 5              | 5                 | 25              |
| 10 | Ausência de logs (repudiação)            | Backend                                 | Repudiation                | Falta de rastreabilidade das ações.                                                   | 10    | 10      | 100    | Logs imutáveis; timestamps; IDs de requisição; SIEM.                                                  | 5              | 5                 | 25              |
| 11 | MITM na comunicação A2A                  | Backend ↔ Agentes IA                     | Info Disclosure/Tampering | Interceptação de tráfego entre serviços.                                              | 10    | 15      | 150    | TLS; mTLS; pinning; service mesh.                                                                    | 5              | 10                | 50              |
| 12 | Respostas incorretas (alucinação)         | Agentes IA → Backend → Frontend         | Tampering/Integrity        | IA fornece conteúdo falso, prejudicando o cliente.                                    | 15    | 10      | 150    | Pós-validação; filtros; checagem factual; fallback seguro.                                            | 5              | 5                 | 25              |
| 13 | Abuso de recursos por usuário            | Frontend → Backend                      | DoS/Tampering              | Usuário legítimo envia requisições excessivas.                                       | 10    | 10      | 100    | Rate limiting; quotas; bloqueio automático.                                                           | 5              | 5                 | 25              |
| 14 | Vazamento via logs                       | Backend → Logs                           | Information Disclosure     | Logs armazenam dados sensíveis sem mascaramento.                                     | 10    | 10      | 100    | Mascaramento; redução de logs sensíveis; criptografia; controles de acesso.                          | 5              | 5                 | 25              |

6. Conclusão

A modelagem de ameaças revelou riscos importantes, especialmente relacionados a:

Prompt Injection

Vazamento de dados em APIs externas

XSS no chat

DoS no agente local

MITM na comunicação A2A

Alucinações da IA

As medidas de mitigação propostas reduzem significativamente o risco residual em todos os cenários.
A análise demonstra que, com os controles aplicados, o sistema torna-se muito mais seguro, mantendo integridade, confidencialidade e disponibilidade adequadas para um ambiente de atendimento automatizado.
