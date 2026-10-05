---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: media
fontes: [https://code.claude.com/docs/en/sandboxing]
verificado_em: 2026-10-05
valido_para: Claude Code 2.1.2xx (docs de 2026-10-05)
criado: 2026-10-05
decisao:
tags: [claude-code, sandbox, bubblewrap, container, seguranca]
---
# Bubblewrap do Claude Code em container sem privilegio falha no /proc e enableWeakerNestedSandbox resolve ao custo de isolamento

## Conteudo proposto

- Sintoma documentado: em container sem privilegio o comando sandboxed falha com `bwrap: Can't mount proc on /newroot/proc: Operation not permitted`.
- Solucao documentada: `sandbox.enableWeakerNestedSandbox: true` faz o sandbox fazer bind do `/proc` existente do container em vez de montar um novo. Custo declarado: expoe aos comandos informacao de processos que um `/proc` novo esconderia; a doc diz para usar so quando o container externo ja der o isolamento necessario, e que o modo "enfraquece consideravelmente" a seguranca.
- **Nao respondido pela doc:** se, com seccomp/AppArmor padrao do Docker e `cap_drop: ALL`, o bubblewrap chega a criar o user namespace (a doc so cita o erro do `/proc`). Em hosts Ubuntu 24.04+ a doc cita a restricao `kernel.apparmor_restrict_unprivileged_userns=1`, resolvida no host com perfil AppArmor para `bwrap`; dentro do container o perfil e o do Docker. Precisa de teste: `docker run` com as opcoes finais e `bwrap --unshare-user --ro-bind / / true`.
- Lembrete da doc: o sandbox cobre so comandos de shell (Bash, PowerShell, Monitor); ferramentas de arquivo, MCP e hooks rodam fora dele; `docker` e incompativel (usar `excludedCommands`). Nunca liberar `/var/run/docker.sock` via `allowUnixSockets`.

## Evidencia

Pagina oficial `sandboxing` (secoes "Bubblewrap fails to start inside a container" e riscos). Sem teste.

## Links confiaveis

- [Sandboxing](https://code.claude.com/docs/en/sandboxing#bubblewrap-fails-to-start-inside-a-container): erro do `/proc` e `enableWeakerNestedSandbox`.
- [Settings reference - enableWeakerNestedSandbox](https://code.claude.com/docs/en/settings-reference#sandbox-enableweakernestedsandbox): definicao da chave.

## Por que e reaproveitavel

Decide se o agente em container usa o sandbox do Claude Code ou so o isolamento do proprio container.

## Relacionadas no Brain

- [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]

## Decisao do Bibliotecario
