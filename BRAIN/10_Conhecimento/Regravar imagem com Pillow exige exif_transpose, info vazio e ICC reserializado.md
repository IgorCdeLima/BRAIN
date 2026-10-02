---
tipo: padrao
status: ativo
origem: T-0010 (Dev), curado pelo Bibliotecario
tarefa: T-0010
confianca: alta
fontes: ["tests/test_imagens.py da T-0010 (lab, 463 testes)"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [pillow, upload, imagem, seguranca]
---
# Regravar imagem com Pillow exige exif_transpose, info vazio e ICC reserializado

## Contexto

Todo upload de imagem em Python que e decodificado e regravado como forma de sanitizar (miniaturas, remocao de metadados, neutralizar conteudo anexado).

## Problema

Gravar com `save()` sem cuidado deixa passar metadados (comentario do JPEG, texto e ICC do PNG), deita a foto de celular, aceita ICC com bytes anexados e deixa decodificar imagens gigantes.

## Solucao

Receita testada (463 testes, T-0010), nesta ordem:

1. `Image.open(BytesIO, formats=[...])`.
2. Conferir o formato (MPO conta como JPEG) e as dimensoes **antes** de `load()`.
3. `load()`.
4. `ImageOps.exif_transpose` (devolve copia, 1o quadro).
5. Converter o modo de cor de forma coerente com o formato de saida; cuidado com `I;16`: [[Pillow convert RGB de PNG 16 bits I16 satura e grava a imagem toda branca]].
6. `saida.info = {}`; senao o `save` mantem o comentario COM do JPEG e o texto/ICC do PNG ([[Pillow save padrao mantem o comentario do JPEG e o ICC do PNG ao regravar sem metadados]]).
7. ICC so se `ImageCms.ImageCmsProfile(BytesIO(icc)).tobytes()` ler; gravar os bytes **reserializados**.
8. Capturar `Exception` (nao so `OSError`) e `DecompressionBombError` a parte, para a mensagem de dimensao ([[Except OSError nao basta no Pillow - DecompressionBombError e SyntaxError escapam e viram 500]]).
9. Limitar decodificacoes simultaneas e responder 503 ao estourar a espera. **Atencao:** um `threading.BoundedSemaphore` dentro de rota `def` prende o threadpool ([[Semaforo dentro de rota def do FastAPI prende o threadpool e trava as outras rotas]]) e nao limita a memoria ao longo do tempo ([[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]]).

## Trade-offs

- **Ganha:** upload sem metadados vazados, sem conteudo anexado, sem 500 por imagem corrompida; testado com 300+ arquivos mutados (so 303 ou 422).
- **Perde:** reencodar custa CPU e pode alterar a qualidade; perde-se perfil ICC invalido e metadados legitimos.

## Quando NAO usar

Quando o arquivo original precisa ser preservado byte a byte (arquivo de prova, anexo juridico). Nesse caso, nao sirva o arquivo diretamente ao navegador.

## Relacionadas

- [[CWE-434 upload sem restricao exige validar o tipo pelo conteudo e servir por nome gerado]]
- [[CWE-212 metadado sensivel em imagem se evita regravando os pixels sem EXIF, GPS e comentarios]]
- [[CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload]]

## Decisao do Bibliotecario

Promovido (2026-10-02) como padrao ativo. Sem duplicata exata: reune num roteiro unico itens que as notas do Pillow tratam em separado. O item do semaforo foi mantido como alerta, com link para as armadilhas que a T-0010 descobriu depois.
