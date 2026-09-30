---
tipo: candidato
status: inbox
tipo_proposto: aprendizado
origem: agente/engenheiro
tarefa: T-0006
pesquisa:
confianca: alta
fontes: ["projetos/lab: docs/retrospectivas/T-0006 retrospectiva T-0003 a T-0005.md", "Brain git: 41a6ef2, 3a77a48, ab6db60", "projetos/lab: VER-0009"]
verificado_em: 2026-09-30
valido_para: "Fluxo de tarefa v3, lancador papel"
criado: 2026-09-30
decisao:
tags: [retrospectiva, fluxo, lancador, triagem, proposta-n4]
---
# Regra de fluxo sem portao no lancador nao e seguida

## Conteudo proposto

Nas T-0003 a T-0005, duas regras escritas do fluxo foram puladas, e as duas custaram uma rodada extra:

1. **Engenheiro antes de entrada de usuario.** A regra entrou no Fluxo de tarefa as 07:56 de 2026-09-30; a T-0003 (upload) foi para `pronta` as 09:56 sem cartao do Engenheiro. Resultado: BUG-0006 (limite de upload ambiguo) e SEC-0001 (RNF-05 nao verificavel).
2. **Seguranca antes do Revisor.** Na T-0005 (`seguranca: sim`), o Revisor rodou primeiro e registrou o VER-0009 como `parcial`.

Em ambos os casos, o lancador `papel` conferia pasta, papel e status, mas nao os pre-requisitos. **Proposta ao humano (area N4):**

- **M1 - Portao do Revisor:** `papel revisor` recusa (ou avisa) quando o cartao tem `seguranca: sim` e a secao "Revisao de seguranca" esta vazia, ou `interface: sim` e a "Revisao visual" esta vazia.
- **M2 - Triagem registrada:** campo `triagem: AAAA-MM-DD` no template de Tarefa, preenchido pelo Coordenador; `papel dev` recusa cartao `normal`/`grande` sem triagem. Quando uma regra de fluxo muda, os cartoes em `backlog`/`pronta` voltam para triagem (a T-0003 era de antes das marcas `interface:`/`seguranca:` e nunca foi retriada).
- **M7 - Comandos com fonte unica:** o `CLAUDE.md` do projeto aponta para o README na secao "Como rodar", em vez de repetir os comandos. Cada comando novo das T-0004 e T-0005 virou escalacao N4 (Coordenador -> Administrador) so para editar o `CLAUDE.md`.

## Evidencia

Historico do Git do Brain (`41a6ef2` regra; `3a77a48` T-0003 pronta; `ab6db60` papeis Coordenador e Seguranca), VER-0006/VER-0007 (T-0003, 2 rodadas) e VER-0009/VER-0010 (T-0005, 2 VER). Analise completa na retrospectiva da T-0006 no projeto lab.

## Links confiaveis

- Retrospectiva no projeto: `projetos/lab/docs/retrospectivas/T-0006 retrospectiva T-0003 a T-0005.md` (causa raiz de cada BUG/SEC).

## Por que e reaproveitavel

Toda regra nova de fluxo: sem conferencia no ponto de transicao (lancador ou triagem), ela depende de memoria.

## Relacionadas no Brain

- [[T-0002 mostrou que regra de entrada ambigua vira bug e que o Revisor precisa testar extremos]]
- [[ADR-0013 Lancador de papeis e identidade dos agentes]]
- [[ADR-0016 Papeis Coordenador e Seguranca]]

## Decisao do Bibliotecario
