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
| `VER-T####-##` | Verificacao de tarefa (ex.: `VER-T0007-01`) | Por tarefa |
| `BUG-T####-##` | Bug achado numa tarefa | Por tarefa |
| `SEC-T####-##` | Achado de seguranca numa tarefa | Por tarefa |
| `UX-T####-##` | Observacao visual numa tarefa | Por tarefa |
| `VER-####`, `BUG-####`, `SEC-####` | Registro sem tarefa e registros anteriores a [[ADR-0021 Pedidos ao Coordenador sempre em COORD e numeracao de qualidade por tarefa]] | Por repositorio |
| `COORD-####` | Pedido ao Coordenador (com ou sem tarefa) | Ambiente (`operacao/coordenador`) |
| `ADM-####` | Pedido ao Administrador | Ambiente (`operacao/administrador`) |
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

Um worktree do Orca por tarefa, com o nome `T-0012-descricao-curta` — o Orca usa esse nome para o branch. Os hooks do Git extraem o `T-####` do nome do branch.

## Logs (Markdown)

Gravados automaticamente por hooks do Claude Code em `D:\01_IA\logs` (cópia principal, **fora do Git**, somente acréscimo). Ver [[ADR-0012 Logs em Markdown fora do Git]].

- `logs/sessoes/AAAA-MM/AAAA-MM-DD_HHMM_<agente>_<sessao>.md` — todos os eventos de uma sessão.
- `logs/erros/AAAA-MM-DD.md` — somente falhas do dia, de todas as sessões.
- `logs/brain/AAAA-MM.jsonl` - cada acesso ao Brain (Read ou comando com `BRAIN/<pasta>`), uma linha JSON: `ts`, `papel`, `tarefa`, `sessao`, `ferramenta`, `tipo` (leitura/busca), `pasta`, `nota`. So o caminho, nunca o comando nem conteudo. Gravado por `ferramentas/hooks/registrar_brain.py`, ligado na definicao de cada papel; lido por `ferramentas/uso_brain.py` ([[ADR-0023 Medir o uso do Brain por acesso, citacao e utilidade declarada]]).
- `logs/consumo/AAAA-MM.jsonl` - tokens acumulados de cada sessao, uma linha por fim de turno (vale a ultima de cada sessao): `ts`, `sessao`, `papel`, `tarefa` (so `T-####`), `modelos` (entrada, cache criado, cache lido, saida, respostas). So numeros. Gravado por `ferramentas/hooks/registrar_consumo.py` (hook `Stop` na definicao de cada papel); lido por `ferramentas/consumo.py`, que o Coordenador roda no fechamento da tarefa (`ADM-0011`).

Arquivo de sessão:

```markdown
---
tipo: log-sessao
sessao: 1a2b3c4d
agente: dev
modelo: claude-sonnet-5
inicio: 2026-09-28T14:05:02-03:00
cwd: C:/Users/igorc/orca/workspaces/lab/T-0001-esqueleto
branch: T-0001-esqueleto
---
# Sessão dev — 2026-09-28 14:05

| Hora | Evento | Ferramenta | Resumo |
|---|---|---|---|
| 14:05:02 | inicio_sessao | — | startup · modo acceptEdits |
| 14:07:40 | ferramenta_usada | Edit | app/main.py |
| 14:08:11 | ferramenta_falhou | Bash | docker compose up: porta 5432 em uso |
| 14:09:30 | permissao_negada | Bash | git push origin main |
```

Arquivo de erros do dia: colunas `Hora | Agente | Sessão | Evento | Ferramenta | Resumo`.

| Evento | Origem (hook) |
|---|---|
| `inicio_sessao` / `fim_sessao` | `SessionStart` / `SessionEnd` |
| `ferramenta_usada` | `PostToolUse` (Edit, Write, Bash, PowerShell) — leituras não são registradas |
| `ferramenta_falhou` | `PostToolUseFailure` |
| `permissao_negada` | `PermissionDenied` |
| `falha_modelo` | `StopFailure` (limite de uso, erro de servidor etc.) |

Regras: o agente vem de `agent_type` (sessões iniciadas com `--agent`); `|` e quebras de linha são escapados; comandos são truncados e têm padrões de segredo mascarados. **Nunca** registrar segredos.

Eventos de processo (`tarefa_concluida`, `bug_registrado`, `conhecimento_proposto`…) não vão para o log: ficam registrados nos cartões de tarefa, nos commits e em `qualidade/`.
