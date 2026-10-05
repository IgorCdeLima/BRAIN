---
tipo: pedido-coordenador
id: COORD-0016
status: concluido
urgencia: nao-bloqueante
pedido_por: revisor
tarefa: ambiente
criado: 2026-10-01
atendido_em: 2026-10-02
adm: ADM-0015
tags: [erro-inesperado, permissao, scratchpad, revisor]
---
# COORD-0016 - Perfil do Revisor nega escrita no scratchpad da sessao

## Pedido

- [x] Avaliar a causa e propor a melhoria (ajuste do perfil via ADM, ou aviso nas regras do Revisor).

Erro exato (hook PreToolUse do Write), na revisao da T-0010, pasta `/home/igor/orca/workspaces/lab/T-0010-imagem-pillow`:

```
PreToolUse:Write hook error: Este papel so pode escrever em: qualidade, .../operacao/tarefas, .../operacao/pesquisas, .../operacao/coordenador, .../BRAIN/00_Inbox. Escrita em '/tmp/claude-1000/-home-igor-orca-workspaces-lab-T-0010-imagem-pillow/<sessao>/scratchpad/gen.py' negada.
```

O que tentava fazer: gravar um script temporario que gera as imagens de teste (exemplos de entrada do `requisitos.md`) para enviar a aplicacao rodando. O scratchpad e a pasta temporaria da propria sessao, fora do projeto.

## Motivo

Nao contornei por escrita em outro lugar. Rodei o mesmo script por stdin (`docker compose -p t0010-rev run --rm -T --no-deps test python - <<'EOF'`), gerando as imagens em memoria dentro do container. Isso funcionou, mas cada ajuste reenvia o script inteiro. Liberar o scratchpad da sessao (temporario, fora do Git) para o Revisor, ou registrar nas regras que o caminho e stdin num container, evita a duvida nas proximas revisoes com upload.

---

## Atendimento

Coordenador, 2026-10-02: mesma causa do COORD-0010 e do COORD-0012 (hook `restringir_escrita` sem o scratchpad da sessao na lista do Revisor). A correcao ja esta pedida no **ADM-0015** (item 3 libera `@scratchpad` para Seguranca e Revisor) -> `escalado`. O contorno por stdin num container, usado aqui, e valido ate la. Ao concluir o ADM-0015, marcar este COORD como `concluido`.

Coordenador, 2026-10-05, com aprovacao do humano: ADM-0015 `concluido` (hook com `@scratchpad`, merge de `admin/hook-scratchpad`; teste real pela Seguranca na revisao da T-0013 em 2026-10-04, registrado no ADM-0025). Pedido `concluido`.
