---
tipo: pedido-coordenador
id: COORD-0026
status: concluido
urgencia: nao-bloqueante
pedido_por: bibliotecario
tarefa: ambiente
criado: 2026-10-03
atendido_em: 2026-10-04
adm: ADM-0024
tags: [brain, links-quebrados, notas-py, area-n4]
---
# COORD-0026 - Corrigir 16 links quebrados em notas de area N4 (escalar ao Administrador)

## Pedido

Pedido do humano ao Bibliotecario na curadoria de 2026-10-03: "para os links quebrados, crie uma ADM". O Bibliotecario nao cria ADM (cadeia: agente -> Coordenador -> Administrador), entao escala por aqui. **Coordenador: abrir o `ADM-####` correspondente.**

`py -3 ferramentas/notas.py quebrados` (copia principal) lista 16 links:

- [ ] -> ADM-0024 **15 links `[[ADM-00NN]]`** em notas do cofre, todos de area N4 (somente o humano/Administrador edita):
  - `BRAIN/50_Decisoes/ADR-0022` (l.16, 43, 44), `ADR-0023` (l.14, 43, 48), `ADR-0024` (l.14, 44), `ADR-0025` (l.15, 18);
  - `BRAIN/60_Agentes/Coordenador.md` (l.26), `Revisor.md` (l.22), `Seguranca.md` (l.22);
  - `BRAIN/70_Workflows/Rastreabilidade.md` (l.53).
  - Ids: ADM-0009, 0011, 0015, 0016, 0017, 0018.
- [ ] -> ADM-0024 **1 link `[[crie um link]]`** em `BRAIN/Bem-vindo.md` (l.3): nota padrao do Obsidian; texto de exemplo, nao e link real. Sugestao: o humano apaga a nota (o proprio texto pede) ou o Administrador troca por texto simples.

## Motivo

Os ADM ficam em `operacao/administrador/ADM-####.md`, **fora do cofre** (`BRAIN/`). `[[ADM-0011]]` nao resolve no Obsidian nem no `notas.py` (que so enxerga o cofre), por isso aparece como quebrado. Nao e erro de digitacao: o arquivo existe. Os links em `operacao/` (ex.: COORD-0021 -> `[[ADM-0017]]`) tem o mesmo problema, mas `quebrados` nao os varre.

Opcoes para o Administrador decidir:

1. **Trocar por texto/codigo** (`ADM-0011` ou `` `operacao/administrador/ADM-0011.md` ``): sem link clicavel, sem alerta. Recomendada, por ser a mais simples e nao exigir mudar o cofre.
2. **Link com caminho relativo ao cofre** (`[[../operacao/administrador/ADM-0011]]`): nao funciona no Obsidian para pasta fora do cofre.
3. **Manter** e tratar os 16 como falso positivo conhecido (documentar no `_LEIAME` de `operacao/administrador` e/ou fazer o `notas.py quebrados` ignorar ids `ADM-/COORD-/SEARCH-/T-`, ajuste de ferramenta, area N4).

Se for a opcao 1 ou 3, avaliar tambem a convencao: templates e regras que mandam escrever `[[ADM-####]]` (ex.: `Fluxo de tarefa`, perfis) vao gerar novos casos.

---

## Atendimento

Coordenador, 2026-10-04: escalado ao ADM-0024 com a aprovacao do humano. Proposta: opcao 1 (trocar `[[ADM-####]]` por codigo), `Bem-vindo.md` para decisao do humano (texto simples ou arquivar) e convencao nova para nao gerar casos novos. Fecha quando o Administrador concluir o ADM-0024.

Coordenador, 2026-10-04: **concluido.** O Administrador concluiu o ADM-0024 e corrigiu os 15 links `[[ADM-00NN]]` (commit `4e01855`, merge `49cd50d`; aviso registrado no COORD-0029). O link de `BRAIN/Bem-vindo.md` virou texto, e o arquivamento da nota segue no COORD-0029 (Bibliotecario).
