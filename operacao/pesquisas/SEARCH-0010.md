---
tipo: pesquisa
id: SEARCH-0010
status: catalogada
urgencia: nao-bloqueante
pedido_por: engenheiro
tarefa: T-0018
criado: 2026-10-05
pesquisado_por: pesquisador
pesquisado_em: 2026-10-05
catalogado_em: 2026-10-05
notas: ["Managed settings do Claude Code no Linux ficam em etc claude-code e a documentacao nao liga esse caminho ao CLAUDE_CONFIG_DIR", "CLAUDE_CONFIG_DIR e herdada pelos hooks como qualquer variavel do ambiente e as transcricoes ficam em projects dentro dela", "Claude Code numa imagem - instalador nativo aceita versao exata e DISABLE_UPDATES trava toda atualizacao", "Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento", "Podman rootless dentro de container Docker - a doc oficial do Podman usa privileged e fuse, sem privileged nao esta documentado", "Codex CLI instala por script, guarda credencial em CODEX_HOME auth.json e limita comandos com sandbox bwrap e seccomp", "Proxy de socket do Docker filtra por secao da API e nao e fronteira de seguranca - a doc nao cobre compose nem o corpo das requisicoes"]
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

- **Resumo (3 a 5 linhas):** (1) Managed settings no Linux: `/etc/claude-code/managed-settings.json`; nenhuma doc liga isso a `CLAUDE_CONFIG_DIR` (o `<dir>/managed` do resumo antigo nao se confirmou). (2) Hooks herdam o ambiente do pai, entao a variavel chega; transcricoes ficam em `<CLAUDE_CONFIG_DIR>/projects`. (3) apt mantem 60 versoes: `apt install claude-code=2.1.285-1` vale. (4) Podman aninhado: README oficial usa `--privileged`/fuse/seccomp=unconfined; sem privileged nao ha receita. (6) Bubblewrap: `enableWeakerNestedSandbox` resolve o `/proc`, custo em isolamento. (7) Codex: ver nota. (5) docker-socket-proxy filtra por rota, nao documenta compose nem corpo.
- **Notas geradas no Inbox:** [[Managed settings do Claude Code no Linux ficam em etc claude-code e a documentacao nao liga esse caminho ao CLAUDE_CONFIG_DIR]], [[CLAUDE_CONFIG_DIR e herdada pelos hooks como qualquer variavel do ambiente e as transcricoes ficam em projects dentro dela]], [[O repositorio apt do Claude Code mantem versoes antigas e permite fixar com apt install claude-code igual versao]], [[Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento]], [[Podman rootless dentro de container Docker - a doc oficial do Podman usa privileged e fuse, sem privileged nao esta documentado]], [[Codex CLI instala por script, guarda credencial em CODEX_HOME auth.json e limita comandos com sandbox bwrap e seccomp]], [[Proxy de socket do Docker filtra por secao da API e nao e fronteira de seguranca - a doc nao cobre compose nem o corpo das requisicoes]]
- **Links confiaveis:** code.claude.com/docs/en/{managed-settings,env-vars,hooks,setup,sandboxing}; downloads.claude.ai (indice apt); github.com/containers/image_build (podman); github.com/Tecnativa/docker-socket-proxy; learn.chatgpt.com/docs (Codex).
- **Sem resposta / limites:** nao confirmado por teste: item 1 (interacao managed x `CLAUDE_CONFIG_DIR`) e item 2 (so inferido do heranca de ambiente); item 6 (userns com seccomp/AppArmor padrao e `cap_drop: ALL`: a doc so trata o `/proc`); item 4 sem `--privileged` e `podman compose` com `docker-compose`; item 5 (secoes exigidas pelo compose e inspecao de corpo); item 7 (chaves do `config.toml`, comportamento em container sem privilegio; pagina de sandboxing dedicada deu 404). Recomendado teste no T-0020. `curl` ao indice apt e negado ao papel: usei WebFetch.
- **Conteudo suspeito descartado:** nenhum.

## Dominios propostos

- `learn.chatgpt.com` (e `developers.openai.com`, que redireciona para ele): documentacao oficial do Codex CLI, necessaria para a T-0023.
- `downloads.claude.ai`: ja usado nas instrucoes de apt do Claude Code (chave e indice de versoes); conferir se esta na lista.
- `github.com/containers` e `github.com/Tecnativa`: so se algum papel precisar abrir os READMEs; propor apenas se a lista nao cobrir github.com.

## Catalogacao

Decisao (2026-10-05): os 7 candidatos do Pesquisador foram **promovidos**; nenhum foi devolvido. Confianca media mantida (documentacao oficial, nada executado); a nota de `CLAUDE_CONFIG_DIR` e hooks entrou como `rascunho` com confianca baixa (conclusao inferida).

- [[Managed settings do Claude Code no Linux ficam em etc claude-code e a documentacao nao liga esse caminho ao CLAUDE_CONFIG_DIR]] (30_Referencias; itens 1)
- [[CLAUDE_CONFIG_DIR e herdada pelos hooks como qualquer variavel do ambiente e as transcricoes ficam em projects dentro dela]] (30_Referencias, rascunho; item 2)
- [[Claude Code numa imagem - instalador nativo aceita versao exata e DISABLE_UPDATES trava toda atualizacao]] (30_Referencias; item 3, fundida com o candidato do apt, arquivado em 90_Arquivo)
- [[Podman rootless dentro de container Docker - a doc oficial do Podman usa privileged e fuse, sem privileged nao esta documentado]] (30_Referencias; item 4)
- [[Proxy de socket do Docker filtra por secao da API e nao e fronteira de seguranca - a doc nao cobre compose nem o corpo das requisicoes]] (30_Referencias; item 5)
- [[Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento]] (10_Conhecimento, problema-solucao; item 6)
- [[Codex CLI instala por script, guarda credencial em CODEX_HOME auth.json e limita comandos com sandbox bwrap e seccomp]] (30_Referencias; item 7)

Links confiaveis preservados em cada nota. Lacunas continuam abertas e dependem de teste (T-0020): interacao managed settings x `CLAUDE_CONFIG_DIR`, heranca da variavel pelos hooks, user namespace com seccomp padrao e `cap_drop: ALL`, Podman sem `--privileged`, secoes exigidas pelo compose no proxy. Os dominios propostos continuam para decisao do humano.
