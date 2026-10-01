---
tipo: pedido-coordenador
id: COORD-0013
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: T-0012
criado: 2026-10-01
atendido_em: 2026-10-01
adm:
tags: [lab, seguranca, t-0010, t-0012]
---
# COORD-0013 - Segurar a copia do CS-02 e do CS-06 (COORD-0011) ate a correcao da T-0012

## Pedido

- [x] Ao atender o COORD-0011, **nao** copiar o CS-02 e o CS-06 na redacao atual para a T-0010. A T-0012 foi para `correcao` (VER-T0012-01): o caso de teste do CS-06 nao detecta ICC com anexo no PNG (BUG-T0012-01) e a receita do caso explicito do CS-02 nao gera `SyntaxError` (BUG-T0012-02). Copiar os dois so depois que a Seguranca corrigir, o humano reaprovar o texto novo e um novo VER aprovar a T-0012. Os demais CS (01, 03, 04, 05, 07 a 11) e o cartao de endurecimento nao foram afetados; copia-los antes ou junto fica a criterio do Coordenador.
  - Pasta: `operacao/tarefas` (cartoes T-0010 e T-0012).

## Motivo

Os criterios ja aprovados pelo humano entrariam na T-0010 com dois testes que nao provam o que dizem; o Revisor nao escreve no cartao da T-0010.

---

## Atendimento

Coordenador, 2026-10-01: condicoes cumpridas antes da copia. A Seguranca corrigiu no `cb60751`, o humano reaprovou o texto novo do CS-02 e do CS-06, e o VER-T0012-02 aprovou a T-0012 (BUG-T0012-01 e -02 `verificado`). Copia liberada e feita com o texto corrigido junto do COORD-0011.
