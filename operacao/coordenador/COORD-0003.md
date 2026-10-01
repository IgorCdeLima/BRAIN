---
tipo: pedido-coordenador
id: COORD-0003
status: concluido
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: ambiente
criado: 2026-09-30
atendido_em: 2026-09-30
adm: ADM-0012
tags: [ambiente, regras, erros, melhoria-continua]
---
# COORD-0003 - Regra: erro inesperado de um agente vira pedido de avaliacao ao Coordenador

<!-- Pedido do humano em 2026-09-30, registrado pela Seguranca. Muda regra de agentes (area N4): o Coordenador provavelmente precisa escalar ao Administrador (ADM-####). -->

## Pedido

- [x] Adicionar como correcao as regras dos agentes, com o texto do humano: -> ADM-0012

  > "quando ocorre um erro, como a falta de um arquivo, voce deve realizar um pedido para o coordenador realizar uma avaliacao e melhorar essa possivel resposta"

  Onde aplicar: decisao do Coordenador/Administrador. Sugestao: secao "Pedidos de comando" do `CLAUDE.md` global, ou `BRAIN/70_Workflows/Fluxo de tarefa.md`, para valer para todos os papeis.
  - Pontos a definir na avaliacao: o que conta como "erro" (ferramenta falhou, arquivo ausente ou movido, permissao negada, comando que nao existe), se o pedido vai no cartao ou num `COORD-####`, e o que se espera do Coordenador (investigar a causa, corrigir o fluxo ou a regra, registrar a resposta melhorada).

## Motivo

Caso concreto (T-0007, 2026-09-30): a Seguranca tentou editar um candidato no `BRAIN/00_Inbox`, mas o Bibliotecario ja o tinha promovido para `10_Conhecimento` e limpado o Inbox. A edicao falhou com "File does not exist". Hoje nenhuma regra diz o que fazer nesse caso: o agente so relata o erro na resposta, e o aprendizado se perde. Com a regra, o Coordenador avalia cada erro e melhora a resposta do ambiente, seja ajustando o fluxo, avisando o papel afetado ou criando conhecimento.

A Seguranca nao pode alterar regras (`CLAUDE.md`, `agentes/`, `BRAIN/60_Agentes`, `BRAIN/70_Workflows` sao area N4).

---

## Atendimento

Coordenador, 2026-09-30: aprovado pelo humano escalar. Como muda regras (area N4), juntado ao COORD-0003/COORD-0005 num so pedido: ADM-0012. Proximo passo: humano roda `papel administrador`.

Coordenador, 2026-10-01: ADM-0012 concluido (merge `b2458c8`; regra de erro inesperado no `CLAUDE.md` global e no Fluxo de tarefa). Pedido concluido, com aprovacao do humano.
