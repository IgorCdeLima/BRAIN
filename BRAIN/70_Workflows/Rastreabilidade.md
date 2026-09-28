---
tipo: workflow
status: ativo
versao: 1
criado: 2026-09-28
tags: [rastreabilidade, painel]
---
# Rastreabilidade

Todo trabalho de agente deixa rastro estruturado. O painel futuro será apenas um leitor destas fontes.

## Identificadores

| Prefixo | O que identifica | Escopo da numeração |
|---|---|---|
| `T-####` | Tarefa | Ambiente (`operacao/tarefas`) |
| `VER-####` | Verificação | Por repositório |
| `BUG-####` | Bug | Por repositório |
| `SEC-####` | Achado de segurança | Por repositório |
| `ADR-####` | Decisão | Por repositório |

Tarefas de montagem do ambiente usam `F<fase>-<passo>` (ex.: `F0-0.5`).

## Commits

Mensagem em português: `tipo(escopo): descrição` — tipos `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.

Todo commit de agente termina com os trailers:

```text
Agente: <papel>          # dev, revisor, seguranca, bibliotecario, coordenador, engenharia...
Tarefa: <id>             # T-0012
Modelo: <modelo>         # claude-sonnet-5, claude-opus-5-5...
```

Consulta: `git log --format='%h %s%n%(trailers:key=Agente,key=Tarefa)'`.

## Branches

`tarefa/T-0012-descricao-curta` — um branch (e um worktree do Orca) por tarefa.

## Log de eventos (JSONL)

Arquivos em `operacao/logs/`, um por mês, **somente acréscimo**:

- `eventos-AAAA-MM.jsonl` — tudo o que acontece.
- `erros-AAAA-MM.jsonl` — somente falhas (subconjunto, para consulta rápida).

Um evento por linha:

```json
{"ts":"2026-09-28T14:03:00-03:00","agente":"dev","modelo":"claude-sonnet-5","tarefa":"T-0012","tipo":"teste_falhou","repo":"01_IA","commit":"4d0436b","ref":"BUG-0003","resumo":"3 testes falharam em auth","detalhe":"caminho/do/log/completo"}
```

| Campo | Obrigatório | Descrição |
|---|---|---|
| `ts` | sim | Data e hora ISO 8601 com fuso |
| `agente` | sim | Papel que gerou o evento |
| `modelo` | não | Modelo usado |
| `tarefa` | sim | `T-####` ou `F#-#.#` |
| `tipo` | sim | Ver lista abaixo |
| `repo` | sim | Repositório afetado |
| `commit` | não | SHA relacionado |
| `ref` | não | `BUG-`, `VER-`, `SEC-`, `ADR-` relacionado |
| `resumo` | sim | Uma linha legível |
| `detalhe` | não | Texto curto ou caminho para arquivo com a saída completa |

Tipos: `tarefa_iniciada`, `tarefa_concluida`, `tarefa_bloqueada`, `escalonamento`, `commit`, `verificacao`, `teste_falhou`, `ferramenta_falhou`, `permissao_negada`, `bug_registrado`, `sec_registrado`, `conhecimento_proposto`.

**Nunca** registrar segredos em nenhum campo.

A partir da fase 1, hooks do Claude Code gravam os eventos automaticamente (especialmente `ferramenta_falhou` e `permissao_negada`, que alimentam o ajuste de permissões).
