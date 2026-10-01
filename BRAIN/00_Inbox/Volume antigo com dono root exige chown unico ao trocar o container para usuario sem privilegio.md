---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/dev
tarefa: T-0008
pesquisa:
confianca: alta
fontes: []
verificado_em: 2026-10-01
valido_para: Docker Engine 29.1 / Compose 2.40, imagem python:3.13.15-slim (Debian 13)
criado: 2026-10-01
decisao:
tags: [docker, seguranca, cwe-250, volume, usuario]
---
# Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio

## Conteudo proposto

Ao adicionar `USER` sem privilegio a uma imagem que ja gravava em volume nomeado:

- Volume **novo**: herda a posse da pasta da imagem (`mkdir /uploads && chown app:app /uploads` antes do `USER`). Funciona sem ajuste.
- Volume **antigo** (arquivos de root): o app falha com `PermissionError: [Errno 13]` ao gravar. Nao ha migracao automatica.
- Ajuste unico, sem apagar dados, usando a propria imagem e o projeto Compose: `docker compose run --rm --no-deps -u 0 --entrypoint chown app -R 10001:10001 /uploads`. Idempotente; apos ele, arquivos antigos e novos gravam normalmente.
- Dica extra: a tag de patch mais nova de `python:3.13-slim` pode ainda trazer pacote com correcao pendente; `apt-get update && apt-get upgrade -y` no estagio base resolve, mas a camada em cache nao repete (`build --pull --no-cache`).

## Evidencia

Teste na T-0008: volume criado com `velho.png` de root; gravar com a imagem nova -> `PermissionError`; apos o `chown` -> gravou, ambos os arquivos com uid 10001. Volume novo: upload 303, arquivo pertence a `app`.

## Links confiaveis

- [Docker: volumes](https://docs.docker.com/engine/storage/volumes/): volume vazio recebe o conteudo da imagem (a parte de volume ja existente nao e documentada; aqui foi testada).

## Por que e reaproveitavel

Todo projeto que endurecer a imagem com `USER` e tiver volume em uso. Fecha a ressalva da nota CWE-250.

## Relacionadas no Brain

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]
- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]
