---
tipo: problema-solucao
status: ativo
origem: agente/engenheiro (T-0018, SEC-T0018-01), curado pelo Bibliotecario
tarefa: T-0018
confianca: media
fontes: ["https://code.claude.com/docs/en/sandboxing"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.2xx (docs de 2026-10-05), Linux"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-01-05
tags: [claude-code, sandbox, credencial, managed-settings, container, seguranca]
---
# Sandbox do Claude Code so protege a pasta de configuracao contra escrita - negue a leitura da credencial em managed settings

## Sintoma

Com o sandbox ligado e a escrita confinada ao worktree, parece que a credencial do Claude Code esta protegida. Nao esta: um comando sandboxed ainda consegue **ler** `.credentials.json`.

## Ambiente

Claude Code 2.1.2xx no Linux (host ou container), sandbox ligado, credencial no mesmo usuario que roda os comandos do agente.

## Causa raiz

A pasta `~/.claude` (ou a de `CLAUDE_CONFIG_DIR`), `.claude.json` e `.credentials.json` sao "protected paths" so contra **escrita**. A leitura padrao dos comandos sandboxed e "most of the machine, including credential files", e a doc diz: "There is no built-in credential deny list". Somado a qualquer dominio liberado (ex.: `github.com`, que a doc avisa permitir domain fronting), um agente enganado le a credencial e a envia para fora.

## Solucao

Valida para todos os papeis, inclusive os que "leem tudo":

1. Em managed settings (`/etc/claude-code/managed-settings.json`, dono root): `sandbox.credentials.files` com `{"path": "<CLAUDE_CONFIG_DIR>/.credentials.json", "mode": "deny"}` e o mesmo para `.claude.json`. Uma entrada `deny` em managed **trava a chave**: so o managed pode desligar o isolamento de arquivos.
2. `sandbox.filesystem.denyRead` para `<CLAUDE_CONFIG_DIR>/projects` (as transcricoes trazem o conteudo de todas as sessoes).
3. As mesmas pastas como regras `Read(...)` em `permissions.deny`: o `denyRead` do sandbox nao vale para a ferramenta Read.
4. Em container sem privilegio, travar em `false` as chaves que enfraquecem o sandbox (`enableWeakerNetworkIsolation`, `network.allowAllUnixSockets`, `network.allowLocalBinding`) e instalar o filtro seccomp opcional (`@anthropic-ai/sandbox-runtime`), que e o que bloqueia sockets Unix.

**Efeito colateral a prever:** ferramentas que leem as transcricoes pelo Bash do agente (relatorios de consumo e de uso) deixam de funcionar. Rodar no host ou ler o que os hooks (fora do sandbox) gravam.

## Como verificar que foi resolvido

Numa sessao com credencial descartavel, `test -r "$CLAUDE_CONFIG_DIR/.credentials.json" && echo LEGIVEL` nao imprime nada e o `Read` do arquivo e negado. **Teste ainda nao executado** (nao havia container).

## O que nao funcionou

Confiar so no confinamento de escrita ao worktree: nao cobre leitura nem envio da credencial.

## Origem

T-0018 (projeto `ambiente`): SEC-T0018-01 e a correcao do RF-35. Leitura da pagina oficial em 2026-10-05 (tabela "What the sandbox restricts", "Protect credentials", "Protected paths", "Enforce sandboxing with managed settings", "Security limitations"). Link confiavel: [Sandboxing](https://code.claude.com/docs/en/sandboxing#protect-credentials).

## Relacionadas

- [[CWE-522 token de ferramenta legivel pelo mesmo usuario se trata com permissao 0600 e escopo minimo]]: a classe de problema; esta nota e o controle especifico do Claude Code.
- [[Managed settings do Claude Code no Linux ficam em etc claude-code e a documentacao nao liga esse caminho ao CLAUDE_CONFIG_DIR]]: onde o arquivo de politica fica.
- [[Bubblewrap do Claude Code em container sem privilegio falha no proc e enableWeakerNestedSandbox resolve ao custo de isolamento]]: o sandbox em container.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como problema-solucao. Sem duplicata. Confianca media: fonte oficial, sem teste executado.
