---
tipo: decisao
status: aceita
decidido_em: 2026-09-28
decidido_por: Igor
substituida_por:
criado: 2026-09-28
tags: [ambiente, agentes, permissoes, orca]
---
# ADR-0013 Lançador de papéis e identidade dos agentes

## Contexto

No piloto 1 da T-0001 todas as sessões rodaram **sem papel**: os worktrees foram criados com o Claude padrão do Orca e os Quick Commands previstos no ADR-0011 nunca foram criados. Consequências: sem perfil de permissões, modelo errado, trailers definidos à mão pelo próprio agente, e o hook do Git tratou essas sessões como humanas. Além disso, o humano precisou copiar conversas entre sessões porque não existia um papel com permissão para registrar a verificação. Ver `operacao/tarefas/_arquivo/piloto-1`.

## Decisão

1. **Lançador único** `D:\01_IA\ferramentas\papel <dev|revisor|bibliotecario>`, digitado pelo humano no terminal. Antes de abrir o Claude ele confere: pasta (worktree da tarefa ou cópia principal), número da tarefa pelo branch, existência e status do cartão. Depois define `IA_PAPEL`, `IA_TAREFA` e `IA_MODELO` e abre o Claude com `--agent`, `--add-dir` e `--settings` do papel, já com o pedido inicial. Substitui os Quick Commands do ADR-0011.
2. **Sessão do Claude sem papel não commita:** o hook do Git recusa commit com `CLAUDECODE=1` e sem `IA_PAPEL`, exceto no app desktop (acompanhado pelo humano no chat).
3. **Agente não se atribui papel:** comandos que mencionam `IA_PAPEL` ou o lançador são negados.
4. **Aviso na abertura:** o hook de início de sessão avisa o próprio Claude quando ele abre sem papel.
5. **Papel Revisor** (modelo Opus, diferente do Dev) registra `VER/BUG/SEC` no branch da tarefa e move o cartão para `aprovada` ou `correcao`.
6. **Repasse por arquivos:** cartão (status + Entrega + Revisão), commits e `qualidade/`. O humano só inicia cada papel. **Um VER vale para um commit.**

## Ajustes após o primeiro uso (2026-09-28)

- **Escrita do Revisor por lista de permissões:** uma regra `deny` com exceção `!` não liberou `qualidade/`. A restrição passou para um hook `PreToolUse` na definição do papel (`ferramentas/hooks/restringir_escrita.py`), que só permite escrita nos caminhos listados e nega na dúvida.
- **Exceção `!` não desfaz regras absolutas:** `Read(//**/.env.*)` bloqueava também o `.env.example`. Nos perfis, o bloqueio de `.env.*` passou a ser relativo à pasta da sessão, onde a exceção funciona.
- **Bibliotecário sem número de tarefa:** o hook recusava seus commits (não há `T-####` na `main`). O lançador define `IA_TAREFA=curadoria-AAAA-MM-DD` para ele.

## Alternativas consideradas

| Alternativa | Prós | Contras |
|---|---|---|
| Quick Commands do Orca | Um clique | Dependiam de configuração manual que não aconteceu; não validam pasta nem cartão |
| Coordenador agora | Menos trabalho manual | Orquestração do Orca experimental; `worker-start` não inicia papéis com perfil |

## Consequências

- **Positivas:** o erro do piloto 1 passa a ser detectado antes de começar; o humano deixa de ser o mensageiro entre sessões.
- **Negativas / riscos:** a identidade ainda depende de variável de ambiente — um agente com acesso irrestrito ao shell poderia contorná-la; mitigado pelas regras de permissão e pelos logs.
