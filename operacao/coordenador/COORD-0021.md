---
tipo: pedido-coordenador
id: COORD-0021
status: aberto
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: ambiente
criado: 2026-10-02
atendido_em:
adm: ADM-0011, ADM-0017
tags: [ambiente, hooks, telemetria, tokens, brain, verificacao]
---
# COORD-0021 - Verificar em sessao real as medicoes de uso do Brain e de tokens

## Pedido

Os hooks e scripts do [[ADM-0017]] (uso do Brain) e do [[ADM-0011]] (tokens) entraram na `main` em 2026-10-02, testados so com eventos simulados. Conferir no uso real e orientar o humano se algo falhar. Todos os comandos rodam na copia principal (`$IA_RAIZ`), sao somente leitura e estao liberados no perfil do Coordenador (`consumo.py`) ou do Bibliotecario (`uso_brain.py`).

- [ ] 1. **Hooks gravando** (depois da primeira sessao de qualquer papel aberta pelo lancador apos o merge, ex.: o Dev da T-0015):
  - `py -3 ferramentas/consumo.py --desde <data do merge>` -> a linha de cabecalho deve mostrar "N pelo log" com N > 0.
  - Pedir ao Bibliotecario, na proxima curadoria: `py -3 ferramentas/uso_brain.py --desde <data do merge>` -> "N pelo log permanente" com N > 0.
  - Se N = 0 depois de uma sessao de papel: os hooks no frontmatter da definicao do papel (`PostToolUse` e `Stop`) nao estao rodando. Abrir `ADM-####` com a saida; alternativa ja prevista: ligar os hooks no `.claude/settings.json` (copia principal e projetos).
- [ ] 2. **Tempo do hook `Stop`**: perguntar ao humano se notou demora ao fim de cada resposta numa sessao longa (o hook rele a transcricao inteira; timeout de 20 s). Se notou: `ADM-####` pedindo leitura incremental.
- [ ] 3. **Primeiro fechamento com "Consumo"** (proxima tarefa que for para `concluida`, ex.: T-0015): rodar `py -3 ferramentas/consumo.py --tarefa T-####`, colar na secao **Consumo** do cartao e conferir se os papeis e as rodadas batem com o que aconteceu na tarefa. Divergencia: `ADM-####` com o exemplo.
- [ ] 4. **"Brain consultado"**: no mesmo fechamento, conferir se a Entrega e o VER trouxeram a linha `[[Nota]] - ajudou: sim | parcial | nao`. Se os papeis nao estiverem preenchendo, avisar o humano (pode precisar de lembrete na definicao do papel, via `ADM-####`).
- [ ] 5. Quando 1 e 3 estiverem ok: avisar o Administrador (ou registrar aqui) para fechar o ADM-0011 e o ADM-0017 (`concluido`).

## Motivo

Itens marcados como "Nao verificado" no ADM-0011 e no ADM-0017: os hooks so rodam em sessoes abertas pelo lancador, e o Administrador nao le `logs/` nem define `IA_PAPEL` para testar. A verificacao do hook de escrita (ADM-0015) segue no [[COORD-0020]], na revisao da T-0015.

---

## Atendimento

Coordenador, 2026-10-03, no fechamento da T-0015. O pedido continua `aberto`.
- **Item 1, parte de tokens: ok.** `consumo.py --tarefa T-0015` mostrou "7 sessoes (7 pelo log, 0 pelas transcricoes)", entao os hooks gravam em sessao real. A parte de `uso_brain.py` fica para o Bibliotecario, na proxima curadoria.
- **Item 2: pendente.** Falta perguntar ao humano se notou demora no fim das respostas.
- **Item 3: ok.** Consumo colado no cartao da T-0015. Os papeis e as rodadas batem: Dev 3, Seguranca 2, Revisor 2.
- **Item 4: ok.** As duas Entregas do Dev e as duas rodadas da Seguranca trazem `[[Nota]] - ajudou: ...`. O VER-T0015-02 registra "nenhuma nota consultada diretamente", com o motivo. Nao e preciso lembrete na definicao dos papeis.
- **Item 5:** aguarda o resultado do `uso_brain.py` do item 1.
