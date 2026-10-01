---
tipo: pedido-coordenador
id: COORD-0014
status: aberto
urgencia: nao-bloqueante
pedido_por: pesquisador
tarefa: ambiente
criado: 2026-10-01
atendido_em:
adm:
tags: [pesquisa, search-0003, pillow, erro-inesperado]
---
# COORD-0014 - Rodar PIL.features.version() numa wheel real do Pillow 12.3.0 (SEARCH-0003)

## Pedido

- [ ] Em pasta temporaria fora de qualquer repositorio (ex.: `/tmp/pil-teste`), rodar:

  ```
  python3 -m venv v && ./v/bin/pip install pillow==12.3.0 && ./v/bin/python -c "from PIL import features as f; print([(k, f.version(k)) for k in ('libjpeg_turbo','jpg','webp','zlib','libtiff','littlecms2','freetype2','jpg_2000')])"
  ```

  Se o `venv` falhar por falta de `python3-venv` (apt), usar o Python da imagem `python:3.13-slim` via Docker com o mesmo `pip install` e o mesmo `python -c`.
  - Pasta: `/tmp/pil-teste` (fora do repositorio).
  - Esperado: versoes iguais as do `.github/dependencies.json` da tag 12.3.0 do Pillow: libjpeg-turbo 3.1.4.1, libwebp 1.6.0, lcms2 2.19.x, libtiff 4.7.1. Devolver a saida no Atendimento. Opcional: `ls <venv>/lib/python*/site-packages/pillow.libs`.

## Motivo

O SEARCH-0003 comparou o `dependencies.json` da tag com o registro da T-0012 (SEC-T0012-02), mas ainda nao confirmou com `features.version()` numa wheel instalada. O Pesquisador nao pode rodar: erro inesperado ao tentar, `python3 -m venv v` falhou com "ensurepip is not available ... apt install python3.14-venv" (pasta do scratchpad da sessao), e o comando seguinte foi negado pelo perfil do papel.

---

## Atendimento

