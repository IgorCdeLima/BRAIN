---
tipo: problema-solucao
status: ativo
origem: T-0010 (Seguranca, SEC-T0010-01 e SEC-T0010-02), curado pelo Bibliotecario
tarefa: T-0010
confianca: media
fontes: ["SEC-T0010-01 (lab, commit b1640cc)", "SEC-T0010-02 (lab)"]
verificado_em: 2026-10-01
valido_para: "FastAPI/Starlette com AnyIO (threadpool padrao de 40), Pillow 12.3.0"
criado: 2026-10-01
decisao: promovido
revisar_em: 2027-04-01
tags: [seguranca, fastapi, dos, threadpool, pillow, cwe-770]
---
# Semaforo dentro de rota def do FastAPI prende o threadpool e trava as outras rotas

## Sintoma

Com um limite de concorrencia sobre uma operacao cara (ex.: decodificar imagem), cerca de 40 requisicoes baratas na fila bastam para **todas** as outras rotas `def` (listagem, arquivos, health) pararem. Medido: com 60 envios na fila, `GET /` levou 29,8 s (antes: 0,2 s).

## Ambiente

FastAPI/Starlette com AnyIO (threadpool padrao de 40 threads), rota sincrona `def`, Pillow 12.3.0.

## Causa raiz

`threading.Semaphore.acquire(timeout=...)` dentro de uma rota `def` faz cada requisicao na fila ocupar uma thread do threadpool durante a espera. Quando as 40 threads estao esperando a vaga, nao sobra thread para as demais rotas.

## Solucao

Esperar sem prender thread: rota `async def` com `asyncio.Semaphore` ou `anyio.Semaphore`, executando so o trabalho pesado em `anyio.to_thread.run_sync`; ou um `CapacityLimiter` proprio.

Limitar por **quantidade** de decodificacoes tambem nao limita a memoria: um WebP de 89 KB com 50 MP custa ~1,1 GiB no processo; duas vagas somam 2 GiB, o que levou ao OOM kill (`OOMKilled=true`, exit 137) num host de 3,4 GB. Dimensione a vaga pelo pior caso ou use um orcamento em pixels, e leia [[Orcamento de pixels nao segura a memoria se as arenas do malloc retem o que o Pillow libera]] antes de achar que isso basta.

## Como verificar que foi resolvido

Enfileirar mais de 40 envios pesados e medir o tempo de `GET /` e de uma rota de listagem durante a fila: deve ficar na casa de centesimos de segundo.

## O que nao funcionou

Semaforo ou `BoundedSemaphore` com timeout dentro de rota `def`. E dimensionar o limite so pela quantidade de operacoes simultaneas.

## Relacionadas

- [[CWE-770 recursos sem limite se evitam com limite de corpo, timeout e rate limit]]
- [[CWE-409 bomba de descompressao se evita com limite de pixels do Pillow tratado como erro e limite de bytes no upload]]
- [[Pagina de 503 que consulta o banco vira 500 justamente quando o servidor esta sobrecarregado]]: o 503 desse limite precisa funcionar sem o banco.

## Origem

SEC-T0010-01 e SEC-T0010-02 (projeto lab, commit `b1640cc`).

## Decisao do Bibliotecario

Promovido (2026-10-02). A segunda armadilha (memoria) ficou aqui como aviso curto, com a analise completa na nota do orcamento de pixels, para manter uma ideia principal por nota.
