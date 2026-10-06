---
tipo: referencia
status: ativo
origem: SEARCH-0010 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0010
tarefa: T-0018
autor: Anthropic (documentacao oficial do Claude Code)
url: https://code.claude.com/docs/en/managed-settings
acessado_em: 2026-10-05
confianca: media
fontes: ["https://code.claude.com/docs/en/managed-settings", "https://code.claude.com/docs/en/env-vars", "https://code.claude.com/docs/en/settings"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.2xx (docs de 2026-10-05)"
revisar_em: 2027-01-05
criado: 2026-10-05
decisao: promovido
tags: [claude-code, managed-settings, container, claude-config-dir, seguranca]
---
# Managed settings do Claude Code no Linux ficam em /etc/claude-code e a documentacao nao liga esse caminho ao CLAUDE_CONFIG_DIR

## Resumo

- A pagina de managed settings lista o arquivo de politica no Linux/WSL como `/etc/claude-code/managed-settings.json` (mais `managed-settings.d/` e `managed-mcp.json` na mesma pasta).
- `CLAUDE_CONFIG_DIR` e descrita como o local das settings do usuario, do historico de sessoes, dos plugins e do `.credentials.json` (substitui `~/.claude`). Nenhuma pagina consultada diz que ela muda o caminho da politica gerenciada. Um resumo anterior dizia `<CLAUDE_CONFIG_DIR>/managed/settings.json`; isso **nao se confirmou** em nenhuma fonte.
- Precedencia: a politica gerenciada vence todas as outras settings.
- O sandbox do Claude Code ja protege contra **escrita** em `~/.claude` e na pasta de `CLAUDE_CONFIG_DIR` nos comandos de shell (a leitura nao e protegida; ver nota derivada).

## O que aproveitar

Em container, a trava do modo bypass vai em `/etc/claude-code/managed-settings.json`, dono root e somente leitura para o usuario do agente.

Teste que fecha a duvida (T-0020): com `CLAUDE_CONFIG_DIR` definida, rodar `claude doctor` ou `/status` e ver se a politica aparece como ativa.

## Ressalvas

Ausencia de afirmacao na doc nao e prova negativa: por isso `confianca: media` e o teste recomendado. Links confiaveis: [Deploy managed settings](https://code.claude.com/docs/en/managed-settings) (caminho por sistema), [Variaveis de ambiente](https://code.claude.com/docs/en/env-vars) (o que `CLAUDE_CONFIG_DIR` controla), [Settings](https://code.claude.com/docs/en/settings) (precedencia e arquivos do usuario).

## Notas derivadas

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]
- [[Sandbox do Claude Code so protege a pasta de configuracao contra escrita - negue a leitura da credencial em managed settings]]: o que colocar no managed settings para proteger a credencial.
- [[CLAUDE_CONFIG_DIR e herdada pelos hooks como qualquer variavel do ambiente e as transcricoes ficam em projects dentro dela]]: outra duvida sobre `CLAUDE_CONFIG_DIR`.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `30_Referencias`. Sem duplicata: a nota da Dev Container Feature cita `/etc/claude-code/` mas nao trata a interacao com `CLAUDE_CONFIG_DIR`. Atende o item 1 do SEARCH-0010.
