#!/usr/bin/env python3
"""Check that AIR's current-tree artifact set is self-contained and lean."""
from __future__ import annotations
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
errors = []
links_checked = 0
for p in files:
    rel = p.relative_to(root)
    if p.suffix not in {'.md', '.patch', '.py'} and p.name not in {'.gitignore', 'SHA256SUMS'}:
        errors.append(f'unexpected artifact: {rel}')
    if p.suffix != '.md':
        continue
    content = p.read_text(encoding='utf-8')
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        cleaned = target.split('#', 1)[0]
        if not cleaned or cleaned.startswith('sandbox:'):
            continue
        links_checked += 1
        if not (p.parent / cleaned).exists():
            errors.append(f'broken link: {rel} -> {target}')

for f in sorted((root / 'proposals').glob('*.patch')):
    r = subprocess.run(['patch', '--dry-run', '-p1'], cwd=root,
                       input=f.read_bytes(), stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
    if r.returncode:
        errors.append(f'unapplicable proposal: {f.name}: {r.stdout.decode(errors="replace")[-240:]}')

unwanted = sorted(str(p.relative_to(root)) for p in files
                  if p.suffix.lower() in {'.jsonl', '.7z', '.zip', '.pdf', '.png', '.jpg', '.log'})
errors += [f'redundant/raw evidence present: {p}' for p in unwanted]
required = [root / 'README.md', *(root / 'docs' / f'{n:02d}_{name}_RU.md' for n, name in [])]
assert (root/'README.md').exists()
print(f'Checked {len(files)} worktree files, {links_checked} relative links, '
      f'{len(list((root / "proposals").glob("*.patch")))} patch dry-runs.')
if errors:
    print('\n'.join(f'ERROR {e}' for e in errors), file=sys.stderr)
    raise SystemExit(1)
print('PASS: links, patch applicability, no raw evidence in current tree.')
