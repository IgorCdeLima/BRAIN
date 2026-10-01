---
tipo: problema-solucao
status: ativo
origem: T-0008 (Dev), curado pelo Bibliotecario
tarefa: T-0008
confianca: alta
fontes: ["teste do Dev na T-0008 (volume com velho.png de root)", "https://docs.docker.com/engine/storage/volumes/"]
verificado_em: 2026-10-01
valido_para: Docker Engine 29.1 / Compose 2.40, imagem python:3.13.15-slim (Debian 13)
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [docker, seguranca, cwe-250, volume, usuario]
---
# Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio

## Sintoma

Depois de adicionar `USER` sem privilegio a uma imagem que ja gravava em volume nomeado, o app falha ao gravar com `PermissionError: [Errno 13]`.

## Ambiente

Docker Engine 29.1, Compose 2.40, `python:3.13.15-slim` (Debian 13).

## Causa raiz

- Volume **novo** herda a posse da pasta da imagem (`mkdir /uploads && chown app:app /uploads` antes do `USER`) e funciona sem ajuste.
- Volume **antigo** tem arquivos e pasta de root e nao ha migracao automatica; o usuario sem privilegio nao escreve.

## Solucao

Ajuste unico, sem apagar dados, usando a propria imagem e o projeto Compose:

```
docker compose run --rm --no-deps -u 0 --entrypoint chown app -R 10001:10001 /uploads
```

Idempotente; depois dele, arquivos antigos e novos gravam normalmente.

Dica extra: a tag de patch mais nova de `python:3.13-slim` pode ainda trazer pacote com correcao pendente; `apt-get update && apt-get upgrade -y` no estagio base resolve, mas a camada em cache nao repete (usar `build --pull --no-cache`).

## Como verificar que foi resolvido

Teste na T-0008: volume criado com `velho.png` de root; gravar com a imagem nova -> `PermissionError`; apos o `chown` -> gravou, ambos os arquivos com uid 10001. Volume novo: upload 303 e arquivo pertence a `app`.

## O que nao funcionou

Esperar que o Docker corrija a posse sozinho: a documentacao so trata volume vazio (recebe o conteudo da imagem); o caso de volume ja existente nao e documentado e foi testado aqui.

## Links confiaveis

- [Docker: volumes](https://docs.docker.com/engine/storage/volumes/): volume vazio recebe o conteudo da imagem.

## Relacionadas

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]: esta nota fecha a ressalva sem teste dela.
- [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]: o proximo passo do endurecimento.
- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]: origem da dica de atualizar a imagem.

## Origem

T-0008 (projeto lab), candidato do Dev.

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao ativo; evidencia experimental. A parte de volume existente continua sem fonte primaria, o que fica declarado acima.
