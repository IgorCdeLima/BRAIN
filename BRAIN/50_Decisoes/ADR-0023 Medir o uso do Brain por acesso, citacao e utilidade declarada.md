---
tipo: decisao
status: aceita
decidido_em: 2026-10-02
decidido_por: humano
substituida_por:
criado: 2026-10-02
tags: [brain, telemetria, uso, hooks, bibliotecario, ambiente]
---
# ADR-0023 Medir o uso do Brain por acesso, citacao e utilidade declarada

## Contexto

- O humano nao sabe quanto o Brain e acessado nem se as notas sao uteis (`ADM-0017`).
- O hook `registrar_evento.py` registra Edit, Write, Bash e PowerShell, mas nao `Read`: leitura de nota nao deixa rastro em `logs/`.
- As transcricoes do Claude Code tem papel, sessao, pasta e cada caminho lido, mas sao apagadas depois de um prazo; hoje so ha dados a partir de 2026-09-30.
- Nas sessoes de worktree, os hooks de log vem do `.claude/settings.json` de cada projeto (outro repositorio). Hook de ambiente posto ali precisaria ser repetido em todo projeto novo.
- Primeira medicao (2026-09-30 a 2026-10-02, 74 sessoes): a maioria das leituras e de regras e templates (`60`, `70`, `99`); `10_Conhecimento` teve 24 leituras em 14 sessoes; 51 notas de conhecimento estao citadas em trabalhos, 14 foram lidas e nunca citadas.

## Decisao

Medir em tres niveis, do mais fraco ao mais forte:

1. **Acesso:** hook `PostToolUse` `ferramentas/hooks/registrar_brain.py` (matcher `Read|Bash|PowerShell`) grava cada acesso ao Brain em `logs/brain/AAAA-MM.jsonl` (fora do Git): data, papel, tarefa, sessao, ferramenta, leitura ou busca, pasta e nota. **So o caminho**; nunca o comando nem conteudo. Ligado **na definicao de cada papel** (`agentes/.claude/agents/*.md`), para valer em qualquer projeto sem tocar no repositorio dele.
2. **Uso:** citacao `[[Nota]]` em `operacao/`, `projetos/*/qualidade` e `projetos/*/docs` (regra ja existente no `CLAUDE.md`).
3. **Utilidade declarada:** linha "Brain consultado" na Entrega do cartao e no VER: `[[Nota]] - ajudou: sim | parcial | nao - por que`. Unico sinal que diz se o dado armazenado ajudou.

`ferramentas/uso_brain.py` (somente leitura) junta o log, as transcricoes (periodo anterior e sessoes sem log, sem contar a mesma sessao duas vezes) e os registros de trabalho, e separa **regras** (60, 70, 99) de **conhecimento**. Situacao de cada nota: util (declarada), usada (citada), lida e nao citada, recente, sem uso. O **Bibliotecario** roda o relatorio todo mes (ou a cada ~10 tarefas) e age sobre notas sem uso, arquivadas ainda lidas, Inbox mais lido e "ajudou: nao".

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| So as transcricoes, sem hook | Nada muda no ambiente; ja ha dados | Somem depois do prazo; o relatorio mensal perderia a historia |
| Aumentar `cleanupPeriodDays` | Guarda tudo | Guarda tambem todo o conteudo das conversas so para medir caminhos |
| `Read` no `registrar_evento.py` (logs de sessao) | Um hook so | Incha os logs de sessao; formato Markdown ruim para contar; teria de entrar no `.claude` de cada projeto |
| Hook no `.claude/settings.json` de cada projeto | Pega tambem sessao sem papel | Repetir em todo projeto; mexe em repositorio de projeto |
| **Hook na definicao do papel (escolhida)** | Vale em todo projeto atual e futuro; um lugar so | Sessao sem papel nao e medida (ja nao deveria trabalhar) |
| So citacao, sem acesso | Simples | Nao mostra o que foi lido e descartado, nem o que e procurado |

## Consequencias

- **Positivas:** dados por pasta, papel, tarefa e nota; notas mortas e notas que nao ajudam aparecem; o Inbox mais lido orienta a curadoria; o mesmo leitor de transcricoes serve ao `ADM-0011` (tokens).
- **Negativas / riscos:** um processo Python a mais por `Read` e `Bash` (hook leve, timeout de 10 s, nunca falha); busca por `grep` que so lista arquivos conta como busca na pasta, nao como leitura; "Brain consultado" depende de os papeis preencherem; leitura no Inbox de nota depois promovida ou arquivada aparece na pasta nova.

## Relacionadas

- `ADM-0017` - pedido do humano.
- [[Rastreabilidade]] - formato de `logs/brain`.
- [[Bibliotecario]] - rotina mensal.
- [[ADR-0012 Logs em Markdown fora do Git]] - logs fora do Git (aqui em JSONL, por ser contagem).
