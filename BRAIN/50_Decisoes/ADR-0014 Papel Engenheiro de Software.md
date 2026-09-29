---
tipo: decisao
status: aceita
decidido_em: 2026-09-29
decidido_por: Igor
substituida_por:
criado: 2026-09-29
tags: [ambiente, agentes, modelagem]
---
# ADR-0014 Papel Engenheiro de Software

## Contexto

Até a T-0001, requisitos, modelos e a escolha de stack foram escritos pelo assistente de configuração, fora do fluxo dos agentes. O humano considera essencial um papel dedicado a entender "o que o cliente precisa", produzir UML e diagramas úteis e avaliar tecnologias antes da implementação.

## Decisão

- Novo papel **`engenheiro`** (modelo Opus), iniciado com `papel engenheiro` em cartões com `papel: engenheiro`.
- Escreve **somente** em `docs/` do projeto, em `operacao/tarefas` e no Inbox — garantido por hook de lista de permissões (`restringir_escrita.py`). Sem Docker; pesquisa na web liberada (versões são fatos voláteis).
- Produz requisitos verificáveis, modelos Mermaid proporcionais à tarefa, avaliações de tecnologia com matriz ponderada e ADRs `proposta`; decompõe em cartões de implementação `backlog` para o Dev.
- O Revisor verifica a documentação pela matriz; o humano aceita os ADRs e libera os cartões.
- O lançador passa a exigir que o `papel:` do cartão coincida com o papel iniciado (dev/engenheiro).
- Guia: `BRAIN/70_Workflows/Padroes de modelagem.md`; templates em `99_Sistema/Templates/Projeto`.

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| Arquiteto e Analista de requisitos separados | Especialização | Volume atual não justifica dois papéis |
| Dev faz a modelagem | Menos passos | Modelo do problema contaminado pela solução; sem revisão independente do desenho |

## Consequências

- **Positivas:** decisões e requisitos passam a ser rastreáveis e revisados antes do código; o humano decide com base em alternativas explícitas.
- **Negativas / riscos:** mais uma etapa por funcionalidade; para tarefas triviais o Dev segue direto do cartão.
