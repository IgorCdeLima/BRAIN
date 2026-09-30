---
tipo: candidato
status: inbox
tipo_proposto: padrao
origem: agente/pesquisador
tarefa: pauta
pesquisa: SEARCH-0001
confianca: media
fontes: [cwe.mitre.org, docs.python.org, cheatsheetseries.owasp.org]
verificado_em: 2026-09-30
valido_para: CWE Top 25 2025 (#6); Python 3.9+
criado: 2026-09-30
decisao:
tags: [seguranca, cwe, cwe-22, path-traversal, uploads]
---
# CWE-22 path traversal se evita resolvendo o caminho e conferindo que fica dentro da pasta base

## Conteudo proposto

**O que e:** o usuario manda um nome como `../../etc/passwd` e o servidor le ou grava fora da pasta prevista. 6o lugar no CWE Top 25 de 2025.

**Como aparece na nossa stack:**
- Rota `/uploads/{nome}` que faz `open(PASTA / nome)` ou `FileResponse(PASTA / nome)`.
- Gravar o arquivo enviado usando `UploadFile.filename` como nome.
- Parametro de rota do tipo `{caminho:path}` (aceita barras).
- Caminho absoluto no parametro: `Path(base) / "/etc/passwd"` descarta a base.

**Controle:**
1. Melhor: nunca usar nome do usuario; gerar nome no servidor (UUID) e guardar o nome original so como metadado.
2. Para servir arquivo por nome: `alvo = (BASE / nome).resolve()` e exigir `alvo.is_relative_to(BASE.resolve())`, senao 404. `resolve()` elimina `..` e symlinks; `is_relative_to` (Python 3.9+) e so comparacao de texto, por isso vem depois do `resolve()`.
3. Alternativa: buscar o arquivo pelo id no banco, sem receber caminho.
4. Pasta de uploads fora do que a aplicacao serve como estatico e sem permissao de execucao.

**Como testar:** requisitar `/uploads/../../etc/passwd`, `%2e%2e%2f`, `..%2f`, caminho absoluto e nome com `\`; esperar 404/400, nunca conteudo.

## Evidencia

Documentacao do Python (pathlib) consultada em 2026-09-30: `resolve()` normaliza `..` e symlinks; `is_relative_to` desde 3.9 e apenas textual. Cheat sheet de upload recomenda nome gerado no servidor. Aparece no lab (traversal em `/uploads`).

## Links confiaveis

- [CWE-22 (MITRE)](https://cwe.mitre.org/data/definitions/22.html): definicao oficial.
- [File Upload Cheat Sheet (OWASP)](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html): nome gerado no servidor evita traversal e sobrescrita.
- [pathlib (Python)](https://docs.python.org/3/library/pathlib.html): `resolve()` e `is_relative_to()`.

## Por que e reaproveitavel

Qualquer rota que le ou grava arquivo por nome vindo de fora.

## Relacionadas no Brain

- [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]
- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]
- [[Mapa das CWE relevantes para Python e FastAPI]]

## Decisao do Bibliotecario
