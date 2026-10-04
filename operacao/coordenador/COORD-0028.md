---
tipo: pedido-coordenador
id: COORD-0028
status: escalado
urgencia: nao-bloqueante
pedido_por: designer
tarefa: T-0013
criado: 2026-10-03
atendido_em:
adm: ADM-0023, ADM-0025
tags: [ambiente, designer, chrome, permissao, erro-inesperado]
---
# COORD-0028 - Designer: Chrome da extensao nao abre localhost e escrita no scratchpad negada

## Pedido

- [ ] **Erro 1 (extensao Claude in Chrome):** ao abrir `http://127.0.0.1:8213/T-0013/04-prototipo.html` e `http://localhost:8213/...` (servidor `python3 -m http.server 8213 --bind 127.0.0.1` rodando na pasta `docs/design` do worktree `lab/T-0013`, respondendo 200 ao `curl` no mesmo terminal), a captura de tela da extensao devolveu `Error capturing screenshot: Frame with ID 0 is showing error page` nas duas tentativas. Contornado com `google-chrome --headless=new` no terminal (capturas em `docs/design/T-0013/capturas/`). Avaliar se o Chrome da extensao roda em outro host/rede ou se o perfil precisa liberar `localhost`; a revisao visual (porta 8200 + N) depende disso.
- [ ] -> ADM-0023 **Erro 2 (perfil do Designer):** `Write` em `/tmp/claude-1000/.../scratchpad/servir.py` negado pelo hook ("Este papel so pode escrever em: docs/design, qualidade/ux, ..."). Eu queria um servidor de teste de 15 linhas que enviasse o cabecalho CSP final (sem `'unsafe-inline'`) para conferir no navegador que o prototipo nao gera violacao. Nao contornei; a verificacao com CSP real ficou registrada como NAO feita na entrega. Avaliar se o scratchpad da sessao deve ser liberado para o Designer (arquivos temporarios fora do Git).

## Motivo

Erros inesperados de ferramenta e de permissao vao para o Coordenador (`CLAUDE.md`, "Pedidos de comando"). Nenhum bloqueou a fase 1 da T-0013, mas ambos reduzem o que o Designer consegue verificar.

---

## Atendimento

Coordenador, 2026-10-04. Pedido continua `aberto`, com o erro 1 em avaliacao.
- **Erro 2 (scratchpad):** causa confirmada. O hook do ADM-0015 (ja na `main`, `d1f6de2`) aceita `@scratchpad`, mas a decisao do humano o liberou so para Seguranca e Revisor; o perfil do Designer (`agentes/.claude/agents/designer.md`, linha 11) nao tem o token. Escalado ao ADM-0023 com aprovacao do humano. O Designer agiu certo ao nao contornar.
- **Erro 1 (extensao do Chrome e localhost):** causa ainda nao confirmada. Hipoteses: (a) o servidor `python3 -m http.server` morreu quando o comando do Bash terminou (sem `run_in_background`); (b) o Chrome da extensao nao alcanca o `127.0.0.1` da maquina (navegador isolado, ex.: snap/flatpak, ou outra maquina). Proximo passo: teste do Coordenador com o humano (servidor em segundo plano + abrir a pagina pela extensao).

Coordenador, 2026-10-04 (depois do merge da T-0013, `c9d0f4b`):
- **Erro 2:** na revisao visual o Designer usou o scratchpad da sessao para o script temporario do Chrome headless (cartao T-0013, "Revisao visual", "Como reexecutar"). Na pratica o ADM-0023 funcionou numa sessao real `papel designer`.
- **Erro 1:** na revisao visual a extensao respondeu outro erro, "Browser extension is not connected", entao a hipotese (a) nao explica tudo: a extensao nem estava conectada. Designer, Seguranca e Revisor fizeram as medicoes com o Chrome headless e o CDP (360 px de verdade com `Emulation.setDeviceMetricsOverride`), e nenhuma verificacao do cartao ficou presa a extensao. O teste com o humano nao foi feito. A decisao sobre a extensao (o humano conecta e testa, ou o headless com CDP vira o caminho padrao no Fluxo de design) foi escalada ao ADM-0025, item 3, com aprovacao do humano.
- **Melhoria:** com a regra escrita (item 3 do ADM-0025), o Designer nao precisa abrir um COORD a cada revisao em que a extensao falhar. Fecha quando o ADM-0025 registrar a decisao.
