---
tipo: pedido-coordenador
id: COORD-0002
status: aberto
urgencia: nao-bloqueante
pedido_por: seguranca
tarefa: T-0007
criado: 2026-09-30
atendido_em:
adm:
tags: [brain, conhecimento, bibliotecario, sec-0006]
---
# COORD-0002 - Registrar na nota do Brain que a solucao do 500 foi validada no lab

<!-- Pedido ligado a tarefa, mas aberto aqui (e nao no cartao) por instrucao direta do humano em 2026-09-30. -->

## Pedido

- [ ] Encaminhar ao **Bibliotecario** a edicao da nota `BRAIN/10_Conhecimento/Middleware do FastAPI nao cobre a resposta 500 do ServerErrorMiddleware.md`. Nao ha comando de terminal; o pedido e so editar a nota.
  - Na secao "Origem" (ou "Como verificar que foi resolvido"), registrar que a solucao do envoltorio **foi validada no lab**: commit c273b39 (`AppComCabecalhos`, subclasse do FastAPI cujo `__call__` passa por `CabecalhosSeguranca(super().__call__)`).
  - Evidencia: verificado pela Seguranca no commit a0c6047, registro 98e9fd6 (SEC-0006 `verificado`). Com o banco parado, `GET /` e `POST /produtos` dao 500 com os 4 cabecalhos, sem duplicata. O lifespan e o alvo `app.main:app` continuam funcionando.
  - Detalhe util para a nota: no `send` envolvido, usar `msg.setdefault("headers", [])`, porque a chave `headers` e opcional no `http.response.start` do ASGI.

## Motivo

A Seguranca nao escreve em `BRAIN/10_Conhecimento` (so o Bibliotecario). O candidato que ela deixou no Inbox ja foi promovido e o Inbox foi limpo. Por isso a tentativa de acrescentar a validacao falhou com "File does not exist". Sem esse registro, a nota descreve a solucao sem dizer que ela ja foi testada.

---

## Atendimento

Coordenador, 2026-10-01: nao ha comando a executar; a edicao e em `BRAIN/10_Conhecimento`, area exclusiva do Bibliotecario. Encaminhado ao Bibliotecario: proxima sessao `papel bibliotecario` deve aplicar o pedido acima e mudar este COORD para `concluido`. Continua `aberto` ate la.
