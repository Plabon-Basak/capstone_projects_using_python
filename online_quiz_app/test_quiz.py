import unittest

from questions import QuestionBank
from quiz import QuizSession


class QuestionBankTest(unittest.TestCase):
    def test_has_three_questions(self):
        self.assertEqual(len(QuestionBank().all()), 3)

    def test_first_question_correct_answer(self):
        self.assertEqual(QuestionBank().all()[0].correct_answer, "def")


class QuizSessionTest(unittest.TestCase):
    def setUp(self):
        self.bank = QuestionBank()
        self.session = QuizSession(self.bank.all(), "Arjun")

    def test_submit_accepted(self):
        response = self.session.submit(1, "def")
        self.assertTrue(response["accepted"])
        self.assertEqual(response["question_id"], 1)

    def test_submit_unknown_question_raises(self):
        with self.assertRaises(LookupError):
            self.session.submit(99, "def")

    def test_submit_invalid_option_raises(self):
        with self.assertRaises(ValueError):
            self.session.submit(1, "int")

    def test_results_score_all_correct(self):
        for question_id, answer in [(1, "def"), (2, "set"), (3, "3")]:
            self.session.submit(question_id, answer)
        results = self.session.results()
        self.assertEqual(results["score"], 3)
        self.assertEqual(results["percentage"], 100.0)

    def test_results_detail_flags_correctness(self):
        self.session.submit(1, "class")
        details = self.session.results()["details"]
        self.assertFalse(details[0]["correct"])
        self.assertEqual(details[0]["correct_answer"], "def")


if __name__ == "__main__":
    unittest.main()