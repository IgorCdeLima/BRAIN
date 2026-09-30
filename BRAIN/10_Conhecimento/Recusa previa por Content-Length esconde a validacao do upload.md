---
tipo: problema-solucao
status: ativo
origem: T-0003, BUG-0006 (curado pelo Bibliotecario a partir do candidato do Revisor, fundido com o aprendizado da correcao registrado pelo Dev)
confianca: media
fontes: ["projeto lab: VER-0006, BUG-0006, SEC-0001"]
verificado_em: 2026-09-30
valido_para: FastAPI/Starlette + uvicorn sem proxy
revisar_em: 2027-03-30
criado: 2026-09-30
tags: [upload, validacao, fastapi, starlette, seguranca, armadilha]
decisao: promovido
---
# Recusa previa por Content-Length esconde a validacao do upload

## Sintoma

Upload de arquivo maior que o limite (foto de 3 a 5 MB) devolve um 413 cru em JSON: o usuario perde o formulario e nunca ve a mensagem de validacao da pagina. Em outro caso, um POST com `Transfer-Encoding: chunked` passa sem limite nenhum.

## Ambiente

FastAPI/Starlette + uvicorn sem proxy na frente. Visto na T-0003 do projeto lab.

## Causa raiz

Dois limites foram misturados: o **teto anti-DoS** (middleware, pelo `Content-Length`) e o **limite de negocio** (validado no handler, com mensagem na pagina).

1. **Tetos quase iguais.** Teto = limite + folga pequena (2 MB + 64 KB): quase todo arquivo grande demais cai no middleware, nao no handler. Os testes nao pegam, pois o arquivo "excedido" costuma ficar poucos bytes acima do limite (ex.: +58 bytes).
2. **Chunked escapa do teto.** Sem `Content-Length`, o Starlette le o multipart inteiro (arquivo temporario) antes do handler. Sem proxy, o corpo nao tem limite.

## Solucao

- Teto anti-DoS bem acima do limite de negocio (ex.: 10 MB contra 2 MB) e o limite de negocio validado no handler, com erro na propria pagina. "Recusar cedo" e "validar com mensagem" nao servem ao mesmo limite.
- POST sem `Content-Length`: recusar com 411 (navegadores sempre enviam o cabecalho em formularios) ou contar os bytes envolvendo o `receive` do ASGI.

## Como verificar que foi resolvido

- Enviar um arquivo tipico grande demais (3 MB), nao so limite + 1: deve aparecer a mensagem na pagina.
- Enviar chunked: deve ser recusado (411).
- Reproduzir o que o navegador envia: `curl -H "Expect:" -F "arquivo=@3mb.bin" ...`. Sem `Expect:` vazio, o curl usa `100-continue` para corpos grandes e nao envia o corpo.

## O que nao funcionou

Teto de Content-Length pouco acima do limite de validacao (2 MB + 64 KB): mascarou a validacao (BUG-0006).

## Origem

T-0003 (projeto lab): VER-0006, BUG-0006, SEC-0001. Vale como item do checklist "Entradas extremas": testar o arquivo "um pouco acima", o "tipico grande demais" e o envio chunked.

## Relacionadas

- [[Upload de imagem valida tipo por magic bytes e serve por nome gerado]]: padrao de upload em que este limite se aplica.
- [[Texto com caractere NUL derruba insert no PostgreSQL com erro 500]]: outra entrada extrema que so aparece com teste sistematico.

## Decisao do Bibliotecario

Promovido a `10_Conhecimento`. Fundido o aprendizado da correcao do BUG-0006 que estava no candidato de `create_all`; duas fontes independentes (Revisor e Dev) concordam. Confianca media: correcao verificada no lab, mas sem teste de carga real.
