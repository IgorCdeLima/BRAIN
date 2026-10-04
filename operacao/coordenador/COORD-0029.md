---
tipo: pedido-coordenador
id: COORD-0029
status: aberto
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: ambiente
criado: 2026-10-04
atendido_em:
adm:
tags: [brain, arquivo, bibliotecario, adm-0024]
---
# COORD-0029 - Bibliotecario: arquivar a nota Bem-vindo.md

## Pedido

- [ ] Rodar o Bibliotecario (`papel bibliotecario`, na copia principal) para mover `BRAIN/Bem-vindo.md` para `BRAIN/90_Arquivo`:
  - simular: `py -3 ferramentas/notas.py mover "BRAIN/Bem-vindo.md" "BRAIN/90_Arquivo/Bem-vindo.md" --simular`;
  - se a simulacao estiver certa, rodar o mesmo comando sem `--simular`.  - Depois do mover, o Bibliotecario decide se a nota recebe frontmatter `status: obsoleto` ou fica como esta.
  - Ao final, `py -3 ferramentas/notas.py quebrados` deve continuar com 0 links quebrados.
- [x] Avisos do Administrador para registrar aqui:
  - o erro 2 do COORD-0028 (scratchpad do Designer) foi atendido no `ADM-0023`. Falta o teste numa sessao real `papel designer`, na revisao visual da T-0013;
  - o COORD-0026 pode ser fechado: os 15 links de ADM foram corrigidos no `ADM-0024`.

## Motivo

- Item 7 do `ADM-0024`, decisao do humano em 2026-10-04: trocar o link por texto (ja feito pelo Administrador) **e** arquivar a nota padrao do Obsidian.
- Mover nota e so com `notas.py mover`, e so o Bibliotecario usa essa ferramenta (`CLAUDE.md`, secao Obsidian). O Administrador nao faz o trabalho de outro papel.

---

## Atendimento

Coordenador, 2026-10-04. Avisos do Administrador registrados:
- Erro 2 do COORD-0028 (scratchpad do Designer): atendido no ADM-0023. Na revisao visual da T-0013, o Designer usou o scratchpad da sessao para o script do Chrome headless (registrado no COORD-0028).
- COORD-0026: fechado como `concluido`.

Pedido continua `aberto`: falta o humano rodar `papel bibliotecario` na copia principal para arquivar `Bem-vindo.md`.
