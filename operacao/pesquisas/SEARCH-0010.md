---
tipo: pesquisa
id: SEARCH-0010
status: em-pesquisa
urgencia: nao-bloqueante
pedido_por: engenheiro
tarefa: T-0018
criado: 2026-10-05
pesquisado_por:
pesquisado_em:
catalogado_em:
notas: []
tags: [ambiente, container, claude-code, docker, podman, adm-0009]
---
# SEARCH-0010 - Fatos a confirmar para o container do ambiente (managed settings, CLAUDE_CONFIG_DIR, apt com versao, Podman aninhado, proxy de socket)

## Pergunta

1. **Claude Code - managed settings x `CLAUDE_CONFIG_DIR`:** com `CLAUDE_CONFIG_DIR` definida, o Claude Code ainda le `/etc/claude-code/managed-settings.json` (Linux), ou passa a ler `<CLAUDE_CONFIG_DIR>/managed/settings.json`? (Um resumo da pagina `env-vars` disse a segunda coisa; a pagina `devcontainer` manda copiar para `/etc/claude-code/`. Se for a segunda, a politica ficaria numa pasta gravavel pelo proprio usuario.)
2. **Claude Code - `CLAUDE_CONFIG_DIR` nos hooks:** o valor da variavel chega aos hooks e subprocessos? (O mesmo resumo disse que nao.) Vale tambem para `Path.home()/.claude/projects` como local das transcricoes quando `CLAUDE_CONFIG_DIR=$HOME/.claude`.
3. **Claude Code pelo apt:** o repositorio `downloads.claude.ai/claude-code/apt/{stable,latest}` mantem versoes antigas, permitindo `apt install claude-code=<versao>` (fixar versao exata)?
4. **Podman rootless dentro de um container Docker sem `--privileged`:** e possivel? Que opcoes exige (dispositivos como `/dev/fuse`, perfil seccomp/AppArmor, capabilities, `/etc/subuid` dentro do container)? `podman compose` com `docker-compose` como provedor funciona assim?
6. **Sandbox do Claude Code (bubblewrap) dentro de um container Docker sem privilegio** (acrescentado em 2026-10-05, decisao do humano de confinar o agente ao projeto): com o perfil seccomp e AppArmor padrao do Docker e `cap_drop: ALL`, o bubblewrap consegue criar o namespace de usuario? Basta `enableWeakerNestedSandbox: true` (a pagina `sandboxing` so cita o erro do `/proc`)? Se nao, qual o ajuste minimo no container e o que ele custa em isolamento?
7. **Codex CLI (OpenAI) em container** (acrescentado em 2026-10-05, T-0023): forma oficial de instalar no Linux, onde guarda a credencial de assinatura (pasta e variavel para mudar o local), como atualiza, e que mecanismo oferece para limitar escrita e rede dos comandos (sandbox/aprovacao) dentro de um container sem privilegio. Dominio provavel: documentacao oficial da OpenAI (propor em "Dominios propostos" se nao estiver na lista).
5. **Proxy do socket do Docker:** existe forma documentada (Docker ou projeto mantido) de expor ao container so parte da API do Docker (ex.: sem `privileged`, sem bind de `/`), suficiente para `docker compose build/run/up/down`? Que garantias e limites a documentacao declara?

## Contexto

T-0018 (Engenheiro, projeto `ambiente`, fase 2 do `ADM-0009`): requisitos e ADR-0001 `proposta` do container do ambiente em `projetos/ambiente/docs`. Itens 1 e 2 definem onde fica a trava do modo bypass (RF-24) e se as ferramentas acham as transcricoes (RF-15); item 3 pode mudar a recomendacao de instalacao (`docs/avaliacoes/instalacao-do-claude-code.md`); itens 4 e 5 alimentam a matriz `docs/avaliacoes/docker-dos-projetos.md` e a analise da Seguranca (T-0019). Host: Ubuntu 26.04, kernel 7.0, Docker Engine rootful, Claude Code 2.1.289. Nao bloqueante: o desenho segue com premissas; o Dev (T-0020) tambem pode confirmar 1 e 2 por teste.

## Ja buscado no Brain

`managed-settings`, `CLAUDE_CONFIG_DIR`, `podman`, `rootless`, `socket proxy`. Notas que cobrem parte: [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]] (diz `/etc/claude-code/managed-settings.json`, sem tratar a interacao com `CLAUDE_CONFIG_DIR`) e [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]] (nao trata Podman aninhado nem proxy). O Engenheiro leu `code.claude.com/docs/en/setup` e `devcontainer` em 2026-10-05 (respondem instalacao e versao); `env-vars` veio truncada no WebFetch.

---

## Resposta

- **Resumo (3 a 5 linhas):**
- **Notas geradas no Inbox:** [[ ]]
- **Links confiaveis:**
- **Sem resposta / limites:**
- **Conteudo suspeito descartado:**

## Dominios propostos

- 

## Catalogacao
