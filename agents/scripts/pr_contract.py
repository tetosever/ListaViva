#!/usr/bin/env python3
"""Check one-task/one-branch/one-PR metadata. This is not human approval."""
import json
import os
import re
from pathlib import Path


def check(event):
    pr = event.get('pull_request')
    if not pr:
        return []
    errors = []
    body = pr.get('body') or ''
    ids = re.findall(r'(?im)^Closes #([1-9][0-9]*)\s*$', body)
    if len(ids) != 1:
        return ['PR must contain exactly one standalone Closes #N line']
    # Reject additional closing directives, including alternative keywords and
    # qualified/URL references. The canonical standalone line is mandatory.
    closing_refs = re.findall(
        r'(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s*:?[ \t]+'
        r'(?:#[1-9][0-9]*|[\w.-]+/[\w.-]+#[1-9][0-9]*|https://github\.com/[^\s]+/issues/[1-9][0-9]*)',
        body,
    )
    if len(closing_refs) != 1:
        errors.append('PR must not contain additional issue-closing directives')
    branch = pr['head']['ref']
    setup = branch == 'chore/multi-agent-setup' and ids == ['1']
    if not setup and not re.fullmatch(r'(feat|fix|chore|docs)/' + ids[0] + r'-[a-z0-9][a-z0-9-]*', branch):
        errors.append('Branch must be <feat|fix|chore|docs>/<issue>-<slug> and match Closes #N')
    if pr['base']['ref'] != 'main':
        errors.append('Task PRs target main; agree stacked PR exceptions explicitly')
    for section in ('Problema e risultato', 'Scope', 'Verifiche', 'Limiti e rischi'):
        if f'## {section}' not in body:
            errors.append('Missing PR section: ' + section)
    return errors


def main():
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    errors = check(event)
    for error in errors:
        print(error)
    if not errors:
        print('PR metadata valid. Human review and manual merge remain required.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
