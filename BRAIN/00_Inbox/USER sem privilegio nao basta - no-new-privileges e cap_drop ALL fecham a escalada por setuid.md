---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/seguranca
tarefa: T-0008
pesquisa:
confianca: alta
fontes: ["https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html"]
verificado_em: 2026-10-01
valido_para: Docker Engine / Compose atuais, imagem python:3.13.15-slim (Debian 13)
criado: 2026-10-01
decisao:
tags: [seguranca, docker, cwe-250, hardening, capabilities]
---
# USER sem privilegio nao basta - no-new-privileges e cap_drop ALL fecham a escalada por setuid

## Conteudo proposto

- Com `USER 10001`, o processo fica com `CapEff: 0`, mas continua com `NoNewPrivs: 0` e com o conjunto limite padrao do Docker (`CapBnd: 00000000a80425fb`). A imagem `python:*-slim` traz 9 binarios setuid (`su`, `mount`, `umount`, `passwd`, `chsh`, `chfn`, `newgrp`, `gpasswd`). Com um bug num deles, quem ja executa codigo como `app` volta a ser root.
- Controle no Compose (OWASP Docker, regras 3 e 4):
  ```yaml
  security_opt: ["no-new-privileges:true"]
  cap_drop: [ALL]
  ```
  App FastAPI/uvicorn na porta 8000 funciona assim (testado: health 200, upload 303). Porta abaixo de 1024 exigiria `cap_add: [NET_BIND_SERVICE]`.
- Como testar: `docker exec <app> grep -E "^(CapBnd|NoNewPrivs)" /proc/1/status` deve mostrar `0000000000000000` e `1`.
- **Armadilha relacionada:** para conferir a imagem com `apt-get update && apt list --upgradable`, rode como root (`-u 0`). Como usuario sem privilegio, o `update` falha com `Permission denied` e a lista volta vazia, o que parece "imagem atualizada" sem ser.

## Evidencia

Revisao de seguranca da T-0008 (SEC-T0008-01). Mesma imagem rodada com `--cap-drop ALL --security-opt no-new-privileges`: CapBnd 0, NoNewPrivs 1, app funcional. A armadilha do apt foi observada na mesma sessao.

## Links confiaveis

- [OWASP Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html): regra 3 (capabilities), regra 4 (`no-new-privileges` contra setuid/setgid), regra 8 (somente leitura).

## Por que e reaproveitavel

Todo container do ambiente. Complementa a nota CWE-250, que hoje so cobre a regra 2 (USER).

## Relacionadas no Brain

- [[CWE-250 container como root se evita com USER sem privilegio e cuidado com a posse de volumes]]
- [[pip-audit limpo nao significa imagem limpa porque a camada do sistema fica fora]]
