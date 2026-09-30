---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: pauta
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#12)
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, cwe-434, upload]
---
# CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado

## Conteudo proposto

**O que e:** o servidor aceita arquivo de tipo perigoso (HTML/SVG com script, executavel, arquivo enorme) e depois o guarda ou serve de forma que ele age. 12o lugar no CWE Top 25 de 2025.

**Como aparece na nossa stack:**
- Confiar em `UploadFile.content_type` ou na extensao: ambos vem do cliente e sao falsificaveis.
- Ler o corpo inteiro na memoria antes de checar o tamanho (ver SEC-0001 e [[Recusa previa por Content-Length esconde a validacao do upload]]).
- Servir o arquivo com o `Content-Type` que o cliente informou, permitindo `text/html` ou SVG com script.
- Guardar dentro da pasta servida como estatico.

**Controle:**
1. Allowlist de extensoes e de tipos reais (ex.: PNG/JPEG/WebP); validar por **assinatura (magic bytes)** e, se imagem, tentando abrir/reprocessar com biblioteca de imagem.
2. Nome gerado no servidor (UUID); guardar o original so como metadado.
3. Limite de tamanho aplicado **durante a leitura** (por blocos), nao so por `Content-Length`.
4. Guardar fora da webroot; servir com `Content-Type` fixado pelo servidor e `X-Content-Type-Options: nosniff`.
5. Evitar SVG de usuario, ou sanitizar.

**Como testar:** enviar `.html` renomeado para `.png`, PNG com sufixo duplo (`a.png.html`), arquivo acima do limite sem `Content-Length` (chunked) e SVG com `<script>`.

## Evidencia

Cheat sheet de upload da OWASP consultado em 2026-09-30 (allowlist de extensao, content-type nao confiavel, assinatura, nome gerado, limite de tamanho, armazenamento fora da webroot). Caso concreto ja visto no lab (T-0003).

## Links confiaveis

- [CWE-434 (MITRE)](https://cwe.mitre.org/data/definitions/434.html): definicao oficial.
- [File Upload Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html): lista completa de controles.

## Por que e reaproveitavel

Todo projeto com upload.

## Relacionadas no Brain

- [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]
- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario
