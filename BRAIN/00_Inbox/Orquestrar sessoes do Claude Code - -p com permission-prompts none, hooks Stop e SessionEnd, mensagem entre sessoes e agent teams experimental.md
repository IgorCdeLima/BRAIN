---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: ambiente
pesquisa: SEARCH-0009
confianca: media
fontes: [https://code.claude.com/docs/en/headless, https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/cross-session-messaging, https://code.claude.com/docs/en/agent-teams]
verificado_em: 2026-10-05
valido_para: Claude Code 2.1.2xx (docs de 2026-10); agent teams e experimental
criado: 2026-10-05
decisao:
tags: [ambiente, claude-code, orquestracao, tmux, permissoes, adm-0009]
---
# Orquestrar sessoes do Claude Code - -p com permission-prompts none, hooks Stop e SessionEnd, mensagem entre sessoes e agent teams experimental

## Conteudo proposto

**1. Modo `-p` (nao interativo).** `claude -p "..."` sai com codigo 0 em sucesso e diferente de zero em falha (SIGTERM = 143), entao um script (ou outra janela tmux) detecta o fim pelo codigo de saida. `--output-format json` devolve `result`, `session_id` e custo; `--resume <id>` / `--continue` continuam a conversa. Limites: comandos so de terminal (`/login`) nao existem; `-p` **nao mostra dialogo de confianca de pasta** e roda hooks e `.mcp.json` do projeto (use `--bare` para nao carregar nada do projeto, mas `--bare` nao le login OAuth: exige `ANTHROPIC_API_KEY`).

**2. Permissoes sem ninguem olhando.** Em `-p` nao ha quem responda `ask`: o pedido e **negado** (Claude e avisado). `--permission-prompts none` (v2.1.259+) torna isso explicito e diz ao Claude para nao insistir; regras `allow`/`deny`, hooks `PermissionRequest` e o modo de permissao continuam decidindo antes. `--permission-mode dontAsk` nega tudo que nao esteja em `allow`; `--allowedTools` pre-aprova. Negacoes aparecem em `permission_denials` do resultado (`stream-json`).

**3. Perceber que outra sessao terminou.**
- Codigo de saida do processo `claude -p` (o mais simples).
- Hooks: `Stop` (fim de cada turno), `SubagentStop` e `SessionEnd` (fim da sessao; nao bloqueia). Hooks rodam em processos separados: o hook pode gravar um arquivo de sinal (ex.: em pasta compartilhada) que o orquestrador observa.
- Mensagem entre sessoes (v2.1.224+, mesma maquina): `SendMessage` com `notify_when_idle` pede **um** aviso quando a outra sessao ficar ociosa ou sair (validade 12 h; v2.1.236+ nos dois lados). Sessoes `-p` recebem mensagens se `crossSessionInbound: accept` estiver no `--settings` delas (senao a mensagem retida expira em 5 min); `--bare` nao abre o socket. Ressalvas: a mensagem nunca vale como aprovacao e nao muda configuracao; **sessao dentro de container e sessao no host nao se alcancam** (duas no mesmo container, sim).

**4. Varias sessoes coordenadas (oficial).** *Subagentes* (dentro de uma sessao, devolvem resultado) e *agent teams* (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, **experimental**, desligado por padrao; so sessao interativa, nao `-p`). Em agent teams os colegas **comecam com o modo de permissao do lider** (exceto `dontAsk`); se o lider usa `--dangerously-skip-permissions`, todos usam; pedidos de permissao dos colegas aparecem na sessao do lider; nao da para dar modo diferente por colega na criacao. Painel dividido pede tmux ou iTerm2 (`teammateMode`). Ou seja, agent teams **nao** servem se o orquestrador nao deve herdar/dividir as permissoes dos outros: nesse caso use processos `claude -p` separados, cada um com seu proprio `--settings`/perfil, mais codigo de saida, hooks e arquivos como canal.

## Evidencia

Quatro paginas oficiais da documentacao do Claude Code lidas em 2026-10-05. Nao testado em execucao. O comportamento exato de `ask` em `-p` sem `--permission-prompts none` vem da frase "in a -p run with no host, these requests are denied either way".

## Links confiaveis

- [Run Claude Code programmatically (-p)](https://code.claude.com/docs/en/headless): codigo de saida, `--bare`, `--permission-mode`, `--permission-prompts none`, `--resume`.
- [Hooks reference](https://code.claude.com/docs/en/hooks): eventos `Stop`, `SubagentStop`, `SessionEnd`, `PermissionRequest`.
- [Message your other Claude Code sessions](https://code.claude.com/docs/en/cross-session-messaging): `notify_when_idle`, `crossSessionInbound`, limite container x host.
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams): permissoes herdadas do lider, experimental, tmux.

## Por que e reaproveitavel

Decide a arquitetura de qualquer "sessao coordenadora" que abra e acompanhe outras sessoes.

## Relacionadas no Brain

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]

## Decisao do Bibliotecario
