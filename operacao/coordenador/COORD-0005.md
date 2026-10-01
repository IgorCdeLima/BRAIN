---
tipo: pedido-coordenador
id: COORD-0005
status: escalado
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: ambiente
criado: 2026-09-30
atendido_em: 2026-09-30
adm: ADM-0012
tags: [ambiente, regras, pedidos, cadeia-de-comando]
---
# COORD-0005 - Regra: agente que precisaria do humano sempre faz uma requisicao ao Coordenador

<!-- Pedido do humano em 2026-09-30, registrado pelo Revisor. Muda regra de agentes (area N4): o Coordenador provavelmente precisa escalar ao Administrador (ADM-####). -->

## Pedido

- [x] Atualizar as regras dos agentes com o texto do humano: -> ADM-0012

  > "quando um agente precisaria da atuacao do humano, ele sempre faca uma requisicao para o coordenador. e ele sabera o que fazer"

  Onde aplicar: decisao do Coordenador/Administrador. Sugestao: secao "Pedidos de comando" do `CLAUDE.md` global e as definicoes dos papeis (`agentes/`, `BRAIN/60_Agentes`), para valer para todos.
  - Pontos a definir na avaliacao:
    - Abrangencia: hoje a regra cobre "comando que o papel nao pode rodar"; o pedido amplia para **qualquer** atuacao do humano (merge, decisao, aprovacao, acao fora do perfil).
    - Formato: o humano pediu, neste caso, um `COORD-####` mesmo para pedido ligado a tarefa (merge da T-0007, ver COORD-0004). O `_LEIAME.md` desta pasta e o ADR-0020 dizem que pedido de tarefa vai no cartao. Definir se a regra passa a ser sempre `COORD-####`, ou cartao + `COORD`, e ajustar o `_LEIAME.md` e a secao "Passos do humano" do template de tarefa.
    - O que o agente diz ao humano: em vez de pedir a acao, informar o numero da requisicao criada.

## Motivo

Caso concreto (T-0007, 2026-09-30): o humano pediu ao Revisor o merge da tarefa. O Revisor nao tem permissao e respondeu com o comando para o humano ou o Coordenador rodar, registrando o pedido no cartao. O humano quer que o caminho padrao seja sempre a requisicao ao Coordenador, que sabe como encaminhar (executar, escalar ao Administrador ou levar ao humano).

O Revisor nao pode alterar regras (`CLAUDE.md`, `agentes/`, `BRAIN/60_Agentes`, `BRAIN/70_Workflows` sao area N4).

Relacionado: COORD-0003 (erro inesperado vira pedido de avaliacao ao Coordenador), mesma linha de mudanca.

---

## Atendimento

Coordenador, 2026-09-30: aprovado pelo humano escalar. Como muda regras (area N4), juntado ao COORD-0003/COORD-0005 num so pedido: ADM-0012. Proximo passo: humano roda `papel administrador`.
