# 3. Visão Arquitetônica Final (Pós-Mitigação) 
## 3.1. Introdução 
Após a análise detalhada de riscos e ameaças descrita na etapa de Modelagem de Ameaças, a arquitetura do ConsultAI Ufla Júnior foi aprimorada com a introdução de controles e mecanismos de segurança 
que garantem a confidencialidade, integridade e disponibilidade dos dados e serviços. 
## 3.2. Estratégias de Mitigação e Aprimoramentos 
A seguir estão descritas as medidas de mitigação implementadas e os aprimoramentos realizados no design do sistema. 
### 3.2.1. Implementação de um API Gateway Seguro 
Um API Gateway foi inserido como camada intermediária e único ponto de entrada entre os usuários e o sistema.

**Responsabilidades e Benefícios:** 

- **Autenticação e Autorização:** valida todas as requisições antes de chegarem à API, evitando spoofing e acessos indevidos. 

- **Rate Limiting:** restringe o número de requisições por IP/usuário, mitigando ataques de negação de serviço (DoS). 

- **Roteamento Inteligente:** encaminha as requisições para os microserviços apropriados (backend, agentes de IA). 

- **Offloading de SSL/TLS:** gerencia a criptografia de comunicações externas via HTTPS.

### 3.2.2. Segurança de Comunicação Interna com mTLS (Mutual TLS) 

A comunicação entre o Backend e os Agentes de IA (local e externo) foi reforçada com o uso de mTLS, garantindo autenticação mútua e criptografia ponta a ponta. 

**Principais controles:** 

- **Autenticação Mútua:** tanto o cliente (Backend) quanto o servidor (Agente de IA) apresentam certificados válidos antes de qualquer troca de dados. 

- **Criptografia Interna:** impede a leitura ou adulteração de mensagens por atacantes internos ou intermediários. 

- **Proteção contra Spoofing e Tampering:** apenas serviços autenticados e legítimos podem participar da comunicação.

## 3.3. Arquitetura Aprimorada e Novo Fluxo de Dados 
**Fluxo de Dados Pós-Mitigação**
1.**Usuário → API Gateway**: o cliente envia uma pergunta via HTTPS. 

2.***API Gateway → Backend**: o Gateway autentica a requisição, aplica limites e repassa ao backend. 

3.**Backend → Agentes de IA (via mTLS)**: comunicação criptografada e autenticada entre serviços. 

4.**Backend → Base de Conhecimento**: consulta controlada com verificação de integridade. 

5.**Agentes → Backend → Gateway → Usuário:** resposta segura retornada pelo mesmo caminho criptografado. 

## 3.4. Tabela de Mitigações e Impacto nas Ameaças 
| Medida de Segurança       | Ameaça STRIDE Mitigada            | Descrição / Impacto                                                              |
|-------------------|----------------------------------|---------------------------------------------------------------------------------|
| **HTTPS e API Gateway** | Information Disclosure, Tampering |Mantém as informações seguras enquanto trafegam entre o usuário e o sistema.|
| **API Gateway**         | Spoofing, Denial of Service (DoS) | Controla quem pode acessar o sistema e limita o número de requisições, evitando sobrecarga e acessos falsos.|
| **mTLS Interno**        | Spoofing, Tampering, Information Disclosure | Garante que só os serviços de confiança conversem entre si, com tudo criptografado.|
| **Verificação de Entradas** | Tampering, Elevation of Privilege | Impede que comandos maliciosos sejam enviados, evitando alterações indevidas ou ganho de acesso.|
| **Registros de Ações (Logs)** | Repudiation |Guarda o que foi feito no sistema para que tudo possa ser conferido depois.|
| **Proteção dos Contêineres** | Elevation of Privilege | Limita o que cada contêiner pode fazer, impedindo que alguém controle o servidor. |

## 3.5. Conclusão

Com as melhorias aplicadas, o ConsultAI Ufla Júnior passou a ter uma estrutura mais segura, organizada e preparada para lidar com possíveis riscos. As medidas adotadas reduzem as chances de falhas, ataques e vazamentos de informações, garantindo que o chatbot funcione de forma estável e confiável.

Além disso, ao incluir a segurança desde o planejamento do sistema, o projeto reforça o compromisso com a proteção dos dados e com a qualidade do serviço oferecido aos usuários. Essas práticas tornam o sistema mais confiável para o uso interno da empresa júnior.Este documento será atualizado conforme o projeto evoluir.
