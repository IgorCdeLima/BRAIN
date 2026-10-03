---
tipo: decisao
status: aceita
decidido_em: 2026-10-02
decidido_por: humano
substituida_por:
criado: 2026-10-02
tags: [obsidian, brain, bibliotecario, ferramentas, ambiente]
---
# ADR-0025 Agentes mantem o cofre sem usar o Obsidian como ferramenta

## Contexto

- O Bibliotecario movia e renomeava notas so com `obsidian move` (o CLI atualiza os links). O CLI exige o aplicativo aberto, e o lancador recusava o papel sem ele.
- Isso prende o ambiente a uma interface grafica e atrapalha a ida para Docker ([[ADM-0009]], em stand by).
- O CLI so atualiza links dentro do cofre; links para notas do Brain em `operacao/`, `CLAUDE.md` e `agentes/` ficavam de fora.
- Uso medido em 2026-10-02: 4 commits com renomeacao no `BRAIN/` desde 2026-09-01; 154 notas, todos os links `[[Nome]]` simples.
- O humano continua usando o Obsidian como cofre e leitor ([[ADM-0018]]): "mantenha os padroes de escrita e de como e realizada a logica e links do Obsidian".

## Decisao

1. `BRAIN/` continua sendo o cofre do Obsidian do humano. Os agentes **nao usam o aplicativo nem o CLI do Obsidian**.
2. Mover e renomear notas: `ferramentas/notas.py mover` (so biblioteca padrao do Python), com as convencoes do Obsidian:
   - `[[Nome]]` resolve pelo nome em qualquer pasta; link reescrito segue `newLinkFormat` de `.obsidian/app.json` (padrao `shortest`: so o nome se for unico, senao o caminho completo a partir do cofre).
   - So os links que deixariam de apontar para a mesma nota sao reescritos; estilo (wikilink ou Markdown), `!`, `#cabecalho`, `#^bloco` e `|alias` (inclusive `\|` em tabela) sao preservados; link Markdown com `%20` ou `<...>` mantem a forma.
   - Links em propriedades do frontmatter sao atualizados; o resto do frontmatter nao muda.
   - Blocos de codigo, codigo em linha e comentarios (HTML e `%%`) nao sao tocados; `.obsidian/` tambem nao.
   - Link ambiguo ou quebrado nao e alterado; o script avisa.
   - Wikilinks em `operacao/`, `CLAUDE.md` e `agentes/` tambem sao atualizados.
   - `git mv` para arquivo versionado; codificacao UTF-8 e fim de linha preservados; `--simular` mostra a lista antes.
3. Manutencao: `notas.py orfas` e `notas.py quebrados` substituem `obsidian orphans` e `obsidian unresolved`.
4. O perfil do Bibliotecario troca `obsidian *` pelo script e nega `mv`/`git mv`/`Move-Item`/`Rename-Item`; o lancador deixa de exigir o Obsidian aberto.

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| Manter o Obsidian CLI | Logica oficial do Obsidian | Exige o aplicativo aberto; nao atualiza links fora do cofre; nao combina com Docker |
| `git mv` + busca e troca manual | Nada para manter | Erro humano em alias, cabecalho, link Markdown e nome repetido |
| Script proprio com as convencoes do Obsidian (escolhida) | Sem interface; cobre links fora do cofre; testavel; `--simular` | Precisa acompanhar mudancas de comportamento do Obsidian |

## Consequencias

- **Positivas:** o Bibliotecario roda sem interface grafica (Linux, Docker); links fora do cofre deixam de quebrar; `quebrados` mostra que os `[[ADM-####]]` das ADRs e regras ja nao resolvem no Obsidian (os ADM ficam fora do cofre).
- **Negativas / riscos:** a resolucao de link ambiguo e a regra exata do `shortest` foram implementadas pelo comportamento conhecido do Obsidian, sem conferencia na documentacao oficial; o humano confere abrindo o cofre de teste no Obsidian. Se o Obsidian mudar o formato, o script precisa acompanhar.

## Relacionadas

- [[ADM-0018]] - pedido e execucao.
- [[ADM-0009]] - ambiente em Docker (stand by).
- [[Bibliotecario]] - regra que usa o script.
