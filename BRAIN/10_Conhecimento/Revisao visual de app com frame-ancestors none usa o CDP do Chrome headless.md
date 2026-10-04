---
tipo: problema-solucao
status: ativo
origem: agente/designer (T-0013), curado pelo Bibliotecario
tarefa: T-0013
confianca: media
fontes: ["projetos/lab: operacao/tarefas/T-0013.md, secao Revisao visual"]
verificado_em: 2026-10-04
valido_para: "google-chrome --headless=new (Linux, 2026-10), Node 22"
criado: 2026-10-04
decisao: promovido
revisar_em: 2027-04-04
tags: [revisao, design, chrome, headless, cdp, responsivo, csp]
---
# Revisao visual de app com frame-ancestors none usa o CDP do Chrome headless

## Sintoma

Na revisao visual da T-0013 (lab) o truque do iframe de [[Chrome headless nao serve para medir celular nem carrossel com rolagem suave]] nao serve: o app manda `frame-ancestors 'none'` e `X-Frame-Options: DENY`, e o iframe fica em branco. A extensao Claude in Chrome estava desconectada.

## Ambiente

Chrome headless novo (`--headless=new`) no Linux, Node 22 (WebSocket nativo, sem dependencias), app com CSP restritiva.

## Causa raiz

O iframe e bloqueado de proposito pela CSP e pelo `X-Frame-Options` do app (ver [[CWE-1021 clickjacking se evita com CSP frame-ancestors e X-Frame-Options em middleware do Starlette]]). A solucao nao deve afrouxar o app: controlar o navegador direto pelo protocolo CDP.

## Solucao (observada, 1 uso)

Chrome headless com `--remote-debugging-port` e um script Node falando CDP:

- `Emulation.setDeviceMetricsOverride {width: 360, height: 780, mobile: true}`: `innerWidth` = 360 de verdade (sem o minimo de 500 px).
- `Emulation.setScriptExecutionDisabled {value: true}`: pagina sem JS.
- `Emulation.setFocusEmulationEnabled {enabled: true}` + `Input.dispatchKeyEvent` Tab: `:focus-visible` aparece na captura (com `element.focus()` numa janela sem foco, nao aparece).
- `Emulation.setEmulatedMedia prefers-reduced-motion: reduce`: a rolagem do carrossel anda sem depender de animacao.
- Formulario com arquivo: `DataTransfer` + `new File([...])` atribuido a `input.files`, depois `form.submit()`.
- `Network.requestWillBeSent` e `Log.entryAdded`: lista de origens e console (violacoes de CSP) por estado.

## Como verificar que foi resolvido

A captura em 360 px mostra a pagina real do app (nao em branco), com foco visivel e sem violacao de CSP no log do console.

## O que nao funcionou

- Iframe com a pagina do app: bloqueado por `frame-ancestors 'none'`.
- Extensao do Chrome: desconectada nesta sessao (COORD-0028).
- `element.focus()` em janela sem foco: nao mostra `:focus-visible`.

## Limites

Nao mostra a animacao da rolagem suave nem toque real; leitor de tela fica fora.

## Origem

T-0013 (lab), revisao visual do Designer, 2026-10-04. Mede celular e foco visivel do app real, com a CSP real, sem alterar o app. Uma unica ocorrencia: confianca `media`.
