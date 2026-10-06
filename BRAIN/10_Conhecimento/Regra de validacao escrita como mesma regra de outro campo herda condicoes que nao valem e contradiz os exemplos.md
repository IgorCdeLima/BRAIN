---
tipo: aprendizado
status: ativo
origem: T-0018 (Revisor; BUG-T0018-03, VER-T0018-02), curado pelo Bibliotecario
tarefa: T-0018
confianca: media
criado: 2026-10-05
decisao: promovido
tags: [requisitos, validacao, entrada, revisao, armadilha]
---
# Regra de validacao escrita como mesma regra de outro campo herda condicoes que nao valem e contradiz os exemplos

## O que aconteceu

Na T-0018 (projeto `ambiente`), a tabela de regras de entrada dizia, para varios campos de pasta, "mesma regra do `IA_RAIZ`". A regra do `IA_RAIZ` exigia que o caminho existisse **e contivesse `ferramentas/tarefa.py`**. Lida ao pe da letra, essa condicao tornava invalidos os exemplos validos dos outros campos. Na leitura pretendida ("so o formato"), a regra deixava passar `/home/<usuario>` e `/`. Quem implementa o validador teria de adivinhar. O `VER-T0018-01` passou porque conferiu os exemplos entre si, nao contra a regra; o defeito saiu no `VER-T0018-02` (`BUG-T0018-03`).

## O que aprendemos

O atalho "mesma regra do campo X" copia **tudo** o que a regra de X diz, inclusive as condicoes proprias de X. O resultado e uma regra que, lida literalmente, contradiz os proprios exemplos.

## O que muda a partir de agora

- **Engenheiro:** separar uma regra comum com nome proprio (ex.: "regra de caminho": absoluto, `realpath`, existe, sem caractere de controle) das condicoes de cada campo; cada linha cita a regra comum e acrescenta so o que e dela.
- **Revisor:** conferir cada exemplo valido e invalido contra a regra **lida ao pe da letra**, nao so os exemplos entre si. Exemplo valido que a regra literal recusa e defeito.

Esta nota nao altera regras nem workflows; se o humano quiser o item na matriz de verificacao, a proposta passa pelo N4.

## Origem

`BUG-T0018-03` e `VER-T0018-02` do projeto `ambiente`. Relacionado ao `SEC-T0018-03` (pastas sensiveis aceitas). Aprendizado de processo interno, sem fonte externa.

## Relacionadas

- [[CWE-20 entrada extrema gerando erro 500 se evita validando com Pydantic e handler global]]: mesma familia (validar a entrada antes de usar).
- [[Decisao do humano registrada depois da entrega exige varrer o texto antigo que ela contradiz]]: outra contradicao interna de requisitos da mesma tarefa.
- [[T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos]]: mesmo padrao, regra de entrada ambigua vira bug.

## Decisao do Bibliotecario

Promovido (2026-10-05) para `10_Conhecimento` como aprendizado. Sem duplicata: a nota da T-0002 trata de ambiguidade em outra regra e foi ligada. Confianca media: um caso, com BUG e VER como evidencia.
