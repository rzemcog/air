#!/usr/bin/env python3
"""Validate AIR Markdown package, committed skill patch and historical proposals."""
from __future__ import annotations
from pathlib import Path
import io
import hashlib
import re
import subprocess
import sys
import tarfile
import tempfile

root = Path(__file__).resolve().parents[1]
files = [p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts]
errors: list[str] = []
links_checked = 0
for p in files:
    rel = p.relative_to(root)
    if p.suffix not in {'.md', '.patch', '.py', '.css', '.js'} and p.name not in {'.gitignore', 'SHA256SUMS'}:
        errors.append(f'unexpected artifact: {rel}')
    if p.suffix != '.md':
        continue
    content = p.read_text(encoding='utf-8')
    if p.relative_to(root).as_posix().startswith(('docs/',)) or p.name == 'README.md':
        expected_style = './docs/air.css' if p.parent == root else './air.css'
        expected_script = './docs/air.js' if p.parent == root else './air.js'
        if f'<!-- @style: {expected_style} -->' not in content or f'<!-- @script: {expected_script} -->' not in content:
            errors.append(f'MdStyled reference missing: {rel}')
        for asset in (expected_style, expected_script):
            if not (p.parent / asset).exists(): errors.append(f'visual asset missing: {rel} -> {asset}')
        if re.search(r'(?m)^\s*<style(?:\s|>)', content) or re.search(r'<(?:div|span|section|article|p|header|a)\b[^>]*\sstyle\s*=', content):
            errors.append(f'inline CSS is forbidden in AIR documentation: {rel}')
        if re.search(r'data-air-[\w-]+=', content):
            errors.append(f'MdStyled sanitizer strips data-air-* attributes: {rel}')
    for target in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)', content):
        if target.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        cleaned = target.split('#', 1)[0]
        if not cleaned or cleaned.startswith('sandbox:'):
            continue
        links_checked += 1
        if not (p.parent / cleaned).exists():
            errors.append(f'broken link: {rel} -> {target}')

# These seven proposals remain *unapplied* and were authored for the older tree.
# Verify them against their historical source revision, never against current docs.
proposals = sorted((root / 'proposals').glob('*.patch'))
with tempfile.TemporaryDirectory(prefix='air-baseline-') as t:
    archive = subprocess.run(['git', 'archive', '--format=tar', '4cbd0c7'],
                             cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if archive.returncode:
        errors.append(f'cannot read historical proposal baseline: {archive.stderr.decode(errors="replace")}')
    else:
        with tarfile.open(fileobj=io.BytesIO(archive.stdout), mode='r:') as tar:
            tar.extractall(t, filter='data')
        for f in proposals:
            r = subprocess.run(['patch', '--dry-run', '-p1'], cwd=t,
                               input=f.read_bytes(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if r.returncode:
                errors.append(f'unapplicable historical proposal: {f.name}: {r.stdout.decode(errors="replace")[-240:]}')

# Documentation workflow and handoff must be discoverable and current.
for wanted in ['HANDOFF_CURRENT_RU.md', 'skills/mdstyled-documentation/SKILL.md', 'docs/MDSTYLED_INTEGRATION_NOTES_RU.md']:
    if not (root / wanted).is_file():
        errors.append(f'missing MdStyled workflow/handoff: {wanted}')
if (root / 'docs/mdstyled.config.json').exists():
    errors.append('duplicated MdStyled config (prefer @style/@script only)')
# MdStyled supports @page and creates an optional nested root. Do not ban it.
css_text = (root / 'docs/air.css').read_text(encoding='utf-8')
if '.mdstyled-root.air-docs' in css_text:
    errors.append('CSS incorrectly targets .mdstyled-root.air-docs')
if '--air-root-css-ready:1' not in css_text or '.mdstyled-root {' not in css_text:
    errors.append('MdStyled root CSS probe missing')
probe_text = (root / 'docs/00_RENDER_TEST_RU.md').read_text(encoding='utf-8')
for probe_id in ['air-js-status', 'air-css-status', 'air-renderer-status', 'air-root-status']:
    if f'id="{probe_id}"' not in probe_text:
        errors.append(f'MdStyled probe missing: {probe_id}')
# No underhanded rewrite of core policies through an unreviewed artifact.
skill = (root / 'skills/instruction-conflict-resolution/SKILL.md').read_text('utf-8')
if '../../shared/agent-policy.md' in skill:
    errors.append('skill still contains a hardcoded relative Shared Policy location')
if 'host' not in skill.lower() or 'Shared Policy' not in skill:
    errors.append('skill must use host-provided Shared Policy')
if (root / 'docs/05_IMPLEMENTATION_TZ_RU.md').exists():
    errors.append('obsolete combined TZ still present')
for wanted in ['05_EXPERIMENTAL_TZ_RU.md', '10_IMPLEMENTATION_DRAFT_TZ_RU.md']:
    if not (root / 'docs' / wanted).exists():
        errors.append(f'missing separated TZ {wanted}')
exp = (root / 'docs/05_EXPERIMENTAL_TZ_RU.md').read_text('utf-8')
if len(re.findall(r'\| H\d+\.', exp)) != 24:
    errors.append('H1-H24 branch map incomplete')
if not all(re.search(rf'\bR{i}(?:[ .])', exp) for i in range(1,10)):
    errors.append('R1-R9 experiment set incomplete')

# Integrity manifest covers every working file apart from itself.
manifest = root / 'SHA256SUMS'
if manifest.exists():
    actual_lines = [f'{hashlib.sha256(f.read_bytes()).hexdigest()}  {f.relative_to(root).as_posix()}'
                    for f in sorted(files, key=lambda x: x.relative_to(root).as_posix())
                    if f != manifest]
    expected_lines = manifest.read_text('utf-8').strip().splitlines()
    if expected_lines != actual_lines:
        errors.append('SHA256SUMS is missing files or does not match current working tree')
else:
    errors.append('SHA256SUMS missing')

unwanted = sorted(str(p.relative_to(root)) for p in files
                  if p.suffix.lower() in {'.jsonl', '.7z', '.zip', '.pdf', '.png', '.jpg', '.log'})
errors += [f'redundant/raw evidence present: {p}' for p in unwanted]
print(f'Checked {len(files)} files, {links_checked} local Markdown links, '
      f'{len(proposals)} historical patch dry-runs, skill loading constraints, R1–R9/H1–H24.')
if errors:
    print('\n'.join(f'ERROR {e}' for e in errors), file=sys.stderr)
    raise SystemExit(1)
print('PASS: links, baseline patches, applied skill contract, split specs, no raw evidence.')
