---
tipo: pedido-coordenador
id: COORD-0028
status: aberto
urgencia: nao-bloqueante
pedido_por: designer
tarefa: T-0013
criado: 2026-10-03
atendido_em:
adm:
tags: [ambiente, designer, chrome, permissao, erro-inesperado]
---
# COORD-0028 - Designer: Chrome da extensao nao abre localhost e escrita no scratchpad negada

## Pedido

- [ ] **Erro 1 (extensao Claude in Chrome):** ao abrir `http://127.0.0.1:8213/T-0013/04-prototipo.html` e `http://localhost:8213/...` (servidor `python3 -m http.server 8213 --bind 127.0.0.1` rodando na pasta `docs/design` do worktree `lab/T-0013`, respondendo 200 ao `curl` no mesmo terminal), a captura de tela da extensao devolveu `Error capturing screenshot: Frame with ID 0 is showing error page` nas duas tentativas. Contornado com `google-chrome --headless=new` no terminal (capturas em `docs/design/T-0013/capturas/`). Avaliar se o Chrome da extensao roda em outro host/rede ou se o perfil precisa liberar `localhost`; a revisao visual (porta 8200 + N) depende disso.
- [ ] **Erro 2 (perfil do Designer):** `Write` em `/tmp/claude-1000/.../scratchpad/servir.py` negado pelo hook ("Este papel so pode escrever em: docs/design, qualidade/ux, ..."). Eu queria um servidor de teste de 15 linhas que enviasse o cabecalho CSP final (sem `'unsafe-inline'`) para conferir no navegador que o prototipo nao gera violacao. Nao contornei; a verificacao com CSP real ficou registrada como NAO feita na entrega. Avaliar se o scratchpad da sessao deve ser liberado para o Designer (arquivos temporarios fora do Git).

## Motivo

Erros inesperados de ferramenta e de permissao vao para o Coordenador (`CLAUDE.md`, "Pedidos de comando"). Nenhum bloqueou a fase 1 da T-0013, mas ambos reduzem o que o Designer consegue verificar.

---

## Atendimento
