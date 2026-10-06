---
tipo: referencia
status: rascunho
origem: SEARCH-0010 (Pesquisador), curado pelo Bibliotecario
pesquisa: SEARCH-0010
tarefa: T-0018
autor: Anthropic (documentacao oficial do Claude Code)
url: https://code.claude.com/docs/en/env-vars
acessado_em: 2026-10-05
confianca: baixa
fontes: ["https://code.claude.com/docs/en/env-vars", "https://code.claude.com/docs/en/hooks"]
verificado_em: 2026-10-05
valido_para: "Claude Code 2.1.2xx (docs de 2026-10-05)"
revisar_em: 2026-11-05
criado: 2026-10-05
decisao: promovido
tags: [claude-code, hooks, claude-config-dir, transcricoes, container]
---
# CLAUDE_CONFIG_DIR e herdada pelos hooks como qualquer variavel do ambiente e as transcricoes ficam em projects dentro dela

## Resumo

**Pista a verificar por teste, nao fato confirmado.** Leitura das docs oficiais, sem prova direta:

- A pagina `hooks` diz que o processo do hook herda o ambiente do pai, exceto `OTEL_*` e o que `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1` remove. `CLAUDE_CONFIG_DIR` nao esta nessas excecoes; logo, se estiver no ambiente do `claude`, chega aos hooks e subprocessos. A lista de variaveis documentadas para hooks (`CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`...) nao a cita, e foi dessa ausencia que veio o resumo antigo "nao chega": ausencia na lista, nao proibicao.
- A pagina `env-vars` recomenda definir `CLAUDE_CONFIG_DIR` no bloco `env` das settings de usuario ou gerenciadas (e nao so por `export`), para o servico em segundo plano herdar. `CLAUDE_CODE_PROJECT_DIR_NAME`, junto com ela, escolhe o nome da pasta de transcricoes dentro de `projects/`.
- As transcricoes ficam em `<CLAUDE_CONFIG_DIR>/projects/`. Com `CLAUDE_CONFIG_DIR=$HOME/.claude` o caminho coincide com `Path.home()/.claude/projects`.

## O que aproveitar

Hook ou ferramenta que le transcricoes (telemetria, relatorio de uso do Brain) deve ler `CLAUDE_CONFIG_DIR` com fallback para `~/.claude`, em vez de fixar `~/.claude/projects`: com outro valor, o caminho fixo nao acha nada.

Teste que fecha a duvida: um hook que imprime `env | grep CLAUDE`.

## Ressalvas

- `confianca: baixa`: conclusao por inferencia da regra geral de heranca de ambiente; nao ha texto que afirme que `CLAUDE_CONFIG_DIR` chega aos hooks. Por isso a nota esta como `rascunho`, com revisao em 1 mes.
- Links confiaveis: [Hooks](https://code.claude.com/docs/en/hooks) (ambiente herdado) e [Variaveis de ambiente](https://code.claude.com/docs/en/env-vars) (`CLAUDE_CONFIG_DIR`, `CLAUDE_CODE_PROJECT_DIR_NAME`).

## Notas derivadas

- [[Claude Code em container usa a Dev Container Feature, volume em CLAUDE_CONFIG_DIR e usuario nao root]]
- [[Sandbox do Claude Code so protege a pasta de configuracao contra escrita - negue a leitura da credencial em managed settings]]: a mesma pasta `projects` tem a leitura negada pelo sandbox, o que afeta ferramentas que leem transcricoes pelo Bash do agente.

## Decisao do Bibliotecario

Promovido como `rascunho` (2026-10-05) para `30_Referencias`: a fonte e oficial, mas a conclusao e inferida e a confianca e baixa. Sem duplicata. Quem confirmar por teste (T-0020) deve subir `confianca` e mudar `status` para `ativo`.
