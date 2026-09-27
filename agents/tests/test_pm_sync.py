"""Offline tests: python -m unittest discover -s agents/tests -v."""
import copy
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import json

SPEC = importlib.util.spec_from_file_location('pm_sync', Path(__file__).resolve().parents[1] / 'scripts/pm_sync.py')
pm = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pm)


def catalog():
    tasks = []
    for n in (1, 2):
        tasks.append(dict(id=f'M1-0{n}', milestone='M1', title=f'Task {n}', kind='technical',
                          story='A measurable outcome', scope=['Included'], out_of_scope=['Excluded'],
                          acceptance=['Observable result'], dependencies=['M1-01'] if n == 2 else [],
                          owner='backend', priority='P1', estimate_days=2))
    return {'schema_version': 1, 'milestones': [dict(id='M1', title='Alpha', objective='Useful list', release='0.1',
                                gate='Usable', tasks=tasks)]}


class FakeClient:
    def __init__(self):
        self.milestones, self.issues, self.labels = [], [], []
        self.writes = []
        self.fail_tracking = False

    def pages(self, path):
        return copy.deepcopy(self.milestones if path.startswith('/milestones') else
                             self.issues if path.startswith('/issues') else self.labels)

    def request(self, method, path, data=None):
        if method == 'GET':
            return copy.deepcopy(next(i for i in self.issues if i['number'] == int(path.split('/')[-1])))
        if method == 'PATCH' and self.fail_tracking:
            self.fail_tracking = False
            raise RuntimeError('Simulated interruption')
        self.writes.append((method, path, copy.deepcopy(data)))
        if path == '/labels':
            self.labels.append(data)
            return data
        if path == '/milestones':
            obj = dict(data, number=len(self.milestones) + 1)
            self.milestones.append(obj)
            return copy.deepcopy(obj)
        if method == 'POST':
            obj = dict(data, number=len(self.issues) + 1, state='open')
            self.issues.append(obj)
            return copy.deepcopy(obj)
        obj = next(i for i in self.issues if i['number'] == int(path.split('/')[-1]))
        obj.update(data)
        return copy.deepcopy(obj)


class SyncTests(unittest.TestCase):
    def test_mutation_pacing_without_real_sleep(self):
        c = pm.Client('tetosever/ListaViva', 'never-used')
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b'{}'
        with patch.object(pm, 'urlopen', return_value=response) as network:
            with patch.object(pm.time, 'monotonic', side_effect=[10.0, 10.2, 11.1, 13.0, 13.0]):
                with patch.object(pm.time, 'sleep') as sleep:
                    c.request('POST', '/labels', {})
                    c.request('GET', '/labels')
                    c.request('PATCH', '/issues/1', {})
                    c.request('POST', '/labels', {})
                    self.assertEqual(sleep.call_count, 1)
                    self.assertAlmostEqual(sleep.call_args.args[0], 0.9)
                    self.assertEqual(network.call_count, 4)

    def test_validation_rejects_malformed_task_fields(self):
        bad = [('title', ' '), ('story', None), ('scope', ['']), ('scope', []),
               ('out_of_scope', []), ('acceptance', [4]), ('dependencies', ['M1-01', 'M1-01']),
               ('owner', 'unknown'), ('kind', 'bug'), ('priority', 'P3'),
               ('estimate_days', True), ('estimate_days', 4), ('estimate_days', 1.5)]
        for field, value in bad:
            with self.subTest(field=field, value=value):
                data = catalog()
                data['milestones'][0]['tasks'][1][field] = value
                with self.assertRaises(ValueError):
                    pm.validate(data)

    def test_validation_rejects_schema_and_milestone_fields(self):
        for value in (None, True, 2, '1'):
            data = catalog()
            data['schema_version'] = value
            with self.assertRaises(ValueError):
                pm.validate(data)
        for field in ('id', 'title', 'objective', 'release', 'gate'):
            data = catalog()
            data['milestones'][0][field] = ''
            with self.assertRaises(ValueError):
                pm.validate(data)

    def test_all_status_labels_and_validation_branch(self):
        data = catalog()
        data['milestones'][0]['tasks'][0]['kind'] = 'validation'
        c = FakeClient()
        pm.sync(c, data)
        statuses = {label['name'] for label in c.labels if label['name'].startswith('status:')}
        self.assertEqual(statuses, {'status:backlog', 'status:ready', 'status:in-progress',
                                    'status:in-review', 'status:blocked', 'status:done'})
        self.assertIn('docs/1-m1-01', c.issues[0]['body'])

    def test_idempotent_preserves_human_scope_and_closed_state(self):
        c = FakeClient()
        pm.sync(c, catalog())
        c.issues[0]['body'] = c.issues[0]['body'].replace('Included', 'Human adjusted scope') + '\nHuman notes'
        c.issues[0]['state'] = 'closed'
        before = len(c.writes)
        pm.sync(c, catalog())
        self.assertEqual(len(c.writes), before)
        self.assertEqual(len(c.issues), 2)
        self.assertIn('Human adjusted scope', c.issues[0]['body'])
        self.assertTrue(c.issues[0]['body'].endswith('Human notes'))
        self.assertEqual(c.issues[0]['state'], 'closed')
        self.assertIn('M1-01: #1', c.issues[1]['body'])

    def test_interrupted_sync_does_not_duplicate(self):
        c = FakeClient()
        c.fail_tracking = True
        with self.assertRaises(RuntimeError):
            pm.sync(c, catalog())
        pm.sync(c, catalog())
        self.assertEqual(len(c.issues), 2)
        self.assertEqual(len(c.milestones), 1)
        self.assertIn('Closes #2', c.issues[1]['body'])

    def test_invalid_block_stops_before_writing(self):
        c = FakeClient()
        pm.sync(c, catalog())
        c.issues[0]['body'] = c.issues[0]['body'].replace(pm.END, '')
        count = len(c.writes)
        with self.assertRaises(ValueError):
            pm.sync(c, catalog())
        self.assertEqual(len(c.writes), count)

    def test_duplicate_remote_marker_rejected(self):
        c = FakeClient()
        pm.sync(c, catalog())
        c.issues.append(copy.deepcopy(c.issues[0]))
        with self.assertRaises(ValueError):
            pm.sync(c, catalog())

    def test_dependency_cycle_rejected(self):
        data = catalog()
        data['milestones'][0]['tasks'][0]['dependencies'] = ['M1-02']
        with self.assertRaises(ValueError):
            pm.validate(data)

    def test_pagination(self):
        c = pm.Client('tetosever/ListaViva', 'never-used')
        with patch.object(c, 'request', side_effect=[list(range(100)), [100]]) as request:
            self.assertEqual(len(list(c.pages('/issues?state=all'))), 101)
            self.assertEqual(request.call_args_list[1].args[1], '/issues?state=all&per_page=100&page=2')

    def test_dry_run_no_token_no_network(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'catalog.json'
            path.write_text(json.dumps(catalog()))
            with patch.object(pm, 'Client', side_effect=AssertionError('network forbidden')):
                with patch.object(pm.os, 'environ', {}):
                    self.assertEqual(pm.main(['--catalog', str(path)]), 0)


if __name__ == '__main__':
    unittest.main()
