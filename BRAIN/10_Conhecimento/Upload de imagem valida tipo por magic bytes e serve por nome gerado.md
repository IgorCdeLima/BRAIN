---
tipo: padrao
status: ativo
origem: T-0003 (curado pelo Bibliotecario a partir do candidato do Dev)
confianca: media
fontes: ["projeto lab: T-0003, SEC-0001"]
verificado_em: 2026-09-30
valido_para: FastAPI/Starlette, upload de imagem JPEG/PNG/WebP
revisar_em: 2027-03-30
criado: 2026-09-30
tags: [upload, seguranca, fastapi, padrao]
decisao: promovido
---
# Upload de imagem valida tipo por magic bytes e serve por nome gerado

## Contexto

Aplicacao web que recebe imagem enviada pelo usuario e a serve de volta (usado na T-0003 do lab).

## Problema

Confiar em extensao ou `Content-Type` do cliente e usar o nome enviado abre caminho para arquivo disfarcado e path traversal.

## Solucao

- **Tipo pelos magic bytes:** JPEG `FFD8FF`, PNG (assinatura de 8 bytes), WebP `RIFF....WEBP`.
- **Nome gerado** no servidor com `secrets.token_hex`; o nome do cliente nunca vai ao disco.
- **Rota de servico** aceita apenas o regex do nome gerado (impede path traversal).
- **Header** `X-Content-Type-Options: nosniff` na resposta.
- **Leitura limitada** a limite + 1 byte, para detectar excesso sem carregar tudo.

## Trade-offs

- **Ganha:** entrada validada pelo conteudo real; sem controle do cliente sobre o caminho do arquivo.
- **Perde:** o limite de tamanho firme depende de tratar `Content-Length` ausente (chunked) e, idealmente, de um proxy; ver [[Recusa previa por Content-Length esconde a validacao do upload]].

## Quando NAO usar

Quando a imagem precisa ser reprocessada (redimensionar, remover metadados): ai decodificar com biblioteca de imagem (decisao do Pillow adiada na T-0003) valida melhor que so a assinatura.

## Relacionadas

- [[Recusa previa por Content-Length esconde a validacao do upload]]: armadilha de limite de tamanho neste padrao.
