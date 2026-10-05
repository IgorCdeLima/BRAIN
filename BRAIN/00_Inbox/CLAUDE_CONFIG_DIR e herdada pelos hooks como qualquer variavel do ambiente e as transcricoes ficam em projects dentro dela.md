---
tipo: candidato
status: inbox
tipo_proposto: referencia
origem: agente/pesquisador
tarefa: T-0018
pesquisa: SEARCH-0010
confianca: baixa
fontes: [https://code.claude.com/docs/en/env-vars, https://code.claude.com/docs/en/hooks]
verificado_em: 2026-10-05
valido_para: Claude Code 2.1.2xx (docs de 2026-10-05)
criado: 2026-10-05
decisao:
tags: [claude-code, hooks, claude-config-dir, transcricoes, container]
---
# CLAUDE_CONFIG_DIR e herdada pelos hooks como qualquer variavel do ambiente e as transcricoes ficam em projects dentro dela

## Conteudo proposto

- A pagina `hooks` diz que o processo do hook herda o ambiente do pai, exceto `OTEL_*` e o que `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` remove. `CLAUDE_CONFIG_DIR` nao esta nessas excecoes, entao, se estiver no ambiente do `claude`, chega aos hooks e subprocessos. A lista de variaveis documentadas para hooks (`CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`...) nao a cita, e foi disso que veio o resumo "nao chega": ausencia na lista, nao proibicao.
- A pagina `env-vars` recomenda definir `CLAUDE_CONFIG_DIR` no bloco `env` das settings de usuario/gerenciadas (e nao so por `export`) para o servico em segundo plano herdar; a variavel `CLAUDE_CODE_PROJECT_DIR_NAME` junto com ela escolhe o nome da pasta `projects/` das transcricoes.
- Transcricoes: ficam em `<CLAUDE_CONFIG_DIR>/projects/`. Com `CLAUDE_CONFIG_DIR=$HOME/.claude` o caminho coincide com `Path.home()/.claude/projects`. Se for outro valor, hook/ferramenta que hardcoda `~/.claude/projects` nao acha nada: leia a variavel com fallback.
- Fica sem prova documental direta; confirmar por teste (hook que imprime `env | grep CLAUDE`).

## Evidencia

Leitura de docs oficiais; sem teste executado.

## Links confiaveis

- [Hooks](https://code.claude.com/docs/en/hooks): ambiente herdado pelos comandos de hook e variaveis documentadas.
- [Variaveis de ambiente](https://code.claude.com/docs/en/env-vars): `CLAUDE_CONFIG_DIR`, `CLAUDE_CODE_PROJECT_DIR_NAME`.

## Por que e reaproveitavel

Ferramentas de telemetria/uso do Brain que leem transcricoes dentro de containers.

## Relacionadas no Brain

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]

## Decisao do Bibliotecario
