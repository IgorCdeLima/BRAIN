---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, seguranca, permissoes, orca]
---
# ADR-0011 Perfis por papel via `--settings`

## Contexto

As regras de `.claude/settings.json` valem para o repositório inteiro, não por papel. A fase 0.12 testou como aplicar permissões diferentes a cada agente dentro de um worktree do Orca. Complementa [[ADR-0006 Modelo de permissoes]].

## Resultados do teste (2026-09-28)

| Teste | Resultado |
|---|---|
| Perfil revisor (`claude --settings agentes/perfis/teste-revisor.json`) em worktree do Orca | ✅ Edição negada (ferramentas Edit/Write removidas); escrita por redirecionamento no shell negada sem pergunta; `git log` liberado executou |
| Trava do bypass (`--dangerously-skip-permissions` com `disableBypassPermissionsMode`) | ✅ Sem efeito: a escrita foi recusada igual ao controle sem a opção |
| Regra comum `Read(**/.env)` | ✅ Bloqueou também a **criação** do `.env` |
| Regras "perguntar" em áreas N4 (`CLAUDE.md`, push) | ⚠️ Não acionadas: o agente recusou antes de tentar, seguindo o `CLAUDE.md`. Camada de instruções funcionou; camada técnica ainda sem teste direto |
| Isolamento | ⚠️ O item "01_IA" do Orca é a **cópia principal**, não um worktree. O primeiro teste rodou nela e deixou alterações em `D:\01_IA` |

## Decisão

- Cada papel terá um arquivo de perfil em `agentes/perfis/<papel>.json`, carregado com `claude --settings`.
- Agentes sem supervisão usam `defaultMode: dontAsk` no perfil. Negar a ferramenta pelo nome (`"Edit"`) remove a ferramenta do agente.
- **Agentes trabalham sempre num worktree criado pelo Orca.** A cópia principal `D:\01_IA` é do humano e do Bibliotecário.
- O acesso de escrita a `BRAIN/00_Inbox` passa a depender do perfil de cada papel (o `CLAUDE.md` foi ajustado).

## Em aberto (fase 1)

- Como o Orca inicia cada papel com seu perfil. Os argumentos padrão do Orca são por tipo de agente, não por papel. Candidatos: terminal no worktree com `claude --settings`, ou argumentos no `worker-start` da orquestração.
- Teste técnico direto das regras "perguntar".

## Consequências

- **Positivas:** permissões por papel com efeito técnico real, independentes do modelo obedecer às instruções.
- **Negativas / riscos:** um papel iniciado sem o perfil herda só as regras comuns — iniciar o papel corretamente precisa ser automatizado.
