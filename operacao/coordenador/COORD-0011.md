---
tipo: pedido-coordenador
id: COORD-0011
status: concluido
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0012
criado: 2026-10-01
atendido_em: 2026-10-01
adm:
tags: [lab, seguranca, t-0010, t-0012, endurecimento]
---
# COORD-0011 - Copiar os criterios de seguranca para a T-0010 e criar o cartao de endurecimento do servico app

## Pedido

- [x] Copiar os criterios **CS-01 a CS-11** do cartao `operacao/tarefas/T-0012.md` (Entrega, secao "Criterios de aceite de seguranca propostos para a T-0010") para a secao "Criterios de aceite" de `operacao/tarefas/T-0010.md`. Aprovados pelo humano em 2026-10-01, com as decisoes D1 a D4 na opcao recomendada (ja refletidas no texto dos CS-04, CS-06 e CS-08). Sugestao: citar no Contexto da T-0010 o documento `docs/seguranca/T-0012-ameacas.md` (lab) e as armadilhas medidas: `DecompressionBombError` nao e `OSError`; o `save` padrao mantem o COM do JPEG e o ICC do PNG; JPEG com MPF abre como `MPO`.
- [x] Atencao ao copiar: o CS-08 (D4) traz texto novo de interface ("Servidor ocupado, tente de novo.", 503 na pagina com campos preservados). A triagem decide se a T-0010 continua `interface: nao`.
- [x] Criar um cartao unico (`papel: dev`, `seguranca: sim`, projeto lab) de endurecimento do servico `app` no `docker-compose.yml`, juntando **SEC-T0012-01** (limites de memoria, CPU e pids) e **SEC-T0008-01** (`no-new-privileges`, `cap_drop: [ALL]`). Aprovado pelo humano em 2026-10-01. Recomendacoes e testes estao nos dois SEC (`qualidade/seguranca/` do lab). O teto de memoria deve sair do teste manual do CS-08 da T-0010, entao o cartao fica melhor **depois** da T-0010.

## Motivo

Os criterios vao na Entrega da T-0012 porque a Seguranca nao altera o cartao da T-0010 (restricao do cartao), e criar cartao de tarefa e atribuicao do Coordenador.

---

## Atendimento

Coordenador, 2026-10-01 (com o "sim" do humano), depois do merge da T-0012 (`f1b9e31`, lab) e da liberacao do COORD-0013:

- CS-01 a CS-11 copiados para "Criterios de aceite" da T-0010 (texto final, com CS-02 e CS-06 corrigidos e reaprovados). Contexto da T-0010 recebeu o documento de ameacas, as decisoes D1 a D4 e as armadilhas medidas. No CS-08 acrescentei so "registrar o pico: ele define o teto de memoria da T-0015".
- `interface:` da T-0010 ficou como esta (`nao`) e virou item em "Passos do humano" para a triagem.
- Cartao **T-0015** criado em `backlog` (`papel: dev`, `seguranca: sim`): endurecimento do servico `app` (SEC-T0012-01 + SEC-T0008-01), so fica `pronta` depois da T-0010 com o pico do CS-08 registrado.
