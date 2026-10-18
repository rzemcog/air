# Diff / удобная навигация

Исторические файлы здесь не лежат отдельными копиями: их версии можно открыть по tag.

```bash
git log --oneline --all
git diff snapshot-baseline..snapshot-bootstrap-proposed -- 04_REFERENCES/bootstrap
git diff snapshot-baseline..snapshot-output-candidate -- 01_CURRENT/output-policy.md
git diff snapshot-output-candidate..snapshot-approved-output -- 01_CURRENT/output-policy.md
git show snapshot-baseline:01_CURRENT/output-policy.md
git show snapshot-approved-output:01_CURRENT/output-policy.md
```

Для просмотра без Git есть текстовые файлы в `HISTORY/DIFFS/`. Версии синтезированы из **точных файлов предыдущего handoff**, без предполагаемых промежуточных edit-коммитов.
