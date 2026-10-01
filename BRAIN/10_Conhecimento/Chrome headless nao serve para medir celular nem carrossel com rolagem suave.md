---
tipo: problema-solucao
status: ativo
origem: agente/revisor (T-0011), curado pelo Bibliotecario
tarefa: T-0011
pesquisa:
confianca: media
fontes: ["projetos/lab: qualidade/verificacoes/VER-0016.md"]
verificado_em: 2026-09-30
valido_para: "google-chrome --headless=new (Linux, 2026-09); extensao Claude in Chrome"
revisar_em: 2027-03-30
criado: 2026-09-30
decisao: promovido
tags: [revisao, design, chrome, headless, responsivo, armadilha]
---
# Chrome headless nao serve para medir celular nem carrossel com rolagem suave

## Sintoma

Ao revisar o prototipo HTML da T-0011 (resultado observado, nao pesquisado):

1. Com `--window-size=320,...` o `--screenshot` sai com 320 px, mas o `innerWidth` visto pelo script e 500.
2. `scrollBy({behavior:"smooth"})` deixa `scrollLeft` em 0 e o evento `scroll` nao dispara; parece defeito do script (carrossel que "nao rola").
3. A extensao Claude in Chrome nao abre paginas `file://`.

## Ambiente

`google-chrome --headless=new` no Linux (2026-09) e extensao Claude in Chrome.

## Causa raiz

1. O `--headless=new` tem largura minima de 500 px: medir rolagem horizontal ou largura de cartao assim da numero errado.
2. A rolagem suave nao anda com `--virtual-time-budget` nem numa janela do Chrome real com `document.visibilityState === "hidden"` (caso da janela controlada pela extensao).
3. A extensao nao aceita `file://`.

## Solucao

1. Largura de celular: abrir a pagina dentro de um `<iframe style="width:320px">` numa pagina auxiliar, rodar com `--allow-file-access-from-files` e ler o resultado com `--dump-dom`.
2. Rolagem: usar `--force-prefers-reduced-motion` (se o script respeita) ou `scrollTo({behavior:"instant"})` seguido de `dispatchEvent(new Event("scroll"))` para verificar a logica. Registrar no VER que a animacao em si nao foi vista.
3. Servir a pasta com `python3 -m http.server <porta> --bind 127.0.0.1` e parar o servidor no fim.

## Como verificar que foi resolvido

A largura medida dentro do iframe e 320 (nao 500) e o `scrollLeft` muda apos o `scrollTo` instantaneo.

## O que nao funcionou

Medir em `--window-size` abaixo de 500 e confiar em `scrollBy` suave em janela oculta.

## Por que vale guardar

Sem isso o Revisor (ou Designer) abre BUG falso de "carrossel nao rola" ou aprova responsivo medido em 500 px.

## Origem

VER-0016 do `lab`, revisao da T-0011. Confianca media: uma unica observacao, sem fonte externa.

## Relacionadas no Brain

Nenhuma nota de revisao visual no Brain ainda (busca por "chrome", "responsivo", "headless" em 2026-10-01).

## Decisao do Bibliotecario

Promovido (2026-10-01) como problema-solucao, confianca media (observado em 1 verificacao). Revisar em 2027-03-30 porque depende de versao do Chrome.
