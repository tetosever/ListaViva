import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from pr_contract import check


class ContractTests(unittest.TestCase):
    def event(self, branch='feat/23-invites', closes='Closes #23'):
        return {'pull_request': {'head': {'ref': branch}, 'base': {'ref': 'main'},
                'body': closes + '\n## Problema e risultato\nX\n## Scope\nX\n## Verifiche\nX\n## Limiti e rischi\nX'}}

    def test_issue_matches_branch(self):
        self.assertEqual(check(self.event()), [])
        self.assertTrue(check(self.event(branch='feat/24-invites')))

    def test_one_issue_only(self):
        self.assertTrue(check(self.event(closes='Closes #23\nCloses #24')))
        self.assertTrue(check(self.event(closes='Closes #NUMERO')))

    def test_additional_closing_keywords_rejected(self):
        for directive in ('Fixes #24', 'Resolves owner/repo#24',
                          'Fixed https://github.com/owner/repo/issues/24',
                          'Closes: #24'):
            self.assertTrue(check(self.event(closes='Closes #23\n' + directive)))

    def test_bootstrap_exception_is_scoped(self):
        self.assertEqual(check(self.event('chore/multi-agent-setup', 'Closes #1')), [])
        self.assertTrue(check(self.event('chore/multi-agent-setup', 'Closes #23')))

    def test_missing_evidence_section(self):
        event = self.event()
        event['pull_request']['body'] = event['pull_request']['body'].replace('## Verifiche', '## Test')
        self.assertTrue(check(event))


if __name__ == '__main__':
    unittest.main()
