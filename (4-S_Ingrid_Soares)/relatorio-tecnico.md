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
- **Deployment:** O sistema é totalmente conteinerizado. A stack de detecção (Wazuh) é gerenciada via Docker Compose, enquanto a API (FastAPI) e o Dashboard (Streamlit) possuem Dockerfiles próprios para garantir reprodutibilidade em qualquer ambiente. A infraestrutura de produção está configurada para deploy automático no **Railway**.
- **CI/CD:** Implementou-se um pipeline via **GitHub Actions** que realiza linting com `Ruff`, constrói as imagens Docker e as publica no **GitHub Container Registry (GHCR)**, seguido pelo deploy automatizado no Railway.
- **Confiabilidade:** Implementou-se a análise de **Falsos Positivos (Noise Analysis)**, simulando ações administrativas legítimas para garantir que o sistema não gere alertas excessivos. Além disso, o sistema possui fallbacks para falhas na API do LLM, retornando análises baseadas em regras pré-definidas.

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

## 6. Reflexões e Próximos Passos

### O que funcionou
A separação entre a lógica do agente e a API permitiu que a interface fosse leve e rápida. A escolha do Atomic Red Team garantiu que os ataques fossem padronizados e seguros.

### Limitações e Melhorias
- **Integração Real:** No protótipo, algumas chamadas de API foram simuladas para garantir a execução. O próximo passo é a configuração de certificados SSL reais para a API do Wazuh.
- **Auto-Remediação:** O agente atualmente *propõe* a regra. O próximo nível seria o agente *aplicar* a regra no Wazuh e re-testar o ataque automaticamente até que ele seja detectado.

---

## 7. Impactos e Ética
A ferramenta é destinada exclusivamente a fins de defesa (Purple Team). O uso indevido para automatizar ataques em sistemas não autorizados é estritamente proibido. Para mitigar riscos, o sistema deve ser executado em redes isoladas.

## 8. Referências
- MITRE ATT&CK Framework.
- Wazuh Documentation.
- Atomic Red Team (Red Canary).
- FastAPI & Streamlit Docs.
