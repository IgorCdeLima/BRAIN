---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: agente/revisor
tarefa: T-0008
pesquisa:
confianca: alta
fontes: [experimento na revisao da T-0008]
verificado_em: 2026-10-01
valido_para: curl 7+/8 (multipart com -F)
criado: 2026-10-01
decisao:
tags: [teste, curl, entradas-extremas, revisor]
---
# curl -F com valor iniciado por menor-que ou arroba le arquivo - use form-string para testar HTML

## Conteudo proposto

No `curl -F 'campo=valor'`, um valor que comeca com `<` e lido como "conteudo do arquivo" e um que comeca com `@` vira upload de arquivo. Assim, `-F 'nome=<script>alert(1)</script>'` nao envia o HTML: o curl tenta abrir o arquivo `script>alert(1)</script>`, falha e a requisicao nem sai (`%{http_code}` = `000`).

Para testar entradas extremas com HTML ou script num formulario multipart, use `--form-string 'nome=<script>...'`, que envia o texto literal. Use `-F 'nome=<arquivo.txt'` de proposito quando quiser mandar um valor muito grande (ex.: 1 MB) sem estourar o limite de argumentos do shell.

## Evidencia

Revisao da T-0008 (projeto lab): `-F 'nome=<script>...'` -> `000`; o mesmo com `--form-string` -> 303 e o texto apareceu escapado na listagem. `-F "nome=$(1 MB)"` falhou com "argument list too long"; `-F "nome=<nome1m.txt"` -> 422.

## Links confiaveis

- [curl man page, opcoes -F e --form-string](https://curl.se/docs/manpage.html): `@` e `<` tem significado especial em `-F`; `--form-string` envia o valor literal.

## Por que e reaproveitavel

O checklist "Entradas extremas" da matriz de verificacao pede HTML/script em todo campo. Um `000` silencioso pode ser lido como "servidor caiu" ou passar despercebido, deixando o caso sem teste.

## Relacionadas no Brain

- [[Matriz de verificacao]]

## Decisao do Bibliotecario
