---
tipo: aprendizado
status: ativo
origem: T-0018 (Engenheiro; BUG-T0018-02 do Revisor), curado pelo Bibliotecario
tarefa: T-0018
confianca: media
criado: 2026-10-05
decisao: promovido
tags: [modelagem, requisitos, consistencia, revisao]
---
# Decisao do humano registrada depois da entrega exige varrer o texto antigo que ela contradiz

## O que aconteceu

Na T-0018 (projeto `ambiente`) as respostas Q1, Q4, Q5 e Q10 do humano chegaram em 5 commits depois do `407f095`. O Engenheiro acrescentou os requisitos novos e a secao "Decisoes do humano", mas o texto anterior, que pressupunha a outra resposta, continuou la. O Revisor achou 5 trechos desatualizados (BUG-T0018-02): um link, a tabela "Usuarios" (ainda dizia "ver questao Q1"), o RNF-07, a "Recomendacao" da avaliacao de instalacao e o diagrama de contexto. Corrigido no `8772aa6`.

## O que aprendemos

Acrescentar nao basta. Quando o humano responde questoes em aberto depois da primeira entrega, o que contradiz a decisao costuma ficar em:

- tabelas de resumo;
- requisitos nao funcionais genericos (ex.: RNF de rede citando a regra antiga);
- a "Recomendacao" de uma avaliacao de tecnologia, quando a decisao vai em outra direcao (marcar como "superada" e apontar para a decisao, sem apagar o historico);
- diagramas de contexto (setas e rotulos).

## O que muda a partir de agora

Roteiro curto ao registrar cada resposta do humano:

1. `grep` pelo id da questao (ex.: `Q4`) e pelas palavras-chave do tema em todo `docs/` do projeto;
2. para cada trecho achado: ajustar, marcar como superado ou justificar por que continua valendo;
3. renderizar de novo os diagramas tocados.

O Revisor pode usar o mesmo roteiro como item de conferencia ("decisoes novas versus texto antigo"). Esta nota nao altera regras nem workflows; se o humano quiser o item na matriz de verificacao, a proposta passa pelo N4.

## Origem

T-0018, `BUG-T0018-02`, commits `407f095` e `8772aa6` do projeto `ambiente`. Aprendizado de processo interno, sem fonte externa.

## Relacionadas

- [[Mermaid em sequenceDiagram corta o texto da mensagem no caractere cerquilha]]: ao renderizar de novo os diagramas, conferir tambem o texto cortado.
- [[Padroes de modelagem]]: padroes que o Engenheiro segue ao modelar.
- [[Regra de validacao escrita como mesma regra de outro campo herda condicoes que nao valem e contradiz os exemplos]]: outra contradicao interna de requisitos achada na mesma tarefa.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como aprendizado. Sem duplicata (a nota mais proxima, a de lacuna declarada pelo Dev, trata de outro caso). Confianca media: um unico caso, mas com evidencia (commits e BUG).
