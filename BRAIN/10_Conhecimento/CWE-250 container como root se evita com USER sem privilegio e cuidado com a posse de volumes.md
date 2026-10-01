---
tipo: padrao
status: ativo
origem: SEARCH-0002 (Pesquisador), curado pelo Bibliotecario
tarefa: T-0005
pesquisa: SEARCH-0002
confianca: media
fontes: ["https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html", "https://docs.docker.com/engine/storage/volumes/", "https://cwe.mitre.org/data/definitions/250.html"]
verificado_em: 2026-09-30
valido_para: Docker Engine / Compose atuais
criado: 2026-09-30
decisao: promovido
revisar_em: 2027-03-30
tags: [seguranca, cwe, cwe-250, docker, usuario]
---
# CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes

## Contexto

**O que e:** executar com mais privilegio que o necessario amplia o dano de qualquer outra falha.

## Solucao

**Controle (OWASP Docker, regra 2):** definir usuario sem privilegio no Dockerfile:
```
RUN groupadd -r app && useradd -r -g app app
USER app
```
(ou `-u` no `docker run` / `user:` no Compose).

**Volume nomeado:** a documentacao do Docker diz que um volume **vazio** recebe os arquivos da imagem no primeiro uso. Ela nao trata volume que ja existe com dono root. Nesse caso, dado antigo continua de root e o app sem privilegio nao escreve. Esta parte e pratica, nao documentada: recriar o volume (perde dados) ou ajustar a posse uma vez (`docker run --rm -u 0 -v vol:/dados imagem chown -R app:app /dados`). Testar no lab antes de adotar.

**Como testar:** `docker run --rm imagem id` deve mostrar uid diferente de 0; tentar gravar no volume e ver se a app funciona.

## Evidencia

Leitura das fontes em 2026-09-30. A parte de volume ja existente ficou sem fonte primaria.

## Links confiaveis

- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regra 2 (definir usuario) e modo rootless.
- [Docker: volumes](https://docs.docker.com/engine/storage/volumes/): populacao de volume vazio.
- [CWE-250 (MITRE)](https://cwe.mitre.org/data/definitions/250.html): menor privilegio necessario.

## Por que e reaproveitavel

Todo container do ambiente.

## Relacionadas no Brain

- [[CWE-78 command injection se evita com subprocess em lista e sem shell]]
- [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]]: testado em 2026-10-01 (T-0008); fecha a ressalva do volume existente.
- [[USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid]]: reforco alem do `USER`.

## Decisao do Bibliotecario

Promovido (2026-09-30) como padrao ativo para o `USER` sem privilegio (OWASP Docker lido). Ressalva: a parte de **volume ja existente com dono root** e pratica, sem fonte primaria; testar no lab antes de adotar. Indexado em [[Mapa das CWE relevantes para Python e FastAPI]].
