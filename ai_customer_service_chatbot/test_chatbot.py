import unittest

from chatbot import SupportChatbot
from knowledge_base import ARTICLES
from tickets import TicketService


class SupportChatbotTest(unittest.TestCase):
    def setUp(self):
        self.tickets = TicketService()
        self.bot = SupportChatbot(ARTICLES, self.tickets)

    def test_matches_order_status_intent(self):
        response = self.bot.reply("Where can I track my order status?")
        self.assertEqual(response["intent"], "order_status")
        self.assertFalse(response["escalated"])
        self.assertGreater(response["confidence"], 0)

    def test_matches_returns_intent(self):
        response = self.bot.reply("I need to return an item for a refund.")
        self.assertEqual(response["intent"], "returns")
        self.assertEqual(response["reply"], ARTICLES["returns"]["answer"])

    def test_unknown_query_escalates_and_creates_ticket(self):
        response = self.bot.reply("My device arrived with a cracked screen.")
        self.assertTrue(response["escalated"])
        self.assertEqual(response["intent"], "unknown")
        self.assertEqual(response["confidence"], 0)
        self.assertEqual(response["ticket"]["status"], "open")
        self.assertEqual(len(self.tickets.tickets), 1)

    def test_tie_broken_toward_more_specific_intent(self):
        response = self.bot.reply("return order")
        self.assertEqual(response["intent"], "returns")


if __name__ == "__main__":
    unittest.main()