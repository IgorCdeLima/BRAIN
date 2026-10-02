---
tipo: problema-solucao
status: ativo
origem: T-0010 (Dev), curado pelo Bibliotecario
tarefa: T-0010
confianca: media
fontes: ["commit 3c35d3e (lab, T-0010)"]
verificado_em: 2026-10-01
valido_para: "Pillow 12.3.0"
criado: 2026-10-02
decisao: promovido
revisar_em: 2027-04-01
tags: [pillow, imagem, testes, flaky, icc]
---
# Teste de ICC de Pillow com createProfile gerado duas vezes falha na virada de segundo

## Sintoma

Um teste que compara dois perfis ICC gerados em momentos diferentes falha de vez em quando, por exemplo `At index 35 diff: 0x1c != 0x1d`. Na T-0010, `test_icc_com_script_anexado_e_limpo[WEBP]` falhava cerca de 1 em 5 rodadas.

## Ambiente

Pillow 12.3.0, `ImageCms.createProfile("sRGB")`.

## Causa raiz

`ImageCms.createProfile("sRGB")` grava a data e hora de criacao no cabecalho ICC (bytes 24 a 35). O indice 35 sao os segundos: dois perfis gerados em segundos diferentes nao sao iguais byte a byte.

## Solucao

Gerar o perfil **uma vez** por sessao de teste (`functools.cache` ou fixture com escopo de sessao) e usar o mesmo objeto nos dois lados da comparacao.

## Como verificar que foi resolvido

Rodar a suite varias vezes (na T-0010, 2 rodadas completas sem falha depois do cache; o defeito aparecia 1 em 5).

## O que nao funcionou

Rodar de novo ate passar. A falha e intermitente, nao um erro do codigo testado.

## Relacionadas

- [[Teste de upload com Pillow - CRC do PNG nao e conferido e o ICC do PNG vai comprimido]]: outro cuidado com testes de ICC.
- [[Regravar imagem com Pillow exige exif_transpose, info vazio e ICC reserializado]]: a receita cujo teste de ICC falhava.
- [[Pillow convert RGB de PNG 16 bits I16 satura e grava a imagem toda branca]]: outro achado do mesmo teste da T-0010.

## Origem

T-0010, commit `3c35d3e` (lab). Vale para qualquer teste que compare saida de funcao com relogio embutido.

## Decisao do Bibliotecario

Promovido (2026-10-02) como nota propria, separada do item do `point` em modo `I`, que foi para a nota do PNG de 16 bits (uma ideia por nota). O candidato original esta em `90_Arquivo`.
