---
tipo: pedido-coordenador
id: COORD-0017
status: concluido
urgencia: nao-bloqueante
pedido_por: dev
tarefa: T-0010
criado: 2026-10-01
atendido_em: 2026-10-02
adm:
tags: [lab, upload, fila, capacidade, avaliacao]
---
# COORD-0017 - Criar tarefa de avaliacao e implementacao de fila de processamento de imagem

## Pedido

- [ ] Criar um cartao para o **Engenheiro** avaliar (matriz de pesos, `docs/avaliacoes/`) e decidir o desenho de uma **fila de processamento de imagem** no lab, e depois cartoes de implementacao conforme o resultado.
- [ ] Perguntas para a avaliacao: (1) fila assincrona com worker (upload grava o bruto, responde 202, worker decodifica) x manter decodificacao sincrona com fila limitada; (2) broker/worker candidatos (RQ/Redis, Celery, fila no PostgreSQL, SQS) e custo no Docker Compose; (3) estado "processando" na interface e no modelo do produto (impacto de UX: o humano ja descartou, na sessao da Seguranca de 2026-10-01, atraso de 1-5 min na exibicao; reavaliar com criterios); (4) arquivo bruto nao validado no disco: nova superficie, exige analise de ameacas da Seguranca; (5) rate limit por cliente, cotas e proxy (T-0015); (6) gatilho para adotar: quando a aplicacao for exposta ou houver volume.
- [ ] Se o Engenheiro nao tiver base para decidir (arquitetura de capacidade, filas, escala), registrar isso e **propor ao humano um novo papel "Arquiteto de Software"** (via ADM-####, area N4). Minha opiniao: por ora o Engenheiro cobre (avalia tecnologias e modela); um Arquiteto so se justifica se aparecerem varias decisoes de sistema distribuido; comecar pelo Engenheiro com SEARCH ao Pesquisador e testar o limite.

## Motivo

Na T-0010 foi implementado o minimo: orcamento de pixels (SEC-T0010-01) e fila de espera limitada com 503 imediato (SEC-T0010-02, `FILA_MAXIMA = 8`, commits da rodada 3 no branch). Isso protege o processo, mas nao escala: a decodificacao continua no servidor web. Decisao de arquitetura e do Engenheiro, nao do Dev; o Dev nao cria tarefas.

---

## Atendimento

Coordenador, 2026-10-02: com o "sim" do humano, criado o cartao **T-0016** (`papel: engenheiro`, `backlog`) com as seis perguntas como criterios de aceite e a saida para propor o papel Arquiteto se faltar base. O humano espera derivar uma tarefa de implementacao dessa avaliacao.
