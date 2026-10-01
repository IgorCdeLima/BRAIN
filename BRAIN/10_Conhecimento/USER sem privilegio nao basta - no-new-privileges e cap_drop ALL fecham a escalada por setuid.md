---
tipo: padrao
status: ativo
origem: T-0008 (Seguranca), curado pelo Bibliotecario
tarefa: T-0008
confianca: alta
fontes: ["https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html", "SEC-T0008-01 do lab (experimento com --cap-drop ALL e no-new-privileges)"]
verificado_em: 2026-10-01
valido_para: Docker Engine / Compose atuais, imagem python:3.13.15-slim (Debian 13)
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, docker, cwe-250, hardening, capabilities]
---
# USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid

## Contexto

Container que ja roda com `USER` sem privilegio. Aplica-se a todo container do ambiente.

## Problema

Com `USER 10001` o processo fica com `CapEff: 0`, mas continua com `NoNewPrivs: 0` e com o conjunto limite padrao do Docker (`CapBnd: 00000000a80425fb`). A imagem `python:*-slim` traz 9 binarios setuid (`su`, `mount`, `umount`, `passwd`, `chsh`, `chfn`, `newgrp`, `gpasswd`). Com um bug num deles, quem ja executa codigo como `app` volta a ser root.

## Solucao

Controle no Compose (OWASP Docker, regras 3 e 4):

```yaml
security_opt: ["no-new-privileges:true"]
cap_drop: [ALL]
```

App FastAPI/uvicorn na porta 8000 funciona assim (testado: health 200, upload 303). Porta abaixo de 1024 exigiria `cap_add: [NET_BIND_SERVICE]`.

**Como testar:** `docker exec <app> grep -E "^(CapBnd|NoNewPrivs)" /proc/1/status` deve mostrar `0000000000000000` e `1`.

**Armadilha relacionada:** para conferir a imagem com `apt-get update && apt list --upgradable`, rode como root (`-u 0`). Como usuario sem privilegio o `update` falha com `Permission denied` e a lista volta vazia, o que parece "imagem atualizada" sem ser.

## Trade-offs

- **Ganha:** fecha a volta a root por setuid mesmo se o app for comprometido.
- **Perde:** processos que precisam de capability (porta baixa, ping raw) exigem `cap_add` explicito.

## Quando NAO usar

Containers que de fato precisam de privilegio (ferramentas de rede, builds com mount); nesses, adicionar so a capability necessaria em vez de abrir mao do `cap_drop: [ALL]`.

## Links confiaveis

- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regra 3 (capabilities), regra 4 (`no-new-privileges` contra setuid/setgid), regra 8 (somente leitura).

## Relacionadas

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]: cobre so a regra 2 (USER); esta nota fecha o resto.
- [[Volume antigo com dono root exige chown unico ao trocar o container para usuario sem privilegio]]: o outro efeito de trocar o usuario.
- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]: a camada do sistema e onde moram os binarios setuid.

## Decisao do Bibliotecario

Promovido (2026-10-01) como padrao ativo. Medido com a mesma imagem (CapBnd 0, NoNewPrivs 1, app funcional) e apoiado em fonte OWASP.
