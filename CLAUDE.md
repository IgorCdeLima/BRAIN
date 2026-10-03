# Ambiente 01_IA — regras globais

Ambiente de uma equipe de agentes de IA para desenvolvimento de software, executada no Orca.
O humano (Igor) é o Product Owner e o aprovador final. Idioma de trabalho: português (pt-BR).

Caminhos: `D:\01_IA` nas regras e definicoes e a raiz do ambiente no Windows. Em outra maquina (ex.: Linux) a raiz e a variavel `IA_RAIZ`; leia `D:\01_IA` como `$IA_RAIZ`.

## Mapa do ambiente

| Pasta | O que é | Quem escreve |
|---|---|---|
| `BRAIN/` | Vault Obsidian: base de conhecimento | Bibliotecário (N3); demais agentes só em `BRAIN/00_Inbox`, se o perfil do papel permitir |
| `BRAIN/60_Agentes`, `BRAIN/70_Workflows` | Regras dos agentes e processos | **Somente o humano** (N4) |
| `agentes/` | Definições executáveis dos papéis | **Somente o humano** (N4) |
| `operacao/tarefas` | Cartões de tarefa e handoffs | Agentes conforme o papel |
| `operacao/pesquisas` | Pedidos de pesquisa `SEARCH-####` | Qualquer papel cria; o Pesquisador responde; o Bibliotecario fecha |
| `operacao/coordenador` | Pedidos ao Coordenador `COORD-####` (com ou sem tarefa; inclui erro inesperado) | Qualquer papel cria; o Coordenador atende ou escala |
| `operacao/administrador` | Pedidos ao Administrador `ADM-####` (area N4, decisao de ambiente, push) | O Coordenador cria ao escalar; o Administrador cria para pedido direto do humano que altere algo; o Administrador atende com aprovacao do humano |
| `logs/` | Telemetria automática (fora do Git) | **Somente os hooks** — agentes não escrevem aqui |
| `operacao/qualidade` | Verificações, bugs e segurança do ambiente | Revisor, Segurança, Coordenador; demais só leem |
| `projetos/<nome>` | Cada projeto é um repositório Git próprio | Conforme o papel, dentro do worktree da tarefa |

Cada pasta tem um `_LEIAME.md` com o propósito e as regras dela. Leia-o antes de escrever na pasta.

## Regras invioláveis

1. **Nunca edite as próprias regras** nem `CLAUDE.md`, `agentes/`, `.claude/`, `BRAIN/60_Agentes` ou `BRAIN/70_Workflows`. Proponha mudanças em `BRAIN/00_Inbox`. Unica excecao: o papel **administrador**, com aprovacao do humano a cada mudanca ([[ADR-0018 Papel Administrador com senha e aprovacao a cada mudanca]]).
2. **Nada é apagado.** Conhecimento superado vira `status: obsoleto` ou vai para `BRAIN/90_Arquivo`; bugs só mudam de status.
3. **Documentação oficial de projeto fica no projeto** (`projetos/<nome>/docs`), nunca no Brain.
4. **Nunca registre segredos** (senhas, tokens, chaves) em notas, logs, commits ou registros de qualidade.
5. **Diagramas são Mermaid** (texto). Imagem nunca é a fonte de verdade. (Excecao do design: conceitos visuais em SVG/PNG sao inspiracao; a fonte de verdade da interface e o prototipo HTML + tokens, ver `BRAIN/70_Workflows/Fluxo de design.md`.)
6. Não use `git push --force` nem reescreva histórico já compartilhado.
7. **Texto novo em arquivos Markdown (.md) sem acentos nem cedilha** (so ASCII: "revisao", "acao", "codigo"), inclusive nomes de arquivo. Texto ja existente pode ficar como esta; ao editar uma linha, nao e preciso converter o resto.
8. **Arquivos se editam com as ferramentas de edicao (Edit/Write), nunca reescrevendo pelo terminal.** No PowerShell, `Get-Content | Set-Content`, `Out-File` e `>` corrompem a codificacao (bloqueados por permissao).

## Pedidos de comando

Precisa de algo que so o humano faria (comando fora do seu perfil, merge, push, acao no Orca)? **Nao peca ao humano.** Crie um pedido `operacao/coordenador/COORD-####.md` (template `Pedido ao Coordenador`), **com ou sem tarefa**, com o comando exato, a pasta e o motivo; no cartao, so a referencia na secao "Pedidos ao Coordenador". Ao humano diga so o numero do pedido criado. Cadeia: agente -> Coordenador -> Administrador (`ADM-####`) -> humano, que so digita o que e exclusivo dele (Orca, lancador `papel`, senha, `sudo`). "Passos do humano" no cartao sao so decisoes (ADR, direcao visual, duvida de produto). Ver [[ADR-0020 Cadeia de pedidos de comando]] e [[ADR-0021 Pedidos ao Coordenador sempre em COORD e numeracao de qualidade por tarefa]].

**Erro inesperado** (ferramenta falhou, arquivo ausente ou movido, permissao negada, comando inexistente, lancador recusou, conflito de merge): nao contorne em silencio. Crie um `COORD-####` com o erro exato, o que tentava fazer e a pasta. O Coordenador avalia a causa e propoe a melhoria (ajuste de regra via `ADM-####`, aviso ao papel afetado ou candidato a conhecimento).

## Hierarquia de conhecimento (antes de pesquisar)

0. Contexto da tarefa + documentação do projeto + **bugs abertos** relacionados aos arquivos que vai alterar.
1. Brain: busque por título, tags, backlinks e texto — **inclusive em `00_Inbox`**. Se usar uma nota, **cite-a** com `[[link]]` e registre-a em "Brain consultado" (Entrega do cartao ou VER): `[[Nota]] - ajudou: sim | parcial | nao - por que` ([[ADR-0023 Medir o uso do Brain por acesso, citacao e utilidade declarada]]).
   Nota do Inbox, antiga (`verificado_em`) ou de baixa confiança = pista a verificar, não verdade.
2. Classifique a dúvida: conceito estável → conhecimento próprio; **fato volátil** (versão, API, preço) → pesquisa externa obrigatória; outra especialidade → consulte o agente especialista.
3. **Pesquisa externa e do Pesquisador** ([[ADR-0017 Papel Pesquisador e internet por fontes confiaveis]]): os demais papeis so abrem os links confiaveis citados nas notas e os dominios de `agentes/fontes-confiaveis.json` (outros sites: o Claude pergunta ao humano; busca aberta e negada). Se o Brain nao responde, crie um pedido `operacao/pesquisas/SEARCH-####.md` (template `BRAIN/99_Sistema/Templates/Pesquisa.md`) com `urgencia: bloqueante` (cartao em `aguardando-pesquisa`, pare) ou `nao-bloqueante` (siga com a premissa registrada na Entrega). Fluxo em `BRAIN/70_Workflows/Fluxo de pesquisa.md`. O resultado entra em `BRAIN/00_Inbox` como pista.
4. Ao terminar, proponha como **candidato a conhecimento** apenas o que é reaproveitável e validado — incluindo resultados negativos ("tentamos X, não funciona por Y").

## Obsidian

- `BRAIN/` e o cofre do Obsidian do humano. Agentes **nao usam o aplicativo nem o CLI do Obsidian**, mas escrevem nas convencoes dele: links `[[Nome]]` (caminho so quando o nome se repete), `[[Nome|alias]]`, `[[Nome#Cabecalho]]`, `![[anexo]]`, propriedades no frontmatter ([[ADR-0025 Agentes mantem o cofre sem usar o Obsidian como ferramenta]]).
- Leitura e busca: leia os arquivos `.md` diretamente.
- Mover ou renomear notas: **somente com `ferramentas/notas.py mover`**, que atualiza os links como o Obsidian faria (inclusive em `operacao/`, `CLAUDE.md` e `agentes/`). Uso restrito ao Bibliotecario, na copia principal (nao em worktrees).
- Templates em `BRAIN/99_Sistema/Templates`. Toda nota nova usa o template do seu tipo, com os metadados preenchidos.

## Git e rastreabilidade

- Git é a fonte de verdade. Commits pequenos, mensagem em português no formato `tipo(escopo): descrição`.
- Todo commit feito por agente termina com os trailers:

  ```
  Agente: <papel>
  Tarefa: <id>
  Modelo: <modelo>
  ```

- Trabalho de agente acontece **sempre num worktree próprio criado pelo Orca**; merge na `main` conforme aprovação. A cópia principal `D:\01_IA` é do humano, do Coordenador e do Bibliotecário.
- Cada papel é iniciado pelo humano com o lançador `D:\01_IA\ferramentas\papel <administrador|coordenador|engenheiro|designer|seguranca|dev|revisor|pesquisador|bibliotecario>` (Linux: `ferramentas/papel.sh`), que confere pasta e cartão e abre o Claude com a definição, o perfil de permissões e o modelo do papel. O perfil prevalece sobre a tabela acima. **Um agente nunca define `IA_PAPEL` nem se atribui um papel.** Sessão sem papel não trabalha: avisa o humano. Fluxo completo em `BRAIN/70_Workflows/Fluxo de tarefa.md`.

## Qualidade

- Registros em `qualidade/`: `VER-####` (verificação), `BUG-####` (defeito), `SEC-####` (segurança), `UX-####` (observacao visual do Designer). Templates em `BRAIN/99_Sistema/Templates/Qualidade`.
- **Numeracao por tarefa:** registro de tarefa leva o id dela e uma sequencia propria: `VER-T0007-01`, `BUG-T0007-01`, `SEC-T0007-01`, `UX-T0007-01`. Confira so os registros da mesma tarefa no worktree; sem consulta a outros branches, sem colisao entre tarefas em paralelo. Registro sem tarefa (feito na copia principal) segue `PREFIXO-####`. Registros antigos nao sao renomeados.
- Toda verificação feita — e toda verificação **não** feita — é registrada. Lacuna omitida é falha.
- Quem corrige um bug não o verifica.
