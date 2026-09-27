#!/usr/bin/env python3
"""Publish ListaViva's backlog. Default dry-run never accesses network or tokens."""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

START = '<!-- listaviva:tracking:start -->'
END = '<!-- listaviva:tracking:end -->'
DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'backlog/catalog.json'


class Client:
    def __init__(self, repo, token):
        self.base = 'https://api.github.com/repos/' + repo
        self.token = token
        self.last_mutation = None

    def request(self, method, path, data=None):
        if method not in {'GET', 'HEAD', 'OPTIONS'}:
            # Pace content writes conservatively, including after failed requests.
            # No automatic retries: a POST may have succeeded before a timeout.
            if self.last_mutation is not None:
                remaining = 1.1 - (time.monotonic() - self.last_mutation)
                if remaining > 0:
                    time.sleep(remaining)
            self.last_mutation = time.monotonic()
        request = Request(self.base + path, method=method,
                          data=json.dumps(data).encode() if data is not None else None,
                          headers={'Authorization': 'Bearer ' + self.token,
                                   'Accept': 'application/vnd.github+json',
                                   'Content-Type': 'application/json',
                                   'X-GitHub-Api-Version': '2022-11-28',
                                   'User-Agent': 'ListaViva-PM'})
        try:
            with urlopen(request, timeout=30) as response:
                raw = response.read()
                return json.loads(raw) if raw else None
        except HTTPError as error:
            # Never print request headers, token, or API response body.
            raise RuntimeError(f'GitHub {method} {path}: HTTP {error.code}. '
                               'No automatic retry; rerun to reconcile remote state.') from None
        except (URLError, TimeoutError):
            raise RuntimeError('GitHub connection failed. No automatic retry; '
                               'rerun to reconcile remote state.') from None

    def pages(self, path):
        page = 1
        while True:
            rows = self.request('GET', path + ('&' if '?' in path else '?') +
                                f'per_page=100&page={page}')
            yield from rows
            if len(rows) < 100:
                break
            page += 1


def validate(catalog):
    if not isinstance(catalog, dict) or type(catalog.get('schema_version')) is not int or catalog['schema_version'] != 1:
        raise ValueError('schema_version must be 1')
    milestones = catalog['milestones']
    if not isinstance(milestones, list) or not milestones:
        raise ValueError('milestones must be a nonempty list')

    def string(value):
        return isinstance(value, str) and bool(value.strip())

    def string_fields(obj, fields, context):
        for field in fields:
            if not string(obj.get(field)):
                raise ValueError(f'{context}: {field} must be a nonempty string')

    ids = set()
    mids = set()
    for milestone in milestones:
        if not isinstance(milestone, dict):
            raise ValueError('Each milestone must be an object')
        for field in ('id', 'title', 'objective', 'release', 'gate', 'tasks'):
            if field not in milestone:
                raise ValueError(f'Milestone missing {field}')
        string_fields(milestone, ('id', 'title', 'objective', 'release', 'gate'), 'Milestone')
        mid = milestone['id']
        if not re.fullmatch(r'M[1-9][0-9]*', mid) or mid in mids:
            raise ValueError('Invalid or duplicate milestone ID')
        mids.add(mid)
        if not isinstance(milestone['tasks'], list) or not milestone['tasks']:
            raise ValueError(f'{mid} must contain tasks')
        for task in milestone['tasks']:
            if not isinstance(task, dict):
                raise ValueError('Each task must be an object')
            for field in ('id', 'milestone', 'title', 'kind', 'story', 'scope',
                          'out_of_scope', 'acceptance', 'dependencies', 'owner',
                          'priority', 'estimate_days'):
                if field not in task:
                    raise ValueError(f'Task missing {field}')
            string_fields(task, ('id', 'milestone', 'title', 'kind', 'story', 'owner', 'priority'), 'Task')
            tid = task['id']
            if not re.fullmatch(re.escape(mid) + r'-[0-9]+', tid) or tid in ids:
                raise ValueError('Invalid or duplicate task ID')
            if task['milestone'] != mid:
                raise ValueError(f'{tid}: milestone mismatch')
            for field in ('scope', 'out_of_scope', 'acceptance', 'dependencies'):
                if not isinstance(task[field], list) or not all(string(v) for v in task[field]):
                    raise ValueError(f'{tid}: {field} must be a list of nonempty strings')
            if any(not task[field] for field in ('scope', 'out_of_scope', 'acceptance')):
                raise ValueError(f'{tid}: scope, out_of_scope and acceptance required')
            if len(set(task['dependencies'])) != len(task['dependencies']):
                raise ValueError(f'{tid}: duplicate dependencies')
            if task['owner'] not in {'pm', 'orchestrator', 'backend', 'mobile', 'data-sync', 'quality'}:
                raise ValueError(f'{tid}: unknown owner')
            if task['kind'] not in {'user-story', 'technical', 'validation'}:
                raise ValueError(f'{tid}: unknown kind')
            if task['priority'] not in {'P0', 'P1', 'P2'}:
                raise ValueError(f'{tid}: unknown priority')
            if type(task['estimate_days']) is not int or not 1 <= task['estimate_days'] <= 3:
                raise ValueError(f'{tid}: estimate_days must be an integer from 1 to 3')
            ids.add(tid)
    tasks = {t['id']: t for m in milestones for t in m['tasks']}
    visiting, visited = set(), set()

    def walk(tid):
        if tid in visiting:
            raise ValueError('Cyclic task dependencies')
        if tid in visited:
            return
        visiting.add(tid)
        for dep in tasks[tid]['dependencies']:
            if dep not in ids:
                raise ValueError(f'{tid}: unknown dependency {dep}')
            walk(dep)
        visiting.remove(tid)
        visited.add(tid)
    for tid in tasks:
        walk(tid)
    return milestones, tasks


def bullets(values, checkbox=False):
    if isinstance(values, str):
        values = [values]
    return '\n'.join(('- [ ] ' if checkbox else '- ') + str(v) for v in values) or '- Nessuna.'


def task_marker(tid):
    return f'<!-- listaviva:task:{tid} -->'


def issue_body(task):
    return (f"{task_marker(task['id'])}\n\n## User story / risultato\n\n{task['story']}\n\n"
            f"## Scope\n\n{bullets(task['scope'])}\n\n## Fuori scope\n\n{bullets(task['out_of_scope'])}\n\n"
            f"## Criteri di accettazione\n\n{bullets(task['acceptance'], True)}\n\n"
            '## Verifica\n\nDimostrare ogni criterio con test mirati o evidenza manuale; '
            'riportare comandi, risultati e limiti nella PR.\n\n'
            f"## Pianificazione\n\nTipo: {task['kind']}; owner operativo: {task['owner']}; "
            f"priorità: {task['priority']}; stima indicativa: {task['estimate_days']} giorni.\n\n"
            'Stato iniziale: Backlog. Lo stato corrente è indicato dalle label status:*. '
            'Done richiede merge; approvazione e merge restano al proprietario.\n\n'
            f'{START}\nTracking da riconciliare al termine della pubblicazione.\n{END}\n')


def replace_tracking(body, text):
    if body.count(START) != 1 or body.count(END) != 1 or body.index(END) < body.index(START):
        raise ValueError('Invalid tracking block; fix manually before rerunning')
    before, rest = body.split(START)
    _, after = rest.split(END)
    return before + START + '\n' + text + '\n' + END + after


def sync(client, catalog):
    milestones, tasks = validate(catalog)
    remote_m = list(client.pages('/milestones?state=all'))
    remote_i = [i for i in client.pages('/issues?state=all') if 'pull_request' not in i]
    known = {}
    for tid in tasks:
        matches = [i for i in remote_i if task_marker(tid) in (i.get('body') or '')]
        if len(matches) > 1:
            raise ValueError(f'Duplicate remote marker for {tid}; resolve manually')
        if matches:
            known[tid] = matches[0]
            # Validate all existing blocks before making any mutation.
            replace_tracking(matches[0].get('body') or '', '')
    mapped_m = {}
    for m in milestones:
        marker = f"<!-- listaviva:milestone:{m['id']} -->"
        matches = [x for x in remote_m if marker in (x.get('description') or '')]
        if len(matches) > 1:
            raise ValueError(f"Duplicate milestone marker {m['id']}")
        mapped_m[m['id']] = matches[0] if matches else None
    labels = {x['name'] for x in client.pages('/labels')}
    required = {f'status:{s}' for s in ('backlog', 'ready', 'in-progress', 'in-review', 'blocked', 'done')} | {f"area:{t['owner']}" for t in tasks.values()} | {
        f"priority:{t['priority']}" for t in tasks.values()}
    for label in sorted(required - labels):
        client.request('POST', '/labels', {'name': label, 'color': '64748b'})
    for m in milestones:
        if mapped_m[m['id']] is None:
            mapped_m[m['id']] = client.request('POST', '/milestones', {
                'title': f"{m['id']} · {m['title']}",
                'description': f"<!-- listaviva:milestone:{m['id']} -->\n\n"
                               f"{m['objective']}\n\nRelease: {m['release']}\n\nGate:\n{bullets(m['gate'])}"})
        for t in m['tasks']:
            if t['id'] not in known:
                known[t['id']] = client.request('POST', '/issues', {
                    'title': f"[{t['id']}] {t['title']}", 'body': issue_body(t),
                    'milestone': mapped_m[m['id']]['number'],
                    'labels': ['status:backlog', f"area:{t['owner']}", f"priority:{t['priority']}"]})
    for tid, task in tasks.items():
        issue = known[tid]
        # Fetch immediately before PATCH to preserve user edits made since listing.
        current = client.request('GET', f"/issues/{issue['number']}")
        dependency_lines = [f"- {dep}: #{known[dep]['number']}" for dep in task['dependencies']]
        prefix = {'validation': 'docs', 'technical': 'chore', 'user-story': 'feat'}[task['kind']]
        tracking = ('### Dipendenze\n\n' + ('\n'.join(dependency_lines) or '- Nessuna.') +
                    f"\n\nBranch al momento dell'avvio: `{prefix}/{issue['number']}-{tid.lower()}`.\n"
                    f"PR: `Closes #{issue['number']}`. Una issue, un branch, una PR; "
                    'nessun branch anticipato. Approvazione e merge manuali del proprietario.')
        body = replace_tracking(current.get('body') or '', tracking)
        if body != current.get('body'):
            client.request('PATCH', f"/issues/{issue['number']}", {'body': body})
    return known


def status(client, catalog):
    milestones, tasks = validate(catalog)
    issues = [i for i in client.pages('/issues?state=all') if 'pull_request' not in i]
    for m in milestones:
        counts = {}
        for t in m['tasks']:
            found = [i for i in issues if task_marker(t['id']) in (i.get('body') or '')]
            if len(found) > 1:
                raise ValueError(f"Duplicate remote marker {t['id']}")
            if not found:
                state = 'non pubblicata'
            elif found[0]['state'] == 'closed':
                state = 'chiusa (merge da verificare)'
            else:
                states = [l['name'] for l in found[0]['labels'] if l['name'].startswith('status:')]
                state = states[0] if len(states) == 1 else 'stato da verificare'
            counts[state] = counts.get(state, 0) + 1
        print(m['id'] + ': ' + json.dumps(counts, ensure_ascii=False))
    print('Issue chiuse e label Done non certificano il merge né il raggiungimento degli OKR.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    parser.add_argument('--repo', default='tetosever/ListaViva')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--status', action='store_true')
    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-]+', args.repo):
            raise ValueError('Repository must have owner/name format')
        catalog = json.loads(args.catalog.read_text())
        milestones, tasks = validate(catalog)
        if not args.apply and not args.status:
            print(f'DRY RUN: {args.repo}; {len(milestones)} milestones; {len(tasks)} issues. No network access.')
            for m in milestones:
                print(f"{m['id']}: {m['title']} ({len(m['tasks'])} tasks)")
            return 0
        token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
        if not token:
            raise ValueError('Set GH_TOKEN or GITHUB_TOKEN in the environment')
        client = Client(args.repo, token)
        if args.status:
            status(client, catalog)
        else:
            known = sync(client, catalog)
            print(f'Reconciled {len(known)} issues on {args.repo}. No branches, PRs or merges created.')
        return 0
    except (ValueError, KeyError, TypeError, OSError, RuntimeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
