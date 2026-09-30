---
tipo: decisao
status: aceita
decidido_em: 2026-09-30
decidido_por: Igor
substituida_por:
criado: 2026-09-30
tags: [ambiente, agentes, design, interface]
---
# ADR-0015 Papel Designer

## Contexto

Ate a T-0002, a aparencia das telas foi decidida pelo Dev enquanto implementava. O humano quer uma IA especializada que (a) pense a experiencia visual com liberdade, sem ficar presa ao codigo, e (b) de observacoes ao Dev sobre a parte web, de forma parecida com o Revisor. Pediu o fluxo: prompt -> imagem -> SVG (esqueleto) -> HTML.

## Decisao

- Novo papel **`designer`** (Opus), com dois modos escolhidos pelo lancador a partir do cartao:
  - **criacao** (`papel: designer`): brief -> 2 ou 3 conceitos visuais -> humano escolhe (`aguardando-humano`) -> esqueleto SVG -> prototipo HTML/CSS -> entrega ao Dev com tokens;
  - **revisao visual** (cartao em `revisao` com `interface: sim`): compara a aplicacao rodando com o prototipo e registra `UX-####` (bloqueante, recomendado, sugestao); nao muda o status, o Revisor decide.
- Escreve **somente** em `docs/design/`, `qualidade/ux/`, cartoes e Inbox (hook de lista de permissoes + hook do Git). Nunca altera o codigo da aplicacao.
- Conceitos visuais (SVG/PNG) sao inspiracao; a fonte de verdade da interface e o prototipo HTML + os tokens do sistema de design (`docs/design/sistema/`).
- Porta 8200 + N e projeto Compose `t000N-des` para a revisao visual.

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| Designer gera direto o HTML | Menos etapas | Solucao presa ao codigo; sem exploracao visual |
| Designer edita os templates reais | Resultado imediato | Mistura papeis; sem revisao independente do codigo |
| Revisao visual feita pelo Revisor | Menos papeis | Revisor foca em funcionamento; olhar visual fica raso |

## Consequencias

- **Positivas:** exploracao visual antes do codigo; escolha consciente do humano entre direcoes; sistema de design cresce a cada tarefa; observacoes visuais rastreaveis.
- **Negativas / riscos:** mais uma etapa por tela; sem gerador de imagem, o conceito e SVG; sem ferramenta de captura de tela, a revisao visual depende de ler HTML/CSS ou de capturas enviadas pelo humano. Ambas ficam para skills futuras.
