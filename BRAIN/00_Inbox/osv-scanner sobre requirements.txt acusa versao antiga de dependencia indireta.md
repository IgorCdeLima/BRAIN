---
tipo: candidato
status: inbox
tipo_proposto: problema-solucao
origem: sessao de manutencao do ambiente (instalacao do osv-scanner)
tarefa: ADR-0017
pesquisa:
confianca: media
fontes: ["osv-scanner 2.6.0 rodado no projeto lab em 2026-09-30", "https://github.com/google/osv-scanner"]
verificado_em: 2026-09-30
valido_para: osv-scanner 2.6.x com requirements.txt sem versao das dependencias indiretas
criado: 2026-09-30
decisao:
tags: [seguranca, dependencias, osv-scanner, falso-positivo, armadilha]
---
# osv-scanner sobre requirements.txt acusa versao antiga de dependencia indireta

## Conteudo proposto

Rodar `osv-scanner scan source -L requirements.txt` num projeto que so fixa as dependencias diretas gera **falso positivo**: o scanner resolve as dependencias indiretas por conta propria e pode escolher uma versao antiga, diferente da instalada.

No lab, ele acusou `pygments 2.9.0` (dependencia indireta do pytest) com PYSEC-2023-117 e PYSEC-2026-2987, mas a imagem tinha `pygments 2.21.0`, acima das duas correcoes.

**Como fazer certo:** escanear o que esta instalado na imagem.

```bash
docker exec <container-da-app> pip freeze > /tmp/instalado.txt
osv-scanner scan source -L /tmp/instalado.txt
```

No lab: 33 pacotes instalados, nenhuma vulnerabilidade (2026-09-30). Se o achado vier do `requirements.txt`, conferir a versao real com `pip show <pacote>` no container antes de registrar um SEC.

## Evidencia

- `osv-scanner scan source -L requirements.txt`: 8 pacotes, 2 vulnerabilidades em `pygments 2.9.0`.
- `docker exec lab-app-1 pip show pygments`: versao 2.21.0, requerida pelo pytest.
- `pip freeze` do container (33 pacotes) passado ao osv-scanner: "No issues found".

## Links confiaveis

- [osv-scanner (Google)](https://github.com/google/osv-scanner): uso, formatos suportados e opcoes de scan.
- [OSV.dev](https://osv.dev/): detalhe de cada vulnerabilidade (versoes afetadas e corrigidas).

## Por que e reaproveitavel

- Evita SEC falso e correcao desnecessaria em qualquer projeto Python do ambiente.
- Mostra que o pytest leva o pygments para a imagem de execucao, o que reforca a T-0004 (separar dependencias de teste).

## Relacionadas no Brain

- [[Fontes de referencia para analise de seguranca por CWE e dependencias]]: fontes que o osv-scanner consulta.
- [[Seguranca]]: papel que roda o scan.

## Decisao do Bibliotecario
