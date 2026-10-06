---
tipo: pedido-coordenador
id: COORD-0036
status: escalado
urgencia: nao-bloqueante
pedido_por: engenheiro
tarefa: T-0018
criado: 2026-10-05
atendido_em: 2026-10-05
adm: ADM-0030
tags: [ambiente, regras, rede, github, pesquisador, perfis, lancador, adm-0009]
---
# COORD-0036 - Rede por papel e Pesquisador sem rodar codigo (respostas Q11 e Q12 da T-0018)

## Pedido

Escalar ao Administrador (area N4: `agentes/perfis/`, `ferramentas/papel.py`, `ferramentas/hooks/restringir_escrita.py`), para juntar ao `ADM-0029` (do `COORD-0033`) ou abrir ADR proprio, com aprovacao do humano. Nao ha comando a rodar agora; o pedido e de mudanca de regra, implementada e testada no container (T-0020).

- [ ] 1. **Rede dos comandos por papel** (RF-31 do projeto `ambiente`). Decisao do humano, 2026-10-05 (Q11): "Negue o acesso ao github a nao ser aqueles que precisam fazer o merge e o push, coordenador e administrador. e no caso o pesquisador para procurar codigo". Proposta: `sandbox.network.allowedDomains` com `github.com` so no perfil do Coordenador; demais papeis do container so `localhost`; Pesquisador sem rede nos comandos (procura codigo pelo `WebFetch`, item 2). O Administrador fica no host e nao muda.
- [ ] 2. **Pesquisador: navegacao livre, sem rodar codigo, so grava `.md`** (RF-32, RF-37). Decisao do humano (Q12): "pode acessar como achar melhor, nao quero dificultar isso para o pesquisador, no entanto ele nao deve ter autorizacao para salvar algum arquivo com alguma extencao diferente de arquivo_pesquisado.md; Isto e, o pesquisador, nao roda codigo". Proposta: `WebFetch`/`WebSearch` sem lista de dominios no Pesquisador (`agentes/fontes-confiaveis.json` vira ponto de partida); no perfil, negar interpretadores e execucao de arquivos (`python3`, `py`, `node`, `bash`, `sh`, `./`, `npx`, `pip`) e `autoAllowBashIfSandboxed: false`; no `restringir_escrita.py`, Edit/Write do Pesquisador so em arquivos `.md` de `operacao/pesquisas`, `BRAIN/00_Inbox` e `operacao/coordenador`. Roteiro de conferencia no RF-37.
- [ ] 3. Lembrete (sem pedido agora): os relatorios `consumo.py`/`uso_brain.py` passam a rodar no host ate a T-0024 (Q13); a mudanca dessas ferramentas, se houver, vira pedido proprio a partir da T-0024.

## Motivo

Respostas do humano as questoes Q11, Q12 e Q13 da T-0018 (registradas em `projetos/ambiente/docs/requisitos/requisitos.md` e no adendo do `ADR-0001`), originadas do `SEC-T0018-01`. O Engenheiro nao altera regras, `agentes/` nem `ferramentas/` (N4).

---

## Atendimento

Coordenador, 2026-10-05, com aprovacao do humano: mudanca de regra em area N4 (`agentes/perfis/`, `ferramentas/papel.py`, `ferramentas/hooks/restringir_escrita.py`) -> escalado ao ADM-0030, separado do ADM-0029 por decisao do humano (mesmo ADR do ambiente), com os itens 1 a 3. Fecha quando o ADM-0030 concluir.
