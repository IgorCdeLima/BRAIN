---
tipo: pesquisa
id: SEARCH-0009
status: respondida
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: ambiente
criado: 2026-10-05
pesquisado_por: pesquisador
pesquisado_em: 2026-10-05
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
5. **Orquestracao (fase 3 do ADM-0009, acrescentada em 2026-10-05):** uma sessao do Claude Code (o "Coordenador da tarefa") abrir e acompanhar outras sessoes em janelas tmux. Na documentacao oficial: modo nao interativo (`-p`) e seus limites; como uma sessao percebe que outra terminou (codigo de saida, hooks `Stop`/`SessionEnd`, arquivos); como ficam os pedidos de permissao numa sessao sem ninguem olhando (o que acontece com `ask` no modo `-p`); se ha recurso oficial de varias sessoes ou agentes coordenados que sirva sem dar ao orquestrador as permissoes dos outros.

## Contexto

[[ADM-0009]], fase 2 (decisao do humano, 2026-10-05): colocar todo o ambiente num container, reproduzivel como uma aplicacao. A fase 1 troca o Orca por `ferramentas/tarefa.py` (git worktree + tmux) no host. Maquina: Linux. Hoje: Claude Code instalado em `~/.local/bin`, hooks em Python 3, git, Docker no host. A escolha da opcao do item 2 sera feita depois desta pesquisa e da analise de ameacas da Seguranca. Nao precisa de preco.

## Ja buscado no Brain

`devcontainer`, `docker-in-docker`, `docker.sock`, `rootless`, `podman`, `tmux`, "claude code" + container: nada. Notas relacionadas so ao container do lab: [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]] e [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]] (ajudam no item 3, mas sao sobre a aplicacao, nao sobre o ambiente dos agentes).

---

## Resposta

- **Resumo (3 a 5 linhas):** A Anthropic documenta Claude Code em dev container (Feature oficial, volume em `~/.claude` + `CLAUDE_CONFIG_DIR`, usuario nao root; `--dangerously-skip-permissions` nao impede exfiltrar credenciais de dentro do container). Docker no container: socket do host = root no host; DinD exige `--privileged`; rootless/Podman isolam mais, com limites de rede e de configuracao. UID: `--user uid:gid` (Docker) ou `--userns=keep-id` (Podman). Orquestracao: em `-p` o `ask` e negado (use `--permission-prompts none`), fim da sessao por codigo de saida, hooks `Stop`/`SessionEnd` ou `notify_when_idle`; agent teams e experimental, interativo e os colegas herdam o modo de permissao do lider; sessao em container nao alcanca sessao no host.
- **Notas geradas no Inbox:**
  - [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]
  - [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]
  - [[Arquivos do volume montado ficam com o dono certo rodando o container com o UID do usuario do host]]
  - [[tmux em container exige TERM tmux ou screen, locale UTF-8 e window-size para varios clientes]]
  - [[Orquestrar sessoes do Claude Code - -p com permission-prompts none, hooks Stop e SessionEnd, mensagem entre sessoes e agent teams experimental]]
- **Links confiaveis:** code.claude.com/docs (devcontainer, headless, hooks, cross-session-messaging, agent-teams); docs.docker.com (security, rootless, userns-remap, container run); hub.docker.com/_/docker; docs.podman.io; github.com/tmux/tmux/wiki/FAQ.
- **Sem resposta / limites:** (1) Nada foi executado: so leitura de documentacao. (2) Limites de Docker Compose em rootless/Podman nao constam numa lista oficial unica; testar com o compose do lab. (3) Redimensionamento da janela no `docker exec -it` nao esta documentado. (4) A pagina de permissoes (76 KB) foi so consultada por busca de trechos; o comportamento de `ask` em `-p` vem da pagina `headless`. (5) Se subagentes herdam permissoes do pai em detalhe: nao confirmado; o que esta confirmado e a heranca de modo nos agent teams. (6) O resumo das paginas veio de modelo pequeno do WebFetch; confira os trechos criticos (seguranca do socket, `--privileged`) antes de decidir.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

<!-- Dominios novos para agentes/fontes-confiaveis.json, com o motivo. O humano decide. -->

- `code.claude.com` (documentacao do Claude Code: hooks, permissoes, -p, devcontainer), se ainda nao estiver na lista.
- `docs.docker.com` e `docs.podman.io` (Docker/Podman: rootless, userns, compose), para Seguranca e Dev avaliarem a opcao do item 2.
- `github.com/tmux/tmux/wiki` (tmux FAQ), para o papel que manter `ferramentas/tarefa`.

## Catalogacao

<!-- Preenchido pelo Bibliotecario: decisao e notas finais. -->
