---
tipo: referencia
status: ativo
origem: SEARCH-0009 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0009
tarefa: ambiente
autor: Anthropic (documentacao do Claude Code)
url: https://code.claude.com/docs/en/headless
acessado_em: 2026-10-05
confianca: media
fontes: ["https://code.claude.com/docs/en/headless", "https://code.claude.com/docs/en/hooks", "https://code.claude.com/docs/en/cross-session-messaging", "https://code.claude.com/docs/en/agent-teams"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.2xx (docs de 2026-10); agent teams e experimental"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [ambiente, claude-code, orquestracao, tmux, permissoes, adm-0009]
---
# Orquestrar sessoes do Claude Code - -p com permission-prompts none, hooks Stop e SessionEnd, mensagem entre sessoes e agent teams experimental

## Resumo

**1. Modo `-p` (nao interativo).** `claude -p "..."` sai com codigo 0 em sucesso e diferente de zero em falha (SIGTERM = 143), entao um script (ou outra janela tmux) detecta o fim pelo codigo de saida. `--output-format json` devolve `result`, `session_id` e custo; `--resume <id>` / `--continue` continuam a conversa. Limites: comandos so de terminal (`/login`) nao existem; `-p` **nao mostra dialogo de confianca de pasta** e roda hooks e `.mcp.json` do projeto (`--bare` nao carrega nada do projeto, mas nao le login OAuth: exige `ANTHROPIC_API_KEY`).

**2. Permissoes sem ninguem olhando.** Em `-p` nao ha quem responda `ask`: o pedido e **negado** (Claude e avisado). `--permission-prompts none` (v2.1.259+) torna isso explicito e diz ao Claude para nao insistir; regras `allow`/`deny`, hooks `PermissionRequest` e o modo de permissao continuam decidindo antes. `--permission-mode dontAsk` nega tudo que nao esteja em `allow`; `--allowedTools` pre-aprova. Negacoes aparecem em `permission_denials` do resultado (`stream-json`).

**3. Perceber que outra sessao terminou.**
- Codigo de saida do processo `claude -p` (o mais simples).
- Hooks: `Stop` (fim de cada turno), `SubagentStop` e `SessionEnd` (fim da sessao; nao bloqueia). Hooks rodam em processos separados: o hook pode gravar um arquivo de sinal em pasta compartilhada que o orquestrador observa.
- Mensagem entre sessoes (v2.1.224+, mesma maquina): `SendMessage` com `notify_when_idle` pede **um** aviso quando a outra sessao ficar ociosa ou sair (validade 12 h; v2.1.236+ nos dois lados). Sessoes `-p` recebem mensagens se `crossSessionInbound: accept` estiver no `--settings` delas (senao a mensagem retida expira em 5 min); `--bare` nao abre o socket. A mensagem nunca vale como aprovacao e nao muda configuracao; **sessao dentro de container e sessao no host nao se alcancam** (duas no mesmo container, sim).

**4. Varias sessoes coordenadas (oficial).** *Subagentes* (dentro de uma sessao, devolvem resultado) e *agent teams* (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, **experimental**, desligado por padrao; so sessao interativa, nao `-p`). Em agent teams os colegas **comecam com o modo de permissao do lider** (exceto `dontAsk`); se o lider usa `--dangerously-skip-permissions`, todos usam; pedidos de permissao dos colegas aparecem na sessao do lider; nao da para dar modo diferente por colega na criacao. Painel dividido pede tmux ou iTerm2 (`teammateMode`).

## O que aproveitar

Decide a arquitetura de uma "sessao coordenadora" que abre e acompanha outras. Agent teams **nao** servem se o orquestrador nao deve herdar/dividir as permissoes dos outros; nesse caso use processos `claude -p` separados, cada um com seu proprio `--settings`/perfil, com codigo de saida, hooks e arquivos como canal.

## Ressalvas

Quatro paginas oficiais lidas em 2026-10-05; **nao testado em execucao**. O comportamento de `ask` em `-p` sem `--permission-prompts none` vem da frase "in a -p run with no host, these requests are denied either way". Versoes minimas citadas (2.1.224, 2.1.236, 2.1.259) mudam rapido; agent teams e experimental. Nao confirmado se subagentes herdam permissoes do pai em detalhe.

## Links confiaveis

- [Run Claude Code programmatically (-p)](https://code.claude.com/docs/en/headless): codigo de saida, `--bare`, `--permission-mode`, `--permission-prompts none`, `--resume`.
- [Hooks reference](https://code.claude.com/docs/en/hooks): eventos `Stop`, `SubagentStop`, `SessionEnd`, `PermissionRequest`.
- [Message your other Claude Code sessions](https://code.claude.com/docs/en/cross-session-messaging): `notify_when_idle`, `crossSessionInbound`, limite container x host.
- [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams): permissoes herdadas do lider, experimental, tmux.

## Notas derivadas

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]: onde as sessoes rodam; a regra "container x host nao se alcancam" depende dele.
- [[tmux em container exige TERM tmux ou screen, locale UTF-8 e window-size para varios clientes]]: as janelas tmux onde as sessoes abertas ficam.

## Decisao do Bibliotecario

Promovido a `30_Referencias` (2026-10-05): resume quatro paginas oficiais para a fase 3 do ADM-0009; sem duplicata no Brain. Confianca media mantida.
