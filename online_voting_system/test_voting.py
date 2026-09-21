import unittest

from audit import AuditLog
from elections import ElectionService
from voting import VotingService


class VotingServiceTest(unittest.TestCase):
    def setUp(self):
        self.elections = ElectionService()
        self.audit = AuditLog()
        self.voting = VotingService(self.elections, self.audit)

    def test_cast_tallies_and_returns_receipt(self):
        response = self.voting.cast(101, "TOKEN-A1", "Ava Patel")
        self.assertEqual(response["message"], "Vote accepted")
        self.assertEqual(len(response["receipt"]), 12)
        self.assertEqual(self.elections.get(101).candidates["Ava Patel"], 1)

    def test_duplicate_vote_raises(self):
        self.voting.cast(101, "TOKEN-A1", "Ava Patel")
        with self.assertRaises(ValueError):
            self.voting.cast(101, "TOKEN-A1", "Ava Patel")

    def test_invalid_token_raises(self):
        with self.assertRaises(PermissionError):
            self.voting.cast(101, "FAKE", "Ava Patel")

    def test_unknown_candidate_raises(self):
        with self.assertRaises(ValueError):
            self.voting.cast(101, "TOKEN-B2", "Nobody")

    def test_unknown_election_raises(self):
        with self.assertRaises(LookupError):
            self.voting.cast(999, "TOKEN-A1", "Ava Patel")

    def test_results_total_matches_votes(self):
        self.voting.cast(101, "TOKEN-A1", "Ava Patel")
        self.voting.cast(101, "TOKEN-B2", "Noah Smith")
        results = self.voting.results(101)
        self.assertEqual(results["total_votes"], 2)
        self.assertEqual(results["votes"]["Ava Patel"], 1)

    def test_audit_log_records_hashed_events(self):
        self.voting.cast(101, "TOKEN-A1", "Ava Patel")
        self.assertEqual(len(self.audit.events), 1)
        event = self.audit.events[0]
        self.assertEqual(event["candidate"], "Ava Patel")
        self.assertNotEqual(event["voter_hash"], "TOKEN-A1")


if __name__ == "__main__":
    unittest.main()