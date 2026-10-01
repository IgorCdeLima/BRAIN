---
tipo: pedido-coordenador
id: COORD-0014
status: concluido
urgencia: nao-bloqueante
pedido_por: pesquisador
tarefa: ambiente
criado: 2026-10-01
atendido_em: 2026-10-01
adm:
tags: [pesquisa, search-0003, pillow, erro-inesperado]
---
# COORD-0014 - Rodar PIL.features.version() numa wheel real do Pillow 12.3.0 (SEARCH-0003)

## Pedido

- [x] Em pasta temporaria fora de qualquer repositorio (ex.: `/tmp/pil-teste`), rodar:

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

Coordenador, 2026-10-01, com aprovacao do humano. O `venv` do host falha (`No module named 'ensurepip'`), entao foi usado o fallback previsto: container descartavel `python:3.13-slim` (`docker run --rm`), sem pasta no host e sem volume.

Comando: `docker run --rm python:3.13-slim sh -c 'pip install -q pillow==12.3.0; python -c "<mesmo -c do pedido>"; ls /usr/local/lib/python3.13/site-packages/pillow.libs'`

Saida de `features.version()`:

```
[('libjpeg_turbo', '3.1.4.1'), ('jpg', '6.2'), ('webp', '1.6.0'), ('zlib', '1.3.1'), ('libtiff', '4.7.1'), ('littlecms2', '2.19'), ('freetype2', '2.14.3'), ('jpg_2000', '2.5.4')]
```

`pillow.libs`: libXau 6.0.0, libavif 16.4.2, libbrotlicommon/dec 1.2.0, libfreetype 6.20.6, libharfbuzz 0.61421.0, libjpeg 62.4.0, liblcms2 2.0.19, liblzma 5.8.3, libopenjp2 2.5.4, libpng16 16.58.0, libsharpyuv 0.1.2, libtiff 6.2.0, libwebp 7.2.0, libwebpdemux 2.0.17, libwebpmux 3.1.2, libxcb 1.1.0, libzstd 1.5.7.

Resultado: confere com o esperado (`dependencies.json` da tag 12.3.0): libjpeg-turbo 3.1.4.1, libwebp 1.6.0, lcms2 2.19, libtiff 4.7.1. Nenhuma divergencia. Pista para o Bibliotecario anexar ao SEARCH-0003 / nota correspondente, se quiser.

Erro inesperado (causa): o host Linux nao tem o pacote `python3-venv`; o perfil do Pesquisador nao permite Docker. Melhoria: nenhuma regra nova necessaria; o fallback via container ja estava no pedido e funcionou pelo Coordenador.
