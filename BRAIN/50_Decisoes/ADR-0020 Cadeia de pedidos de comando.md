---
tipo: decisao
status: aceita
decidido_em: 2026-09-30
decidido_por: Igor
substituida_por:
criado: 2026-09-30
tags: [ambiente, agentes, coordenacao, administracao, operacao]
---
# ADR-0020 Cadeia de pedidos de comando

## Contexto

- Os agentes pediam ao humano, na secao "Passos do humano" do cartao, que rodasse comandos (apagar volume, subir container, push). O humano virava executor de comandos.
- A mesma secao misturava comandos com decisoes (direcao visual, aceitar ADR, criterios propostos pela Seguranca), que so o humano pode tomar.
- O Coordenador ja roda varios comandos com a aprovacao do humano; o Administrador ([[ADR-0018 Papel Administrador com senha e aprovacao a cada mudanca]]) roda o resto, tambem com aprovacao. Os pedidos ao Administrador ficam em `operacao/administrador` ([[ADR-0019 Pedidos ao Administrador em operacao]]).
- Papeis sem cartao (Pesquisador, Bibliotecario) nao tinham onde pedir.

## Decisao

1. **Cadeia:** agente precisa de comando -> **Coordenador** executa (com o clique de aprovacao do humano) -> sem permissao, abre `ADM-####` -> **Administrador** executa (com aprovacao) -> se so o humano pode (Orca, lancador `papel`, senha, `sudo`, acao fora do computador), o Administrador informa o humano com o comando exato.
2. **Cartao:** secao nova **"Pedidos ao Coordenador"** para comandos (comando exato, pasta, motivo). O Coordenador marca `[x]` ao executar ou `-> ADM-####` ao escalar. A secao **"Passos do humano"** fica so com decisoes e acoes que so o humano pode fazer.
3. **Caixa do Coordenador:** `operacao/coordenador/COORD-####.md` para pedidos sem tarefa. Qualquer papel cria; o Coordenador le no panorama. Pedido ligado a tarefa continua no cartao.
4. O humano continua aprovando cada comando que altera algo (regra de ouro do ambiente); so deixa de digita-los.

## Alternativas consideradas

| Alternativa | Por que nao |
|---|---|
| Manter "Passos do humano" para tudo | O humano continua executando comandos que um papel poderia rodar |
| Renomear "Passos do humano" para "Pedidos ao Coordenador" | Decisoes do humano passariam por um intermediario sem necessidade |
| Sem caixa do Coordenador | Pesquisador e Bibliotecario continuariam pedindo direto ao humano |
| Novo tipo "AGENTE-####" para chamar papeis | O cartao de tarefa ja faz isso (campo `papel:` + lancador) |
| Dar ao Coordenador permissao para tudo | Perde a separacao N2/N4; o Administrador existe para isso |

## Consequencias

- O humano so digita comandos em Orca, lancador, senha e `sudo`; o resto e aprovar.
- Mais uma pasta liberada no hook de escrita dos papeis e nos perfis.
- Cartoes antigos (T-0002 a T-0006) continuam com "Passos do humano" misturado; os novos usam as duas secoes.
- Tudo fica rastreado no Git: cartao, COORD e ADM formam o historico de quem pediu, quem executou e quem aprovou.
- 2026-10-01: itens 2 e 3 emendados pelo [[ADR-0021 Pedidos ao Coordenador sempre em COORD e numeracao de qualidade por tarefa]]: todo pedido vira `COORD-####`, inclusive com tarefa; o cartao guarda so a referencia.
