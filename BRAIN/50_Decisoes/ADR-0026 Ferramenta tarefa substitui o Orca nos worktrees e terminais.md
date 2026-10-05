---
tipo: decisao
status: aceita
decidido_em: 2026-10-05
decidido_por: humano
substituida_por:
criado: 2026-10-05
tags: [ambiente, orca, worktree, tmux, ferramentas, adm-0009]
---
# ADR-0026 Ferramenta tarefa substitui o Orca nos worktrees e terminais

## Contexto

- O Orca so criava o worktree `T-####-descricao` a partir da `main`, abria um terminal em branco nele e, no fechamento, o humano excluia o worktree por ele. Lancador, cartoes, hooks e Git ja eram independentes do Orca.
- O humano quer o ambiente inteiro num container, reproduzivel como uma aplicacao, e no futuro um quadro de tarefas em que **aceitar a tarefa cria o worktree** (`ADM-0009`, decisao de 2026-10-05). Um aplicativo grafico externo nao combina com nenhum dos dois.
- Ordem decidida: (1) ferramenta propria no host; (2) container; (3) Coordenador por tarefa (orquestracao); (4) quadro web. Esta ADR cobre so a fase 1.
- Terminais: o humano escolheu tmux (uma sessao por tarefa, uma janela por papel; funciona no host e no container).

## Decisao

- **`ferramentas/tarefa.py`** (Linux: `tarefa.sh`), com quatro acoes:
  - `aceitar T-####`: le `projeto:` e o titulo do cartao; cria o branch e o worktree `T-####-<descricao>` a partir da `main` de `projetos/<projeto>` em `$IA_WORKTREES/<projeto>/` (padrao `~/01_ia/worktrees`) e a sessao tmux `T-####`. Se ja aceita, so reabre; se o branch ja existe, cria so o worktree. Recusa cartao em `backlog`, `concluida` ou `cancelada`. **Nao muda o status do cartao.**
  - `abrir T-#### <papel>`: so papeis de worktree (dev, engenheiro, designer, seguranca, revisor); abre a janela do papel na sessao da tarefa, que chama o lancador `papel` no worktree. Quem confere cartao e status e define `IA_PAPEL` continua sendo o lancador.
  - `listar`: tarefas com worktree, branch, status do cartao e sessao tmux.
  - `fechar T-####`: so com o cartao `concluida` ou `cancelada` e o worktree sem mudanca pendente; `concluida` exige o branch na `main`. Fecha a sessao tmux, remove o worktree (sem `--force`) e apaga o branch so se ja estiver na `main` (`git branch -d`); branch fora da `main` fica (nada e apagado).
  - `--simular` mostra os comandos sem executar.
- **Agente nao aceita tarefa nem abre papel:** `aceitar`, `abrir` e `fechar` recusam rodar dentro do Claude (variavel `CLAUDECODE`), como o lancador ([[ADR-0013 Lancador de papeis e identidade dos agentes]]). Dentro do Claude, so `listar` e `--simular`. O humano roda as acoes ate o quadro existir; o Coordenador so diz o comando.
- Regras atualizadas (sem Orca): `CLAUDE.md`, `Fluxo de tarefa`, `Rastreabilidade`, `Coordenador` (nota e definicao), definicao do Administrador, template `Tarefa`, `agentes/_LEIAME.md`, `operacao/coordenador/_LEIAME.md`, mensagens de `papel.py` e comentario de `verificar_commit.py`. Registros antigos (cartoes, VER, logs) ficam como estao.

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| Manter o Orca | Nada a fazer | Aplicativo grafico externo; nao vai para o container nem para o quadro |
| Lancador `papel` cria o worktree | Um comando so | Mistura "aceitar a tarefa" com "abrir um papel"; o quadro precisa das duas acoes separadas |
| Terminal no navegador (ttyd/xterm.js) | Bonito, ja integra no quadro | Abre porta, exige autenticacao e analise da Seguranca; fica para a fase 4 |
| **tmux + `tarefa.py`** | Simples, sem porta aberta, mesmo uso no host e no container; acoes reaproveitadas pelo quadro | Precisa instalar tmux; o humano aprende 3 atalhos (`attach`, `Ctrl-b w`, `Ctrl-b d`) |

## Consequencias

- **Positivas:** o Orca sai do ambiente; o quadro da fase 4 e o Coordenador por tarefa da fase 3 chamam as mesmas acoes; `IA_WORKTREES` permite montar os worktrees como volume no container (fase 2).
- **Negativas / riscos:** tmux precisa estar instalado (`sudo apt install tmux`); a sessao tmux nao mostra pedidos de permissao de varias janelas ao mesmo tempo (o humano troca de janela); worktrees antigos do Orca (`~/orca/workspaces`) nao aparecem em `listar` se o repositorio nao os tiver (hoje nao ha nenhum).
- **Verificacao:** teste do ciclo num ambiente falso no scratchpad do Administrador, 14/14 (aceitar, reabrir, listar, recusas de fechar, fechar com e sem merge, cancelada mantendo o branch, aceitar com branch existente, abrir sem tmux). **Nao verificado:** tmux (nao instalado) e o lancador aberto pela janela do tmux numa tarefa real.

## Relacionadas

- `ADM-0009` (ideia completa e fases)
- [[ADR-0013 Lancador de papeis e identidade dos agentes]]
- [[ADR-0018 Papel Administrador com senha e aprovacao a cada mudanca]]
