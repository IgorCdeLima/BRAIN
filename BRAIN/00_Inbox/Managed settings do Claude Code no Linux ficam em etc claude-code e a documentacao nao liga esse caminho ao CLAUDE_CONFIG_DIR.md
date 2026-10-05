---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: media
fontes: [https://code.claude.com/docs/en/managed-settings, https://code.claude.com/docs/en/env-vars, https://code.claude.com/docs/en/settings]
verificado_em: 2026-10-05
valido_para: Claude Code 2.1.2xx (docs de 2026-10-05)
criado: 2026-10-05
decisao:
tags: [claude-code, managed-settings, container, claude-config-dir, seguranca]
---
# Managed settings do Claude Code no Linux ficam em /etc/claude-code e a documentacao nao liga esse caminho ao CLAUDE_CONFIG_DIR

## Conteudo proposto

- A pagina de managed settings lista o arquivo de politica no Linux/WSL como `/etc/claude-code/managed-settings.json` (mais `managed-settings.d/` e `managed-mcp.json` na mesma pasta).
- `CLAUDE_CONFIG_DIR` e descrita como o local de settings do usuario, historico de sessoes, plugins e `.credentials.json` (substitui `~/.claude`). Nenhuma pagina consultada diz que ela muda o caminho da politica gerenciada. O resumo que dizia `<CLAUDE_CONFIG_DIR>/managed/settings.json` **nao foi confirmado** em nenhuma fonte.
- Para o container: a trava do modo bypass vai em `/etc/claude-code/managed-settings.json`, dono root, somente leitura para o usuario do agente. Como a doc nao e explicita sobre a interacao, o teste do Dev (T-0020) deve confirmar: com `CLAUDE_CONFIG_DIR` definida, pedir `claude doctor` / `/status` e ver se a politica aparece como ativa.
- O sandbox do Claude Code ja protege contra escrita em `~/.claude` ou na pasta de `CLAUDE_CONFIG_DIR` nos comandos de shell.

## Evidencia

Leitura das paginas oficiais em 2026-10-05. Ausencia de afirmacao na doc nao e prova negativa: por isso `confianca: media` e o teste recomendado.

## Links confiaveis

- [Deploy managed settings](https://code.claude.com/docs/en/managed-settings): caminho do arquivo por sistema operacional.
- [Variaveis de ambiente](https://code.claude.com/docs/en/env-vars): o que `CLAUDE_CONFIG_DIR` controla.
- [Settings](https://code.claude.com/docs/en/settings): precedencia (gerenciado vence tudo) e onde ficam os arquivos do usuario.

## Por que e reaproveitavel

Qualquer imagem/container que precise travar permissoes do agente (RF-24 do projeto ambiente).

## Relacionadas no Brain

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]

## Decisao do Bibliotecario
