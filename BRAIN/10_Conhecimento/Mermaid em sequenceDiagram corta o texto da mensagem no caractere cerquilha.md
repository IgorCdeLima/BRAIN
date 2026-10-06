---
tipo: problema-solucao
status: ativo
origem: T-0018 (VER-T0018-01, BUG-T0018-01), proposto pelo Revisor e curado pelo Bibliotecario
tarefa: T-0018
confianca: alta
fontes: ["mermaid-cli 11.17.0, teste local de 2026-10-05"]
verificado_em: 2026-10-05
valido_para: "mermaid-cli 11.17.0"
criado: 2026-10-05
decisao: promovido
revisar_em: 2027-04-05
tags: [mermaid, diagrama, documentacao, revisao]
---
# Mermaid em sequenceDiagram corta o texto da mensagem no caractere cerquilha

## Sintoma

Num `sequenceDiagram`, a mensagem `H->>T: tarefa abrir T-#### dev` aparece renderizada como `tarefa abrir T-`: tudo depois do primeiro `#` some, **sem erro de sintaxe**. Em `flowchart`, o mesmo texto entre aspas (`n["sessao T-####"]`) aparece inteiro.

Revisar a sintaxe "a mao" nao pega: o diagrama renderiza, so que com o texto errado.

## Ambiente

mermaid-cli 11.17.0 (`@mermaid-js/mermaid-cli@11`), Linux, usuario comum.

## Causa raiz

Causa provavel (nao confirmada na documentacao): no `sequenceDiagram` o `#` inicia a sintaxe de entidade (`#35;`) e o texto apos ele e descartado. Observado: o `flowchart` com rotulo entre aspas nao tem esse comportamento.

## Solucao

Nas mensagens de sequencia, nao usar `#` literal: escrever `T-NNNN` ou a entidade `#35;`.

## Como verificar que foi resolvido

Renderizar os diagramas e procurar texto cortado nos SVG:

```bash
awk '/^```mermaid/{n++;p=1;fn="d"n".mmd";next} /^```/{p=0} p{print > fn}' arquivo.md
echo '{"args":["--no-sandbox","--disable-setuid-sandbox"]}' > p.json
for f in d*.mmd; do npx -y @mermaid-js/mermaid-cli@11 -p p.json -i $f -o ${f%.mmd}.svg; done
grep -o '>[^<]*<' d*.svg | less
```

## O que nao funcionou

- Conferir so a sintaxe do diagrama (nao acusa o corte).
- Rodar o mermaid-cli sem `--no-sandbox`: o Chromium do puppeteer nao abriu (Linux, usuario comum).

## Origem

T-0018 (projeto `ambiente`): `VER-T0018-01` e `BUG-T0018-01`. Teste de 2026-10-05: 6 mensagens de uma sequencia cortadas em `T-`; 3 rotulos de flowchart com `T-####` entre aspas inteiros.

## Relacionadas

- [[Decisao do humano registrada depois da entrega exige varrer o texto antigo que ela contradiz]]: aprendizado da mesma tarefa que manda renderizar de novo os diagramas tocados.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento`, reescrito no template problema-solucao (o candidato usava um tipo `armadilha` inexistente). Sem duplicata.
