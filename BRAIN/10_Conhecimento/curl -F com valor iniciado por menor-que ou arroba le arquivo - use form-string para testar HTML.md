---
tipo: problema-solucao
status: ativo
origem: T-0008 (Revisor), curado pelo Bibliotecario
tarefa: T-0008
confianca: alta
fontes: ["experimento na revisao da T-0008", "https://curl.se/docs/manpage.html"]
verificado_em: 2026-10-01
valido_para: curl 7+/8 (multipart com -F)
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [teste, curl, entradas-extremas, revisor, armadilha]
---
# curl -F com valor iniciado por menor-que ou arroba le arquivo - use form-string para testar HTML

## Sintoma

`curl -F 'nome=<script>alert(1)</script>' ...` nao envia o HTML: a requisicao nem sai e `%{http_code}` mostra `000`. Parece que o servidor caiu, ou o caso passa sem ser testado.

## Ambiente

curl 7+/8, formulario multipart. Observado na revisao da T-0008 (projeto lab).

## Causa raiz

No `-F 'campo=valor'`, valor iniciado por `<` e lido como "conteudo do arquivo" e valor iniciado por `@` vira upload de arquivo. O curl tenta abrir o arquivo `script>alert(1)</script>`, falha e aborta.

## Solucao

Para enviar o texto literal (HTML, script), use `--form-string 'nome=<script>...'`.

Uso intencional do comportamento: `-F 'nome=<arquivo.txt'` manda um valor muito grande (ex.: 1 MB) sem estourar o limite de argumentos do shell.

## Como verificar que foi resolvido

Com `--form-string` a resposta e um status HTTP real (no lab: 303) e o texto aparece escapado na listagem.

## O que nao funcionou

- `-F 'nome=<script>...'` -> `000`.
- `-F "nome=$(valor de 1 MB)"` -> "argument list too long"; `-F "nome=<nome1m.txt"` funcionou (422).

## Links confiaveis

- [curl man page, opcoes -F e --form-string](https://curl.se/docs/manpage.html): `@` e `<` tem significado especial em `-F`; `--form-string` envia o valor literal.

## Relacionadas

- [[Matriz de verificacao]]: o checklist "Entradas extremas" pede HTML/script em todo campo; um `000` silencioso deixaria o caso sem teste.

## Origem

Revisao da T-0008 (projeto lab), candidato do Revisor.

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao ativo. Sem duplicata no Brain; evidencia experimental e fonte oficial citada.
