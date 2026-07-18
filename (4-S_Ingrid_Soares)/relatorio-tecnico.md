# Relatório Técnico: Purple Team AI Orchestrator

## 1. Cabeçalho
- **Aplicação:** Purple Team AI Orchestrator
- **Repositório:** `ingrid-soares/purple-team-project`
- **Integrantes:** Ingrid Soares
- **Objetivo:** Automatizar o ciclo de Simulação -> Detecção -> Remediação para TTPs Linux.

---

## 2. Definição do Problema

### A Dor
A maioria das empresas possui ferramentas de detecção (SIEM/EDR), mas não sabe se as regras de detecção realmente funcionam contra técnicas específicas do MITRE ATT&CK. A validação manual de cada TTP é exaustiva e raramente é feita de forma sistêmica.

### Stakeholders
- **Security Engineers:** Responsáveis por criar as regras de detecção.
- **SOC Analysts:** Quem opera as ferramentas e precisa de alertas precisos.
- **CISO:** Interessado na métrica de "cobertura de segurança" da infraestrutura Linux.

### Métricas de Sucesso
- **Métrica de Negócio:** Aumento da porcentagem de cobertura do MITRE ATT&CK validada empiricamente.
- **Métrica Técnica:** Redução do tempo entre a simulação de um ataque e a proposta de uma regra de detecção funcional.

---

## 3. Arquitetura do Sistema

### Diagrama de Fluxo
`TTP ID` -> `AI Agent` -> `Atomic Red Team (Ataque)` -> `Wazuh/Sysmon (Logs)` -> `AI Agent (Análise)` -> `FastAPI` -> `Streamlit Dashboard (Heatmap)`

### Engenharia da Solução
- **Agent/Model Exploration:** Foi escolhido um modelo de orquestração baseado em ferramentas (Tool-use) com um loop de **Closed-Loop Security**. O agente não apenas identifica a falha, mas aplica a correção e re-testa a eficácia da nova regra automaticamente.
- **Explainability (IA Explicável):** O sistema implementa um `Reasoning Log` que captura a corrente de pensamento (Chain of Thought) do agente, permitindo que analistas de segurança auditem por que o agente tomou determinada decisão.
- **Deployment:** O sistema é totalmente conteinerizado. A stack de detecção (Wazuh) é gerenciada via Docker Compose, enquanto a API (FastAPI) e o Dashboard (Streamlit) possuem Dockerfiles próprios. A infraestrutura de produção está hospedada no **Railway**, com deploy automatizado via pipeline GitHub Actions.
- **CI/CD:** Implementou-se um pipeline via **GitHub Actions** que realiza linting com `Ruff`, constrói as imagens Docker e as publica no **GitHub Container Registry (GHCR)**, seguido pelo deploy automatizado no Railway.
- **Confiabilidade:** Implementou-se a análise de **Falsos Positivos (Noise Analysis)**, simulando ações administrativas legítimas para garantir que o sistema não gere alertas excessivos. Além disso, o sistema possui fallbacks para falhas na API do LLM, retornando análises baseadas em regras pré-definidas.

---

## Pipeline de CI/CD
Implementou-se um pipeline robusto via **GitHub Actions** composto por 4 etapas críticas que garantem a qualidade e a automação do ciclo de entrega:

1. **CI / lint-and-test**: Executa `Ruff` para garantir a qualidade do código, formatação e integridade das importações em cada Push/PR.
2. **CD / build-and-push**: Constrói as imagens Docker da API e do Dashboard de forma automatizada e as publica com segurança no **GitHub Container Registry (GHCR)**.
3. **FastAPI Backend (Deploy)**: Deploy automatizado da API no **Railway**, garantindo alta disponibilidade.
4. **Streamlit Dashboard (Deploy)**: Deploy automatizado do Dashboard no **Railway**, configurado para comunicação segura com a API via variáveis de ambiente.

---

## 4. Descrição do Agente

### Modelo e Ferramentas
- **Modelo Base:** Gemini / GPT-4 (via LangChain) para raciocínio lógico e geração de regras Sigma.
- **Ferramentas:**
    - `simulate_attack`: Interface com o Atomic Red Team.
    - `check_detection`: Interface com a API do Wazuh.
    - `propose_detection_rule`: Motor de geração de sintaxe para regras de detecção.

### Dados e Contexto
O agente utiliza a matriz do **MITRE ATT&CK** como base de conhecimento para entender o comportamento esperado de cada TTP e correlacionar com os logs gerados.

### Guardrails
- **Validação de Entrada:** O agente valida se o ID da TTP é válido antes de disparar qualquer comando no sistema.
- **Isolamento:** As simulações são desenhadas para rodar em ambientes de laboratório, evitando impactos em produção.

---

## 5. Avaliação do Sistema

### Performance
O sistema consegue validar o ciclo completo de 5 TTPs críticas em poucos minutos, transformando um processo que levaria horas de análise manual de logs em um relatório automático de "Coberto/Não Coberto".

### UX (Experiência do Usuário)
O uso de um **Mapa de Calor (Heatmap)** permite que o gestor de segurança identifique instantaneamente as "zonas cegas" da rede sem precisar ler logs técnicos, enquanto o analista tem acesso ao log de raciocínio do agente para entender a falha.

---

## Evolução e Amadurecimento do Projeto
A evolução do Purple Team AI Orchestrator transformou um protótipo local em uma solução de engenharia de nível profissional. Abaixo, detalhamos essa evolução:

1. **De "Local" para "Produção" (Deploy)**
   - **Antes**: O sistema rodava apenas localmente com configurações manuais de Docker.
   - **Depois**: Implementamos uma infraestrutura pública e viva no **Railway**, garantindo que o sistema seja acessível via internet, cumprindo critérios de confiabilidade e disponibilidade.

2. **Automação e DevOps**
   - **Antes**: Deploy manual e repetitivo.
   - **Depois**: Criamos um pipeline de **CI/CD com GitHub Actions**. Qualquer mudança no código é testada (linting), construída (Docker) e implantada (Deploy) automaticamente, seguindo padrões de mercado.

3. **Qualidade e Segurança do Código**
   - **Antes**: Existiam variáveis não utilizadas, importações redundantes, blocos `except` genéricos e URLs fixas ("hardcoded").
   - **Depois**: Adotamos um linter (**Ruff**) rigoroso, gerenciamento de dependências via `requirements.txt` e uso de variáveis de ambiente (`API_URL`), tornando a aplicação compatível com padrões modernos de desenvolvimento (12-Factor App).

4. **Documentação e Profissionalismo**
   - **Antes**: Documentação básica.
   - **Depois**: Adicionamos seções detalhadas sobre o Pipeline de CI/CD, fluxos de deploy e referências técnicas, garantindo uma visão profissional de ponta a ponta do ciclo de vida do software.

---

## Melhorias Futuras
Para elevar ainda mais o projeto, os seguintes pontos foram identificados como próximos passos:

- **Automação de Remediação:** Atualmente, o agente propõe a regra de detecção. O próximo nível seria a aplicação automática da regra no SIEM (Wazuh) e a re-execução do teste de ataque para validar a mitigação.
- **Integração com Certificados SSL Reais:** Configuração de certificados SSL personalizados para a comunicação entre a API e o SIEM, reforçando a segurança em produção.
- **Monitoramento Avançado:** Implementação de logs estruturados e métricas de desempenho mais granulares no painel de controle do Dashboard.
- **Suporte a mais TTPs:** Ampliar a biblioteca do Atomic Red Team utilizada, cobrindo novas táticas do framework MITRE ATT&CK.

---

## 7. Impactos e Ética
A ferramenta é destinada exclusivamente a fins de defesa (Purple Team). O uso indevido para automatizar ataques em sistemas não autorizados é estritamente proibido. Para mitigar riscos, o sistema deve ser executado em redes isoladas.

## 8. Referências e Licenças
- **MITRE ATT&CK Framework:** Base de conhecimento de táticas e técnicas de adversários. [Licença MITRE](https://attack.mitre.org/resources/terms-of-use/).
- **Atomic Red Team (Red Canary):** Biblioteca de testes de segurança. [Licença MIT](https://github.com/redcanaryco/atomic-red-team/blob/master/LICENSE).
- **Wazuh:** Plataforma de segurança open-source. [Licença GPLv2](https://github.com/wazuh/wazuh/blob/master/LICENSE).
- **Sysmon for Linux (Microsoft):** Ferramenta de telemetria de processos. [Licença MIT](https://github.com/microsoft/SysmonForLinux/blob/main/LICENSE).
- **Sigma Rules:** Padrão genérico para assinaturas de detecção. [Licença Apache 2.0](https://github.com/SigmaHQ/sigma/blob/master/LICENSE.md).

## 9. Aprovação do Docente
- **Status:** [Insira aqui: Aguardando/Aprovado]
- **Data da aprovação:** [Insira aqui a data]
- **Observações:** [Insira aqui eventuais observações feitas pelo docente]
