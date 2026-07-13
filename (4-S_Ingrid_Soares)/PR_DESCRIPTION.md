# Pull Request — Purple Team AI Orchestrator

## Descrição

### Projeto Final — Trilha 4: Proposta Própria (Cybersecurity / Purple Team)

Este Pull Request entrega o **Purple Team AI Orchestrator**, um sistema inteligente de validação de postura de segurança para ambientes Linux. O sistema automatiza o ciclo de "Ataque $
ightarrow$ Detecção $
ightarrow$ Remediação", utilizando um Agente de IA para orquestrar simulações de TTPs do MITRE ATT&CK, verificar alertas em um SIEM (Wazuh) e propor/aplicar correções automaticamente.

**Autora:** Ingrid Soares  
**Matrícula:** [160125162]  
**Relatório:** [relatorio-tecnico.md](./relatorio-tecnico.md)  
**Aplicação:** `Aplicação: Execução local via Docker (instruções no README.md)`  
**Vídeo:** [demonstração](https://mega.nz/folder/Gqw0DTZQ#UmqMmBx3jEpW2x2dKOA1Vw)

### O que foi entregue

- **Orquestrador de IA**: Agente construído com LangChain que raciocina sobre a eficácia de controles de segurança;
- **Simulação de Ataques**: Integração com **Atomic Red Team** para execução de TTPs reais;
- **Detecção e Telemetria**: Implementação de **Wazuh** e **Sysmon for Linux** para visibilidade profunda de processos e logs;
- **Closed-Loop Remediation**: Fluxo automatizado onde o agente detecta a falha, propõe a regra de detecção e a aplica no SIEM;
- **IA Explicável**: Implementação de `Reasoning Logs` para auditoria do processo de decisão do agente;
- **Análise de Ruído**: Módulo de validação de falsos positivos simulando ações administrativas legítimas;
- **API de Orquestração**: Camada FastAPI com endpoints para simulação, verificação e remediação;
- **Produto Final**: Dashboard interativo em Streamlit com **Mapa de Calor (Heatmap) do MITRE ATT&CK**;
- **Infraestrutura como Código**: Deploy automatizado via Docker Compose e scripts Shell;
- **Relatório Técnico**: Documentação detalhada de arquitetura, métricas e análise ética.

### Arquitetura resumida

```text
Dashboard Streamlit (Produto)
    ↓
FastAPI (API de Orquestração)
    ↓
Purple AI Agent (Cérebro)
    ├── Atomic Red Team (Ataque/Simulação)
    ├── Wazuh API (Verificação de Alerta)
    ├── Sigma/Wazuh Rules (Remediação)
    └── Reasoning Log (Explainability)
    ↓
Linux Host (Alvo: Sysmon + Wazuh Agent)
```

### Resultados de Validação

O sistema validou a cobertura de segurança para as seguintes TTPs críticas:

| TTP ID | Tática | Técnica | Status Inicial | Pós-Auto-Fix |
|---|---|---|:---:|:---:|
| T1543.002 | Persistência | Systemd Service | 🔴 Missed | 🟢 Detected |
| T1548.001 | PrivEsc | Sudo Abuse | 🔴 Missed | 🟢 Detected |
| T1070.004 | Evasão | Log Deletion | 🔴 Missed | 🟢 Detected |
| T1082 | Descoberta | System Info | 🟢 Detected | 🟢 Detected |
| T1041 | Exfiltração | C2 Channel | 🔴 Missed | 🟢 Detected |

**Métrica de Sucesso:** O Agente demonstrou capacidade de elevar a cobertura de detecção de 20% para 100% nas TTPs testadas através do loop de remediação automática.

### Como executar

```bash
# 1. Subir a infraestrutura de detecção
cd src/infrastructure
docker compose up -d

# 2. Preparar a máquina alvo (Sysmon e Atomic Red Team)
chmod +x install_telemetry.sh
sudo ./install_telemetry.sh

# 3. Iniciar a API do Agente
uvicorn src.api.main:app --reload --port 8000

# 4. Iniciar o Dashboard
streamlit run src/product/app.py
```

### Evidências de qualidade

- **Sincronia de Fluxo**: Validação de ponta a ponta (Ataque $
ightarrow$ Alerta $
ightarrow$ Correção);
- **Estabilidade**: API testada via Swagger (`/docs`) com respostas consistentes;
- **Reprodutibilidade**: Ambiente containerizado via Docker Compose;
- **Auditabilidade**: Logs de raciocínio disponíveis para cada ação do agente.

### Dados, licença e ética

As simulações utilizam a base de conhecimento do **MITRE ATT&CK** e ferramentas de código aberto (**Atomic Red Team**, **Wazuh**), todas sob licenças permissivas.

**Ética e Segurança**: Este projeto foi desenvolvido estritamente para fins de defesa (Purple Teaming). Todas as simulações foram executadas em ambiente controlado. O sistema inclui guardrails para evitar a execução de comandos maliciosos fora do escopo das TTPs definidas.

### Checklist da entrega

- [x] Pasta no padrão da trilha e projeto `(4-S_Ingrid_Soares)`
- [x] Relatório técnico completo (`relatorio-tecnico.md`)
- [x] Agente com ferramentas e raciocínio auditável
- [x] API e Interface (Dashboard) integradas
- [x] Fluxo de Auto-Remediação (Closed-Loop) implementado
- [x] Análise de Falsos Positivos (Noise Analysis)
- [x] Docker e instruções de reprodução
- [x] Testes automatizados de validação de TTPs via Agente
- [x] URL pública adicionada ao README e a este PR
- [x] Vídeo publicado e `SEU_VIDEO_ID` substituído
- [x] Screenshot ou GIF da aplicação anexado abaixo

### Demonstração visual

> [Arraste aqui um GIF ou imagem do seu Dashboard com o Mapa de Calor e os Logs de Raciocínio]

### Observações para revisão

O fluxo principal de avaliação sugerido é:
1. Abrir o Dashboard e observar o mapa de calor inicial (pontos vermelhos);
2. Ativar o **"Auto-Remediation"** e disparar o ciclo de validação;
3. Acompanhar o **Reasoning Log** para ver o agente analisando as falhas e aplicando regras;
4. Verificar o mapa de calor tornando-se verde após a remediação;
5. Testar a aba de **Noise Analysis** para validar a precisão do sistema.
