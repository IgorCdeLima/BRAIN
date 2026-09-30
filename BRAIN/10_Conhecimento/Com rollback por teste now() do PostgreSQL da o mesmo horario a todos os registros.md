---
tipo: problema-solucao
status: ativo
origem: agente/revisor (candidato da tarefa T-0002, curado pelo Bibliotecário)
confianca: media
fontes: ["https://www.postgresql.org/docs/current/functions-datetime.html#FUNCTIONS-DATETIME-CURRENT", "projetos/lab: qualidade/verificacoes/VER-0003.md"]
verificado_em: 2026-09-29
valido_para: PostgreSQL (todas as versões atuais) + testes com transação externa e rollback
criado: 2026-09-29
tags: [postgresql, testes, pytest, armadilha]
decisao: promovido
---
# Com rollback por teste, o `now()` do PostgreSQL dá o mesmo horário a todos os registros

## Sintoma

Um teste de "ordem do mais recente para o mais antigo" passa, mas exercita só o desempate (ex.: `id desc`), não a ordenação por data.

## Ambiente

PostgreSQL com coluna `criado_em` de `server_default=func.now()`; testes numa única transação externa com rollback ([[Testes com banco separado e rollback por teste funcionam no FastAPI com SQLAlchemy]]).

## Causa raiz

`now()` e `CURRENT_TIMESTAMP` devolvem o início da **transação**, não do comando. A documentação oficial (relida em 2026-09-29) diz: "these functions return the start time of the current transaction, their values do not change during the transaction". Já `clock_timestamp()` "returns the actual current time". Numa transação de teste, todos os registros recebem o mesmo `criado_em`. Se o desempate mudar ou sair, o teste não percebe.

## Solução

- Dar `criado_em` explícito e diferente aos registros do teste; ou
- usar `clock_timestamp()` se o modelo aceitar essa semântica.

## Como verificar que foi resolvido

Os registros do teste têm `criado_em` distintos, e o teste falha se a ordenação por data for removida (deixando só o desempate).

## O que não funcionou

Confiar no `server_default` dentro da transação do teste. Na aplicação real (uma transação por requisição) os horários saíram diferentes, o que esconde o problema.

## Origem

T-0002 do `lab`, `test_listagem_do_mais_recente_para_o_mais_antigo`, apontado pelo Revisor no VER-0003. A **igualdade dentro do teste não foi medida**: vem da documentação e do código. Por isso `confianca: media`.

## Decisão do Bibliotecário

**Promovido** em 2026-09-29. Documentação oficial confirmada por leitura. Sem duplicata. Confiança média até haver reprodução medida.
