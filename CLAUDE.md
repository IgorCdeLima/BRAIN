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
| `logs/` | Telemetria automática (fora do Git) | **Somente os hooks** — agentes não escrevem aqui |
| `operacao/qualidade` | Verificações, bugs e segurança do ambiente | Revisor, Segurança, Coordenador; demais só leem |
| `projetos/<nome>` | Cada projeto é um repositório Git próprio | Conforme o papel, dentro do worktree da tarefa |

Cada pasta tem um `_LEIAME.md` com o propósito e as regras dela. Leia-o antes de escrever na pasta.

## Regras invioláveis

1. **Nunca edite as próprias regras** nem `CLAUDE.md`, `agentes/`, `.claude/`, `BRAIN/60_Agentes` ou `BRAIN/70_Workflows`. Proponha mudanças em `BRAIN/00_Inbox`.
2. **Nada é apagado.** Conhecimento superado vira `status: obsoleto` ou vai para `BRAIN/90_Arquivo`; bugs só mudam de status.
3. **Documentação oficial de projeto fica no projeto** (`projetos/<nome>/docs`), nunca no Brain.
4. **Nunca registre segredos** (senhas, tokens, chaves) em notas, logs, commits ou registros de qualidade.
5. **Diagramas são Mermaid** (texto). Imagem nunca é a fonte de verdade. (Excecao do design: conceitos visuais em SVG/PNG sao inspiracao; a fonte de verdade da interface e o prototipo HTML + tokens, ver `BRAIN/70_Workflows/Fluxo de design.md`.)
6. Não use `git push --force` nem reescreva histórico já compartilhado.
7. **Texto novo em arquivos Markdown (.md) sem acentos nem cedilha** (so ASCII: "revisao", "acao", "codigo"), inclusive nomes de arquivo. Texto ja existente pode ficar como esta; ao editar uma linha, nao e preciso converter o resto.
8. **Arquivos se editam com as ferramentas de edicao (Edit/Write), nunca reescrevendo pelo terminal.** No PowerShell, `Get-Content | Set-Content`, `Out-File` e `>` corrompem a codificacao (bloqueados por permissao).

## Hierarquia de conhecimento (antes de pesquisar)

0. Contexto da tarefa + documentação do projeto + **bugs abertos** relacionados aos arquivos que vai alterar.
1. Brain: busque por título, tags, backlinks e texto — **inclusive em `00_Inbox`**. Se usar uma nota, **cite-a** com `[[link]]`.
   Nota do Inbox, antiga (`verificado_em`) ou de baixa confiança = pista a verificar, não verdade.
2. Classifique a dúvida: conceito estável → conhecimento próprio; **fato volátil** (versão, API, preço) → pesquisa externa obrigatória; outra especialidade → consulte o agente especialista.
3. Pesquisa externa entra em `BRAIN/00_Inbox` como não confiável.
4. Ao terminar, proponha como **candidato a conhecimento** apenas o que é reaproveitável e validado — incluindo resultados negativos ("tentamos X, não funciona por Y").

## Obsidian

- Leitura e busca: leia os arquivos `.md` diretamente.
- Mover ou renomear notas: **somente via Obsidian CLI** (`obsidian move`), que atualiza os links. Uso restrito ao Bibliotecário, na cópia principal (não em worktrees).
- Templates em `BRAIN/99_Sistema/Templates`. Toda nota nova usa o template do seu tipo, com os metadados preenchidos.

## Git e rastreabilidade

- Git é a fonte de verdade. Commits pequenos, mensagem em português no formato `tipo(escopo): descrição`.
- Todo commit feito por agente termina com os trailers:

  ```
  Agente: <papel>
  Tarefa: <id>
  Modelo: <modelo>
  ```

- Trabalho de agente acontece **sempre num worktree próprio criado pelo Orca**; merge na `main` conforme aprovação. A cópia principal `D:\01_IA` é do humano e do Bibliotecário.
- Cada papel é iniciado pelo humano com o lançador `D:\01_IA\ferramentas\papel <engenheiro|designer|dev|revisor|bibliotecario>`, que confere pasta e cartão e abre o Claude com a definição, o perfil de permissões e o modelo do papel. O perfil prevalece sobre a tabela acima. **Um agente nunca define `IA_PAPEL` nem se atribui um papel.** Sessão sem papel não trabalha: avisa o humano. Fluxo completo em `BRAIN/70_Workflows/Fluxo de tarefa.md`.

## Qualidade

- Registros em `qualidade/`: `VER-####` (verificação), `BUG-####` (defeito), `SEC-####` (segurança), `UX-####` (observacao visual do Designer). Templates em `BRAIN/99_Sistema/Templates/Qualidade`.
- Toda verificação feita — e toda verificação **não** feita — é registrada. Lacuna omitida é falha.
- Quem corrige um bug não o verifica.
