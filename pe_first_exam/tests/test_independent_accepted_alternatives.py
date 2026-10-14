import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from publish_authored_batch import independent_comparison


class AcceptedAlternatives(unittest.TestCase):
    def test_official_reordered_alternatives(self):
        self.assertEqual(independent_comparison('3|4', '4|3', 'multiple_accepted'),
                         'matches_official_draft')

    def test_one_accepted_solve_is_not_the_whole_set(self):
        self.assertEqual(independent_comparison('4', '4|3', 'multiple_accepted'),
                         'accepted_official_member_draft')

    def test_unaccepted_option_remains_discrepancy(self):
        self.assertEqual(independent_comparison('2', '4|3', 'multiple_accepted'),
                         'discrepancy_pending')

    def test_no_inference_of_multiple_kind(self):
        self.assertEqual(independent_comparison('4', '4|3', 'single'),
                         'discrepancy_pending')

    def test_all_correct_does_not_claim_an_independent_set(self):
        self.assertEqual(independent_comparison('4', '1|2|3|4|5', 'all_correct'),
                         'discrepancy_pending')
