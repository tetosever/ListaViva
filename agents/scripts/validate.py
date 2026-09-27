#!/usr/bin/env python3
"""Validate repository agent configuration and backlog without network access."""
import json
import re
import sys
import tomllib
from pathlib import Path

from pm_sync import validate

ROOT = Path(__file__).resolve().parents[2]
ROLES = {'orchestrator', 'pm', 'backend', 'mobile', 'data-sync', 'quality'}


def main():
    errors = []
    try:
        catalog = json.loads((ROOT / 'agents/backlog/catalog.json').read_text())
        milestones, tasks = validate(catalog)
        if {m['id'] for m in milestones} != {f'M{i}' for i in range(1, 7)}:
            errors.append('Expected the six roadmap milestones M1–M6')
        cfg = tomllib.loads((ROOT / '.codex/config.toml').read_text())
        if cfg['agents'].get('max_concurrent_threads_per_session') != 3:
            errors.append('Expected concurrency cap of three subagents')
        for role in ROLES:
            path = ROOT / f'.codex/agents/{role}.toml'
            cfg = tomllib.loads(path.read_text())
            if cfg.get('name') != role.replace('-', '_'):
                errors.append(f'{path}: invalid custom agent name')
            if not cfg.get('description') or not cfg.get('developer_instructions'):
                errors.append(f'{path}: missing agent instructions')
            role_path = f'agents/roles/{role}.md'
            if role_path not in cfg['developer_instructions'] or not (ROOT / role_path).is_file():
                errors.append(f'{path}: missing role reference')
        skill_files = list((ROOT / 'agents/skills').glob('*/SKILL.md'))
        if not skill_files:
            errors.append('Missing repository skills')
        for skill in skill_files:
            content = skill.read_text()
            match = re.match(r'\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n', content)
            if not match or match[1] != skill.parent.name:
                errors.append(f'{skill}: invalid name/description frontmatter')
        docs = [ROOT / 'AGENTS.md', ROOT / 'README.md'] + list((ROOT / 'agents').rglob('*.md'))
        for doc in docs:
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', doc.read_text()):
                if '://' in target or target.startswith('#'):
                    continue
                target = target.split('#')[0]
                if not (doc.parent / target).exists():
                    errors.append(f'{doc.relative_to(ROOT)}: broken link {target}')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        errors.append(str(exc))
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Valid: {len(ROLES)} roles, {len(skill_files)} skills, {len(milestones)} milestones, {len(tasks)} tasks.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
