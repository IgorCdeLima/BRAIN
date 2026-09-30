# Como configurar outro computador

Roteiro para trabalhar no ambiente 01_IA em outra maquina. Repositorios:

- Ambiente e Brain: https://github.com/IgorCdeLima/BRAIN
- Projeto lab: https://github.com/IgorCdeLima/lab

## 1. Programas

| Programa | Observacao |
|---|---|
| Git for Windows | Traz o Git Bash, usado pelos hooks |
| Python 3 | Com o lancador `py` (instalador oficial do python.org) |
| Claude Code (terminal) | PowerShell: `irm https://claude.ai/install.ps1 \| iex`; depois `claude` para fazer login |
| Docker Desktop | Precisa estar aberto para rodar o lab |
| Obsidian | Versao 1.12.7 ou maior |
| Orca | https://www.onorca.dev |

## 2. Clonar no mesmo caminho: D:\01_IA

Hooks, lancador e permissoes usam o caminho `D:\01_IA`. Clone exatamente assim:

```powershell
git clone https://github.com/IgorCdeLima/BRAIN.git D:\01_IA
git clone https://github.com/IgorCdeLima/lab.git D:\01_IA\projetos\lab
```

Se a maquina nao tiver disco `D:` (ou for Linux), siga a secao **Linux** mais abaixo.

## 3. Ativar os hooks do Git (uma vez por repositorio)

```powershell
git -C D:\01_IA config core.hooksPath .githooks
git -C D:\01_IA\projetos\lab config core.hooksPath .githooks
```

## 4. Travar o modo bypass do Claude Code

Crie `C:\Users\<usuario>\.claude\settings.json` com:

```json
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

## 5. Obsidian

- Abrir a pasta `D:\01_IA\BRAIN` como Vault.
- Configuracoes -> Sobre -> **Interface de linha de comando**: ativar e clicar em **Registrar**. Abrir um terminal novo e conferir com `obsidian version`.
- O Git e a fonte de verdade: nao use o Obsidian Sync para editar o mesmo conteudo nas duas maquinas.

## 6. Orca

- Adicionar os repositorios `D:\01_IA` e `D:\01_IA\projetos\lab`.
- Settings -> Agents: modo **Manual** (remover `--dangerously-skip-permissions` do Claude).
- Worktrees sempre com **terminal em branco**; o papel e iniciado pelo lancador.

## 7. Conferir

Num terminal em `D:\01_IA`, com o Obsidian aberto:

```powershell
D:\01_IA\ferramentas\papel bibliotecario --verificar
```

Esperado: `Tudo certo`.

## Linux (ou outro caminho que nao D:\01_IA)

A raiz do ambiente vem da variavel `IA_RAIZ`; sem ela, vale `D:/01_IA` (Windows nao muda nada).
Os hooks do Git acham a raiz sozinhos pelo repositorio. Onde as regras citam `D:\01_IA`, leia `$IA_RAIZ`.

1. Programas: git, python3, Docker (usuario no grupo `docker`), Claude Code (`curl -fsSL https://claude.ai/install.sh | bash`),
   Obsidian (Flatpak `md.obsidian.Obsidian` serve) e Orca (AppImage em https://github.com/stablyai/orca/releases).
2. Clonar em qualquer pasta, mantendo `projetos/lab` dentro dela:

   ```bash
   git clone https://github.com/IgorCdeLima/BRAIN.git ~/Documentos/01.GITHUB/BRAIN
   git clone https://github.com/IgorCdeLima/lab.git ~/Documentos/01.GITHUB/BRAIN/projetos/lab
   ```

3. `IA_RAIZ` com o caminho absoluto da raiz, em `~/.profile`, `~/.bashrc` e `~/.config/environment.d/01_ia.conf`
   (o ultimo vale para apps graficos como o Orca; exige sair e entrar na sessao).
4. Shim do lancador `py` (hooks e permissoes usam `py -3`), em `~/.local/bin/py`:

   ```sh
   #!/bin/sh
   [ "$1" = "-3" ] && shift
   exec python3 "$@"
   ```

5. Hooks do Git e `~/.claude/settings.json`: iguais aos passos 3 e 4 acima.
6. Obsidian: Vault em `$IA_RAIZ/BRAIN`; ativar o CLI como no passo 5. Se `obsidian version` nao existir no terminal
   (Flatpak), criar `~/.local/bin/obsidian` com `exec flatpak run md.obsidian.Obsidian "$@"`.
7. Lancador: `$IA_RAIZ/ferramentas/papel.sh <papel>` (no lugar de `D:\01_IA\ferramentas\papel`).
   Conferir com `$IA_RAIZ/ferramentas/papel.sh bibliotecario --verificar`.

## Rotina entre os dois computadores

1. **Ao comecar:** `git pull` nos dois repositorios (`D:\01_IA` e `D:\01_IA\projetos\lab`).
2. **Ao terminar:** commit e `git push` nos dois.
3. Nao deixe trabalho sem commit numa maquina e comece o mesmo arquivo na outra.
4. Ficam so na maquina (nao sincronizam): `logs/`, volumes do Docker, worktrees do Orca e configuracoes pessoais.
