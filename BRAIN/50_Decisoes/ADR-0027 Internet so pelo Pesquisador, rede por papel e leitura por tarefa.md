---
tipo: decisao
status: aceita
decidido_em: 2026-10-05
decidido_por: humano
substituida_por:
criado: 2026-10-05
tags: [ambiente, agentes, pesquisa, seguranca, rede, sandbox, lancador, perfis, adm-0029, adm-0030]
---
# ADR-0027 Internet so pelo Pesquisador, rede por papel e leitura por tarefa

## Contexto

- Hoje ([[ADR-0017 Papel Pesquisador e internet por fontes confiaveis]]) o Pesquisador navega livremente, mas os demais papeis abrem por `WebFetch` os dominios de `agentes/fontes-confiaveis.json` (item 2) e a Seguranca consulta `osv.dev` com `pip-audit`/`osv-scanner` (item 5). Todo papel que le uma pagina da internet fica exposto a instrucoes escondidas (*prompt injection*).
- Na T-0018 (container do ambiente, projeto `ambiente`) o humano decidiu, em 2026-10-05:
  - Q4/Q10 (`COORD-0033`, [[ADM-0029]]): "Qualquer outro agente, incluindo o administrador, tem que realizar uma requisicao ao pesquisador procurar na internet por ele. Fora isso, os outros agentes ficam sim limitados a agencia que mantem a IA e ferramentas do git." e "Cada agente em cada worktree/tarefa tem que saber apenas da propria tarefa e do que o BRAIN disponibiliza."
  - Q11/Q12 (`COORD-0036`, [[ADM-0030]]): `github.com` so para quem faz merge e push (Coordenador e Administrador); o Pesquisador navega como achar melhor, mas nao roda codigo e so grava `.md`.
- Na sessao do Administrador de 2026-10-05 o humano confirmou e fechou os pontos em aberto:
  - "Qualquer pesquisa na internet deve ser realizada pelo pesquisador [...] o pesquisador deve procurar e colocar no inbox do BRAIN para o bibliotecario trabalhar. Mesmo o seguranca deve requisitar pesquisas na internet para o Pesquisador."
  - "o fontes-confiaveis vira so ponto de partida."
  - "Apenas o Pesquisador sai para pesquisar na internet; coordenador e administrador devem fazer apenas merge e push pelo git; os demais agentes so acessam as coisas na maquina e a propria empresa da IA para nao parar de funcionar."
- Requisitos detalhados e roteiros de conferencia: RF-26, RF-31, RF-32, RF-33, RF-35 e RF-37 de `projetos/ambiente/docs/requisitos/requisitos.md` (branch da T-0018). Analise de risco: `SEC-T0018-01`.

## Decisao

1. **Navegacao na internet so pelo Pesquisador.** `WebFetch` e `WebSearch` sao negados a todos os outros papeis, **inclusive a Seguranca e o Administrador**. Quem precisa de um fato da internet abre `SEARCH-####`; o Pesquisador procura e entrega a nota no `BRAIN/00_Inbox`, onde vale como pista ate o Bibliotecario catalogar ([[Fluxo de pesquisa]]). Substitui o item 2 da ADR-0017.
2. **Pesquisador sem lista de dominios.** `WebFetch`/`WebSearch` livres, inclusive paginas e arquivos `raw` do GitHub para procurar codigo (sem `git clone`). `agentes/fontes-confiaveis.json` deixa de ser filtro e passa a ser **ponto de partida** do Pesquisador: as fontes preferidas, que ele tenta primeiro e cita como confiaveis. Continua N4.
3. **Pesquisador nao roda codigo e so grava Markdown.** Interpretadores e execucao de arquivos negados no perfil (`python3`, `py`, `node`, `bash`, `sh`, `./`, `npx`, `pip`), `autoAllowBashIfSandboxed: false`; comandos so de leitura e git de leitura e commit. Edit/Write so em arquivos `.md` de `operacao/pesquisas`, `BRAIN/00_Inbox` e `operacao/coordenador` (`ferramentas/hooks/restringir_escrita.py`). Os comandos dele nao tem rede.
4. **Rede dos comandos por papel** (sandbox do Claude Code, RF-31):

   | Papel | Rede dos comandos | Para que |
   |---|---|---|
   | Pesquisador | nenhuma | navega so por `WebFetch`/`WebSearch` |
   | Coordenador | `github.com` e `localhost` | git: `fetch`, `pull`, merge e push |
   | Administrador | `github.com` (host) | git: merge e push |
   | Demais (dev, engenheiro, designer, seguranca, revisor, bibliotecario) | so `localhost` | trabalho na maquina (testes, Designer abrindo a aplicacao) |

   O trafego do proprio Claude Code com a Anthropic (API e login) nao passa pelo sandbox e continua liberado para todos: e o que mantem os agentes funcionando. `curl`/`wget` para fora de `localhost` continuam negados a todos.
5. **Seguranca sem consulta direta a bases de vulnerabilidade.** Substitui o item 5 da ADR-0017: `pip-audit`/`osv-scanner` deixam de consultar `osv.dev` pela rede. A Seguranca pede a consulta ao Pesquisador por `SEARCH-####` (pacotes e versoes exatos), ou registra a verificacao como **nao feita** no SEC, com o motivo. Uso de uma base local espelhada fica para uma decisao futura, se fizer falta.
6. **Leitura limitada a propria tarefa** (RF-33). Para os papeis de worktree, o lancador `papel` gera regras `Read` negadas e `sandbox.filesystem.denyRead` para outros worktrees, outros projetos, cartoes de outras tarefas e `logs/`. Ficam liberados: o proprio worktree, o proprio cartao, `BRAIN/`, as regras (`CLAUDE.md`, definicoes) e os canais de pedido `operacao/coordenador` e `operacao/pesquisas` (para numerar e acompanhar os proprios pedidos, premissa P11). Papeis da copia principal mantem a leitura atual, menos a credencial e as transcricoes (RF-35).
7. **Onde ficam as regras.** No container, as chaves do sandbox (RF-26, RF-31, RF-35) ficam em managed settings na imagem (`/etc/claude-code/managed-settings.json`, dono root), onde o agente nao altera; se a T-0020 mostrar que nao valem com `CLAUDE_CONFIG_DIR`, vao para os perfis dos papeis em `agentes/perfis/` (pedido ao Administrador). Regras que dependem do papel ou da tarefa (itens 1, 3, 4 e 6) ficam nos perfis e no lancador.
8. **Vigencia.** No host, a negacao de `WebFetch`/`WebSearch` (itens 1 e 5), o fim da lista para o Pesquisador (item 2) e as regras de escrita do Pesquisador (item 3) valem assim que implementadas. A rede por papel pelo sandbox (item 4) e a leitura por tarefa (item 6) valem no container, conferidas pelos roteiros da T-0020; no host o Administrador continua sem sandbox, limitado pelas permissoes do perfil.

## Alternativas consideradas

| Alternativa | Pros | Contras |
|---|---|---|
| Manter a ADR-0017 (fontes confiaveis para todos) | Menos pedidos de pesquisa | Todos os papeis leem paginas da internet; a lista nao separa "quem le" de "quem envia" |
| Excecao de rede so para `pip-audit`/`osv-scanner` da Seguranca | Auditoria de dependencias automatica | Abre rede de comando justo no papel que analisa codigo nao confiavel; o humano recusou ("mesmo o seguranca") |
| `github.com` para todos os papeis | `fetch` em qualquer worktree | Caminho de saida de dados para todos (`SEC-T0018-01`); nenhum passo dos papeis de worktree precisa do GitHub |
| Pesquisador com comandos e internet aberta | Pode clonar e testar codigo | Junta leitura de conteudo nao confiavel com execucao e envio |
| Firewall no container (`NET_ADMIN`) | Filtra tambem o trafego do Claude Code e do Docker | Permissao extra no container; decisao Q4 adiou para depois da analise da Seguranca |

## Consequencias

- **Positivas:**
  - So um papel le a internet, e ele nao executa nada nem tem rede nos comandos: quem le conteudo nao confiavel nao consegue enviar dados para fora por comando.
  - Toda pesquisa vira nota no Inbox, reaproveitada pelos outros papeis (menos pesquisa repetida e menos tokens).
  - Um agente enganado em uma tarefa nao le outras tarefas nem outros projetos.
- **Negativas / riscos:**
  - Mais `SEARCH-####`: duvida bloqueante custa sessoes extras (Pesquisador e retomada). Usar `nao-bloqueante` sempre que der.
  - Auditoria de dependencias da Seguranca fica mais lenta (por `SEARCH`) ou registrada como nao feita.
  - Risco residual aceito pelo humano: `github.com` no Coordenador e no Administrador e caminho de saida (o proxy decide pelo nome, admite *domain fronting*; um texto malicioso pode trazer o token do atacante). Limitado aos papeis da copia principal, que nao leem paginas da internet. Avaliacao pela Seguranca na T-0019.
  - Downloads do Docker dos projetos (imagens, pacotes no build do lab) sao feitos pelo daemon, fora do sandbox: esta ADR nao os limita.
  - Notas antigas do Brain citam links para os demais papeis abrirem; esses links passam a ser referencia para o humano ou ponto de partida para um `SEARCH`.

## Implementacao (depois do aceite, cada mudanca com aprovacao do humano)

- [ ] `ferramentas/papel.py`: parar de injetar `WebFetch(domain:...)` nos papeis que nao sao o Pesquisador; Pesquisador com `WebFetch`/`WebSearch` sem lista; regras de leitura por tarefa (item 6).
- [ ] `agentes/perfis/`: negar `WebFetch`/`WebSearch` em todos os perfis menos o Pesquisador (inclusive Seguranca e Administrador); Pesquisador sem interpretadores e com `autoAllowBashIfSandboxed: false`; Seguranca sem `pip-audit`/`osv-scanner` com rede; `allowedDomains` por papel (ou managed settings, item 7).
- [ ] `ferramentas/hooks/restringir_escrita.py`: Pesquisador so `.md` nas tres pastas.
- [ ] Regras: `CLAUDE.md` (hierarquia de conhecimento, item 3), `BRAIN/60_Agentes` (Pesquisador, Seguranca, Administrador, demais papeis que citam fontes confiaveis), `BRAIN/70_Workflows/Fluxo de pesquisa.md`, `agentes/_LEIAME.md` e definicoes em `agentes/`.
- [ ] ADR-0017: itens 2 e 5 marcados como substituidos por esta ADR (`substituida_por` parcial anotado no texto, sem apagar).
- [ ] Roteiros de conferencia (RF-31, RF-32, RF-33, RF-37) executados no container pela T-0020 ou registrados como nao verificados.

## Relacionadas

- [[ADR-0017 Papel Pesquisador e internet por fontes confiaveis]]
- [[ADR-0018 Papel Administrador com senha e aprovacao a cada mudanca]]
- [[ADR-0013 Lancador de papeis e identidade dos agentes]]
- [[ADM-0029]], [[ADM-0030]]
