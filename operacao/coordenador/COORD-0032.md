---
tipo: pedido-coordenador
id: COORD-0032
status: aberto
urgencia: nao-bloqueante
pedido_por: administrador
tarefa: ambiente
criado: 2026-10-05
atendido_em:
adm: ADM-0009
tags: [ambiente, container, projeto-ambiente, cartoes, adm-0009]
---
# COORD-0032 - Cartoes da fase 2 do ADM-0009: o 01_IA num container (projeto ambiente)

## Pedido

O humano aprovou a fase 2 do `ADM-0009` como um **projeto novo**, `projetos/ambiente` (repositorio proprio, esqueleto criado pelo Administrador, commit `2d0135f`). Criar e triar os cartoes, com o "sim" do humano, nesta ordem:

- [x] 1. -> T-0018 **Engenheiro** - `projeto: ambiente`, `papel: engenheiro`, `seguranca: sim`, `tamanho: grande`. Requisitos e arquitetura do container em `projetos/ambiente/docs` (requisitos, modelos em Mermaid, ADR do projeto). Cobrir no minimo:
  - o que vai na imagem (Claude Code, git, Python 3, tmux, `ferramentas/`, `py` como em `~/.local/bin/py`) e como o repositorio 01_IA, `projetos/*` e `$IA_WORKTREES` entram como volumes;
  - login e configuracao do Claude Code fora da imagem (`CLAUDE_CONFIG_DIR` em volume), sem segredo no repositorio;
  - usuario sem privilegio com o UID/GID do humano (arquivos do volume com o dono certo);
  - caminhos que hoje dependem do host: `IA_RAIZ`, hooks (`py -3 ...`), scratchpad do Claude Code e token `@scratchpad` de `ferramentas/hooks/restringir_escrita.py` (lembrete do `ADM-0015` no `ADM-0009`), `logs/`, transcricoes (`uso_brain.py`, `consumo.py`);
  - tmux no container (`TERM`, UTF-8, `window-size`) e como o humano entra (`docker exec -it ... tmux attach`);
  - as 3 opcoes para os projetos com Docker Compose (socket do host, Docker-in-Docker, rootless/Podman) **descritas e comparadas, sem escolher**: a escolha e do humano depois da analise da Seguranca;
  - o que fica fora desta fase: Coordenador por tarefa (fase 3) e quadro web (fase 4).
  Insumos: `SEARCH-0009` e as 5 notas que ele gerou no `BRAIN/00_Inbox` (pistas), `ADR-0026`, `ADM-0009`.
- [ ] 2. **Seguranca** - analise de ameacas do desenho do Engenheiro (`papel: seguranca`, depois do item 1), com foco na opcao de Docker dos projetos, no login do Claude Code em volume e no que o container enxerga do host. Saida em `projetos/ambiente/docs/seguranca/`. Depois dela, o humano escolhe a opcao de Docker (ADR do projeto).
- [ ] 3. **Dev** - so depois da escolha: `Dockerfile`, `compose` e roteiro de verificacao. Revisao pela Seguranca e pelo Revisor; merge pelo Administrador ou Coordenador, como no lab.
- [x] 4. Lembrar o humano: o **Bibliotecario** cataloga o `SEARCH-0009` (pode ser antes do item 1, para as notas sairem do Inbox).

Como abrir o papel de cada cartao (o humano roda, num terminal comum): `ferramentas/tarefa.sh aceitar T-####` e `ferramentas/tarefa.sh abrir T-#### engenheiro` (ADR-0026).

## Motivo

Criar e triar cartoes e do Coordenador; o Administrador cuidou so da parte de ambiente (esqueleto do repositorio, `docs.podman.io` nas fontes confiaveis). O repositorio `projetos/ambiente` ainda nao tem remoto (decisao do humano: "Depois").

---

## Atendimento

Coordenador, 2026-10-05, com aprovacao do humano:
- Item 1: cartao [[T-0018]] criado em `backlog` (`papel: engenheiro`, `seguranca: sim`, `interface: nao`, `tamanho: grande`), com os criterios do item 1. Vai para `pronta` com o "sim" do humano.
- Item 4: o Bibliotecario catalogou o `SEARCH-0009` (`03f0d54`); as 5 notas sairam do Inbox.
- Itens 2 e 3 (Seguranca e Dev): cartoes criados depois da entrega do Engenheiro, que tambem propoe os cartoes seguintes. Pedido continua `aberto`.
