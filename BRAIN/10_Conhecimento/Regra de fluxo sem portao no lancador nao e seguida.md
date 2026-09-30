---
tipo: aprendizado
status: ativo
origem: T-0006 (Engenheiro, retrospectiva T-0003 a T-0005), curado pelo Bibliotecario
tarefa: T-0006
confianca: alta
fontes: ["projetos/lab: docs/retrospectivas/T-0006 retrospectiva T-0003 a T-0005.md", "Brain git: 41a6ef2, 3a77a48, ab6db60", "projetos/lab: VER-0009"]
verificado_em: 2026-09-30
valido_para: "Fluxo de tarefa v3, lancador papel"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [retrospectiva, fluxo, lancador, triagem, proposta-n4]
---
# Regra de fluxo sem portao no lancador nao e seguida

## O que aconteceu

Nas T-0003 a T-0005, duas regras escritas do fluxo foram puladas, e cada uma custou uma rodada extra:

1. **Engenheiro antes de entrada de usuario.** A regra entrou no Fluxo de tarefa as 07:56 de 2026-09-30 (`41a6ef2`); a T-0003 (upload) foi para `pronta` as 09:56 (`3a77a48`) sem cartao do Engenheiro. Resultado: BUG-0006 (limite de upload ambiguo) e SEC-0001 (RNF-05 nao verificavel).
2. **Seguranca antes do Revisor.** Na T-0005 (`seguranca: sim`), o Revisor rodou primeiro e registrou o VER-0009 como `parcial`.

O lancador `papel` conferia pasta, papel e status, mas nao os pre-requisitos.

## O que aprendemos

Regra de fluxo sem conferencia no ponto de transicao (lancador ou triagem) depende de memoria e nao e seguida.

## O que muda a partir de agora

**Propostas ao humano (area N4; pendentes):**

- **M1 - Portao do Revisor:** `papel revisor` recusa (ou avisa) quando o cartao tem `seguranca: sim` e a secao "Revisao de seguranca" esta vazia, ou `interface: sim` e a "Revisao visual" esta vazia.
- **M2 - Triagem registrada:** campo `triagem: AAAA-MM-DD` no template de Tarefa, preenchido pelo Coordenador; `papel dev` recusa cartao `normal`/`grande` sem triagem. Quando uma regra de fluxo muda, os cartoes em `backlog`/`pronta` voltam para triagem (a T-0003 era de antes das marcas `interface:`/`seguranca:` e nunca foi retriada).
- **M7 - Comandos com fonte unica:** o `CLAUDE.md` do projeto aponta para o README na secao "Como rodar", em vez de repetir os comandos. Cada comando novo das T-0004 e T-0005 virou escalacao N4 (Coordenador -> Administrador) so para editar o `CLAUDE.md`.

## Origem

Historico do Git do Brain (`41a6ef2` regra; `3a77a48` T-0003 pronta; `ab6db60` papeis Coordenador e Seguranca), VER-0006/VER-0007 (T-0003) e VER-0009/VER-0010 (T-0005). Analise completa na retrospectiva da T-0006 no projeto lab.

## Relacionadas no Brain

- [[T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos]]: retrospectiva anterior, mesmo padrao de regra nao seguida.
- [[ADR-0013 Lancador de papeis e identidade dos agentes]]: o lancador onde os portoes entrariam.
- [[ADR-0016 Papeis Coordenador e Seguranca]]: papeis cujo pre-requisito foi pulado.
- [[Lacuna declarada pelo Dev em criterio de aceite precisa de destino antes da revisao]]: outra falha de fluxo da mesma retrospectiva.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento` (2026-09-30): confianca alta, evidencia em commits e VER; as mudancas de lancador e fluxo sao proposta ao humano (N4), sem edicao minha.
