---
tipo: candidato
status: arquivado
decisao: fundido em [[pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in]] (2026-10-02). Mesmo fato validado; o resultado extra de no-new-privileges ficou na nota de only-binary.
origem: T-0014
tags: [pip-tools, docker, dependencias]
---
# pip-compile em container so com /tmp precisa copiar tambem os .txt existentes

- **Fato validado:** servico `lock` que copia so os `.in` para `/tmp` resolve tudo do zero e sobe todas as indiretas sem mudanca nos `.in` (filelock 4.0.8 -> 4.0.9). Correcao: `cp /in/*.in /out/*.txt /tmp/` antes de compilar; os 3 travados saem identicos.
- **Premissa errada (T-0014):** tratei a diferenca como "deriva do PyPI" sem comparar o mecanismo.
- **Resultado extra:** `no-new-privileges` e `cap_drop: [ALL]` no servico lock funcionam sem quebrar o pip-compile.
- Relacionado: nota do Inbox "pip-compile so preserva as versoes travadas se o arquivo de saida existir ao lado do in".
