---
tipo: workflow
status: ativo
versao: 2
fase: 2
criado: 2026-09-28
atualizado: 2026-09-28
tags: [workflow, tarefas]
---
# Fluxo de tarefa

Equipe: **humano** (Product Owner e integrador), **Engenheiro de Software**, **Dev**, **Revisor** e **Bibliotecário**.

O repasse entre agentes acontece **por arquivos** — cartão da tarefa, commits e registros em `qualidade/` —, nunca copiando conversas. O humano só diz a cada papel quando começar.

## Três conceitos

| Conceito | O que define | Onde |
|---|---|---|
| **Onde** | A pasta em que o agente trabalha | Worktree da tarefa (criado no Orca) ou cópia principal `D:\01_IA` |
| **Quem** | O papel do agente: regras, permissões e modelo | Escolhido no lançador: `papel engenheiro`, `papel dev`, `papel revisor`, `papel bibliotecario` — tem que bater com o campo `papel:` do cartão |
| **O quê** | A tarefa | Cartão `operacao/tarefas/T-####.md`, identificado pelo nome do worktree |

## Status do cartão

```mermaid
stateDiagram-v2
    [*] --> backlog
    backlog --> pronta: humano aprova
    pronta --> em_andamento: Dev começa
    em_andamento --> revisao: Dev entrega
    revisao --> correcao: Revisor encontra defeito
    correcao --> em_andamento: Dev corrige
    revisao --> aprovada: Revisor aprova
    aprovada --> concluida: humano faz o merge
    concluida --> [*]
```

(`em_andamento` = `em-andamento` no cartão.)

## Passo a passo

1. **Cartão** (humano): criar ou revisar `operacao/tarefas/T-####.md` e mudar o status para `pronta`.
2. **Worktree** (humano): no Orca, *Create Worktree* no repositório do projeto, nome `T-####-descricao`, *Branch from* `main`, **terminal em branco** (não escolher agente).
3. **Dev** (humano digita no terminal do worktree): `D:\01_IA\ferramentas\papel dev`
   → o Dev implementa, commita, preenche a Entrega e muda o status para `revisao`.
4. **Revisor** (humano, no mesmo worktree, depois de fechar o Dev): `D:\01_IA\ferramentas\papel revisor`
   → o Revisor verifica, commita `VER-####` (e `BUG-`/`SEC-`) no branch e muda o status para `aprovada` ou `correcao`.
5. **Se `correcao`**: voltar ao passo 3. O Dev lê o VER e corrige. Depois, passo 4 de novo — **todo novo commit exige um novo VER**.
6. **Merge** (humano): com status `aprovada`, fazer o merge do branch na `main`, mudar o status para `concluida` e excluir o worktree no Orca.
7. **Bibliotecário** (humano, num terminal em `D:\01_IA`): `D:\01_IA\ferramentas\papel bibliotecario`
   → cura os candidatos do Inbox e commita.

### Tarefas de engenharia (`papel: engenheiro` no cartão)

Mesmo fluxo, com três diferenças:

- No passo 3 o comando é `D:\01_IA\ferramentas\papel engenheiro`. O Engenheiro escreve só em `docs/` (requisitos, modelos Mermaid, avaliações, ADRs `proposta`) e cria os **cartões de implementação** em `backlog`.
- O Revisor verifica a documentação pela coluna "Documentação de projeto" da matriz de verificação.
- Antes do merge, o humano responde as questões em aberto e **aceita ou rejeita os ADRs** (muda o `status` do ADR). Depois, revisa os cartões de implementação criados e muda para `pronta` os que quiser executar.

Guia de modelagem: [[Padroes de modelagem]].

## O lançador `papel`

Antes de abrir o Claude, ele confere a pasta, a tarefa e o status do cartão, e recusa com uma mensagem clara se algo estiver errado. Depois abre o Claude já no papel certo, com o pedido inicial ("Execute a tarefa T-0001", "Revise a tarefa T-0001", "Processe o Inbox do Brain").

| Papel | Onde roda | Status exigido do cartão | Modelo |
|---|---|---|---|
| `engenheiro` | Worktree da tarefa | `pronta`, `em-andamento` ou `correcao` (cartão com `papel: engenheiro`) | Opus |
| `dev` | Worktree da tarefa | `pronta`, `em-andamento` ou `correcao` (cartão com `papel: dev`) | Sonnet |
| `revisor` | Worktree da tarefa | `revisao` | Opus |
| `bibliotecario` | Cópia principal `D:\01_IA` | — | Sonnet |

Opções: `--verificar` (só confere, não abre o Claude) e `--sem-pedido` (abre sem o pedido inicial).

Para conferir que deu certo: o cabeçalho do Claude mostra `@dev`, `@revisor` ou `@bibliotecario`. Se uma sessão abrir sem papel, o próprio Claude avisa e os commits dela são recusados.
