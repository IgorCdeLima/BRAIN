---
tipo: decisao
status: aceita
decidido_em: 2026-09-30
decidido_por: Igor
substituida_por:
criado: 2026-09-30
tags: [ambiente, agentes, coordenacao, seguranca]
---
# ADR-0016 Papeis Coordenador e Seguranca

## Contexto

- Na T-0003 (upload de imagem) a revisao de seguranca obrigatoria ficou com o Revisor, que encontrou o BUG-0006 e o SEC-0001 so na primeira rodada. Nao havia analise de ameacas antes do Dev.
- As regras ja citavam os papeis `seguranca` e `coordenador` (`regras.json`, `qualidade/`), mas eles nao existiam.
- O humano fazia sozinho a conducao: saber o proximo passo, merge, Docker, fechar cartao, push. Parte disso foi feita numa sessao do app desktop, sem papel, e os commits entraram sem os trailers `Agente/Tarefa/Modelo`.

## Decisao

1. **Coordenador** (Opus, copia principal, sem cartao; tarefa `coordenacao-AAAA-MM-DD`): panorama, triagem de cartoes, proximo passo com o comando exato, merge `--no-ff` e passos operacionais **apos o "sim" do humano**, fechamento do cartao. Nao escreve codigo, nao inicia papeis, nao aprova tarefas. Merge e push ficam em "pergunta" no perfil.
2. **Seguranca** (Opus, worktree da tarefa), com dois modos como o Designer: **analise de ameacas** (cartao proprio, antes do Dev) e **revisao de seguranca** (cartao em `revisao` com `seguranca: sim`, antes do Revisor fechar, sem mudar o status).
3. Nova marca no cartao: `seguranca: sim|nao`. O Revisor considera os SEC bloqueantes (severidade media ou maior) na decisao.
4. A conducao do dia a dia passa a ser feita pelo Coordenador; sessoes sem papel ficam para manutencao do proprio ambiente.

## Alternativas consideradas

| Alternativa | Por que nao |
|---|---|
| Engenheiro como segunda aprovacao depois do Revisor | Duplica o Revisor; o Engenheiro rende mais antes do Dev, definindo regras |
| Coordenador que inicia os outros papeis sozinho | Quebra a identidade dos agentes do [[ADR-0013 Lancador de papeis e identidade dos agentes]] |
| Seguranca so dentro do Revisor | Foi o modelo da T-0003; mesmo agente com foco dividido |

## Consequencias

- Mais uma sessao Opus nas tarefas com `seguranca: sim`: usar a marca so quando o criterio do [[Fluxo de tarefa]] pedir.
- Commits de conducao passam a ter trailers.
- A avaliacao geral do modelo depois da T-0005 fica no cartao T-0006.
