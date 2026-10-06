---
tipo: problema-solucao
status: ativo
origem: SEARCH-0010 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: media
fontes: ["https://code.claude.com/docs/en/sandboxing", "https://code.claude.com/docs/en/settings-reference#sandbox-enableweakernestedsandbox"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.2xx (docs de 2026-10-05)"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-01-05
tags: [claude-code, sandbox, bubblewrap, container, seguranca]
---
# Bubblewrap do Claude Code em container sem privilegio falha no /proc e enableWeakerNestedSandbox resolve ao custo de isolamento

## Sintoma

Em container sem privilegio, o comando executado dentro do sandbox do Claude Code falha com `bwrap: Can't mount proc on /newroot/proc: Operation not permitted`.

## Ambiente

Claude Code 2.1.2xx no Linux, dentro de container Docker sem `--privileged`. Em hosts Ubuntu 24.04+ a doc cita ainda a restricao `kernel.apparmor_restrict_unprivileged_userns=1`, que se resolve no host com perfil AppArmor para o `bwrap`; dentro do container vale o perfil do Docker.

## Causa raiz

O bubblewrap tenta montar um `/proc` novo no namespace do comando, e o container sem privilegio nao tem permissao para isso.

## Solucao

Ligar `sandbox.enableWeakerNestedSandbox: true`: o sandbox passa a fazer bind do `/proc` que o container ja tem, em vez de montar outro.

**Custo (declarado pela doc):** os comandos enxergam informacao de processos que um `/proc` novo esconderia. A doc diz para usar so quando o container externo ja der o isolamento necessario e que o modo "enfraquece consideravelmente" a seguranca.

Lembretes da doc:

- o sandbox cobre so comandos de shell (Bash, PowerShell, Monitor); ferramentas de arquivo, MCP e hooks rodam fora dele;
- `docker` e incompativel com o sandbox (usar `excludedCommands`);
- nunca liberar `/var/run/docker.sock` via `allowUnixSockets`.

## Como verificar que foi resolvido

**Nao verificado.** A doc so trata o erro do `/proc`. Fica em aberto se, com seccomp e AppArmor padrao do Docker e `cap_drop: ALL`, o bubblewrap chega a criar o user namespace. Teste proposto: `docker run` com as opcoes finais do container e, dentro dele, `bwrap --unshare-user --ro-bind / / true`, depois um comando sandboxed de verdade.

## O que nao funcionou

Nada tentado ainda; so leitura da documentacao oficial (sem teste).

## Origem

SEARCH-0010, item 6, pedido pelo Engenheiro na T-0018 (container do ambiente, projeto `ambiente`). Links confiaveis:

- [Sandboxing](https://code.claude.com/docs/en/sandboxing#bubblewrap-fails-to-start-inside-a-container): erro do `/proc` e `enableWeakerNestedSandbox`.
- [Settings reference - enableWeakerNestedSandbox](https://code.claude.com/docs/en/settings-reference#sandbox-enableweakernestedsandbox): definicao da chave.

## Relacionadas

- [[Docker dentro de container - socket do host equivale a root no host, DinD exige privileged, rootless tem limites]]: mesma familia de limites de container aninhado.
- [[Sandbox do Claude Code so protege a pasta de configuracao contra escrita - negue a leitura da credencial em managed settings]]: o que o sandbox nao protege, mesmo funcionando.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como problema-solucao. Sem duplicata no Brain. Confianca media: fonte oficial, sem teste; a lacuna do user namespace ficou declarada.
