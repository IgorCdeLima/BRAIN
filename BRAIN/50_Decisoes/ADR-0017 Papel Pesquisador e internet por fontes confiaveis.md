---
tipo: decisao
status: aceita
decidido_em: 2026-09-30
decidido_por: Igor
substituida_por:
criado: 2026-09-30
tags: [ambiente, agentes, pesquisa, seguranca, brain]
---
# ADR-0017 Papel Pesquisador e internet por fontes confiaveis

## Contexto

- Varios papeis podiam pesquisar na web (Designer e Seguranca com busca liberada; os demais com pergunta ao humano). Cada um repetia pesquisas e o resultado se perdia na sessao.
- Conteudo da web pode trazer instrucoes escondidas (*prompt injection*). Um papel que navega livremente **e** escreve codigo junta as duas coisas.
- O Brain cresce melhor quando a pesquisa vira nota curta com fonte, reaproveitada por todos, e isso tende a reduzir tokens nas proximas tarefas.

## Decisao

1. **Papel Pesquisador** (Sonnet, copia principal): unico com busca (WebSearch) e navegacao livre (WebFetch). So escreve em `operacao/pesquisas` e `BRAIN/00_Inbox`; `curl`/`wget` negados. Atende pedidos `SEARCH-####` e pesquisas de pauta; toda nota traz **links confiaveis**.
2. **Internet por fontes confiaveis** para os demais papeis: o lancador injeta no perfil `WebFetch(domain:...)` para os dominios de `agentes/fontes-confiaveis.json` (N4, so o humano altera) e nega WebSearch. Outros sites caem em "pergunta ao humano". `curl` so em `localhost`.
3. **Pedido de pesquisa** `operacao/pesquisas/SEARCH-####.md` com status `nao-pesquisada -> em-pesquisa -> respondida | sem-resposta -> catalogada`, `urgencia` bloqueante ou nao, e rastreio de quem pediu, para qual tarefa e quem pesquisou.
4. O agente que pediu **nao espera o Bibliotecario**: com o SEARCH `respondida`, a nota do Inbox vale como pista. Novo status de cartao `aguardando-pesquisa` para pedidos bloqueantes.
5. A Seguranca pode rodar `pip-audit` e `osv-scanner` (consulta de dado da hora, nao navegacao).

## Alternativas consideradas

| Alternativa | Por que nao |
|---|---|
| Cada papel pesquisa livremente | Pesquisa repetida, sem catalogo, e todos os papeis expostos a injecao |
| Nenhum papel acessa a internet | O Designer precisa ver a aplicacao e todos precisam abrir a documentacao oficial citada nas notas |
| Pedinte espera a catalogacao do Bibliotecario | Quatro sessoes por duvida; o Inbox ja vale como pista pela hierarquia de conhecimento |

## Consequencias

- Duvida bloqueante custa duas sessoes extras (Pesquisador e retomada). Usar `nao-bloqueante` sempre que der para seguir com premissa.
- `github.com` na lista libera todo o GitHub; aceito pela utilidade (repositorios oficiais). Revisar se aparecer abuso.
- Padrao de `curl` por `*localhost*` e uma protecao pratica, nao absoluta; a lista de fontes e o isolamento do Pesquisador sao a protecao principal.
