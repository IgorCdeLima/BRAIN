---
tipo: pesquisa
id: SEARCH-0009
status: nao-pesquisada
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: ambiente
criado: 2026-10-05
pesquisado_por:
pesquisado_em:
catalogado_em:
notas: []
tags: [ambiente, docker, container, claude-code, tmux, adm-0009]
---
# SEARCH-0009 - Rodar o ambiente 01_IA (Claude Code, git, hooks, tmux) dentro de um container

## Pergunta

1. **Claude Code em container (documentacao oficial da Anthropic):** existe imagem ou devcontainer de referencia? Como instalar o CLI numa imagem Linux, como fazer o login (conta claude.ai) sem gravar segredo na imagem nem no repositorio, e onde ficam a configuracao e as transcricoes (`~/.claude`, `cleanupPeriodDays`) para montar como volume. O que a documentacao diz sobre `--dangerously-skip-permissions` e firewall no devcontainer (para nao usar sem saber).
2. **Docker dos projetos dentro do container** (o lab usa Docker Compose): comparar, com fontes oficiais (Docker, Podman), (a) montar o socket do Docker do host, (b) Docker-in-Docker (container privilegiado), (c) Docker rootless ou Podman. Para cada um: o que o container passa a poder fazer no host, requisitos no Linux e limitacoes conhecidas com Compose.
3. **Usuario e arquivos:** como rodar o container com usuario sem privilegio cujo UID/GID bate com o do humano no host, para que os arquivos do repositorio montado (worktrees, `.git`) nao fiquem com dono root.
4. **tmux dentro do container:** acessar a sessao tmux do container a partir do terminal do host (`docker exec -it ... tmux attach`): ressalvas de TERM, UTF-8 e tamanho da janela.

## Contexto

[[ADM-0009]], fase 2 (decisao do humano, 2026-10-05): colocar todo o ambiente num container, reproduzivel como uma aplicacao. A fase 1 troca o Orca por `ferramentas/tarefa.py` (git worktree + tmux) no host. Maquina: Linux. Hoje: Claude Code instalado em `~/.local/bin`, hooks em Python 3, git, Docker no host. A escolha da opcao do item 2 sera feita depois desta pesquisa e da analise de ameacas da Seguranca. Nao precisa de preco.

## Ja buscado no Brain

`devcontainer`, `docker-in-docker`, `docker.sock`, `rootless`, `podman`, `tmux`, "claude code" + container: nada. Notas relacionadas so ao container do lab: [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]] e [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]] (ajudam no item 3, mas sao sobre a aplicacao, nao sobre o ambiente dos agentes).

---

## Resposta

<!-- Preenchido pelo Pesquisador. -->

- **Resumo (3 a 5 linhas):**
- **Notas geradas no Inbox:** [[ ]]
- **Links confiaveis:**
- **Sem resposta / limites:**
- **Conteudo suspeito descartado:**

## Dominios propostos

<!-- Dominios novos para agentes/fontes-confiaveis.json, com o motivo. O humano decide. -->

- 

## Catalogacao

<!-- Preenchido pelo Bibliotecario: decisao e notas finais. -->
