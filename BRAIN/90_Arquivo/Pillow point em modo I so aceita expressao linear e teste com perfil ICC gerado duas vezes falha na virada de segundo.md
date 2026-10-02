---
tipo: candidato
status: arquivado
decisao: dividido em 2 notas (2026-10-02). Item 1 (point em modo I) fundido em [[Pillow convert RGB de PNG 16 bits I16 satura e grava a imagem toda branca]]; item 2 (ICC) virou [[Teste de ICC de Pillow com createProfile gerado duas vezes falha na virada de segundo]]. Motivo - uma ideia por nota.
tipo_proposto: problema-solucao
origem: agente/dev
tarefa: T-0010
pesquisa:
confianca: media
fontes: []
verificado_em: 2026-10-01
valido_para: Pillow 12.3.0
criado: 2026-10-01
decisao:
tags: [pillow, imagem, testes, flaky, t-0010]
---
# Pillow point em modo I so aceita expressao linear e perfil ICC gerado duas vezes difere na virada de segundo

## Conteudo proposto

1. Para reescalar PNG de 16 bits em cinza (`I;16`) para 8 bits: `im.convert("I").point(lambda v: v / 257 + 0.5).convert("L")`. O `point` em modo `I` avalia a lambda uma vez simbolicamente e so aceita `a*v + b`; `round(v / 257)` dentro da lambda levanta excecao (aqui virou "corrompida"). O `+ 0.5` faz o arredondamento (30000 -> 117; sem ele, 116).
2. `ImageCms.createProfile("sRGB")` grava a data/hora de criacao no cabecalho ICC (bytes 24-35). Teste que compara dois perfis gerados em momentos diferentes falha de vez em quando (indice 35 = segundos). Gerar uma vez (`functools.cache`).

## Evidencia

T-0010, commit `3c35d3e`: testes de gradiente 16 bits passam; `test_icc_com_script_anexado_e_limpo[WEBP]` falhava ~1 em 5 rodadas ("At index 35 diff: 0x1c != 0x1d") e deixou de falhar com o cache (2 rodadas completas).

## Por que e reaproveitavel

Qualquer conversao de profundidade de bits com Pillow; qualquer teste que compare saida de funcao com relogio embutido.

## Relacionadas no Brain

- [[Pillow convert RGB de PNG 16 bits I16 satura e grava a imagem toda branca]]
