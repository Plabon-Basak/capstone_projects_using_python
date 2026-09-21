import re


class SupportChatbot:
    def __init__(self, articles, tickets):
        self.articles, self.tickets = articles, tickets

    def reply(self, message):
        words = set(re.findall(r"[a-z]+", message.lower()))
        ranked = []
        for intent, article in self.articles.items():
            matched = len(words & article["keywords"])
            ranked.append(
                (matched, matched / max(len(article["keywords"]), 1), intent, article)
            )
        score, _, intent, article = max(ranked, key=lambda item: item[:2])
        confidence = round(score / max(len(words), 1), 2)
        if score == 0:
            ticket = self.tickets.create(message, "No matching knowledge article")
            return {
                "intent": "unknown",
                "confidence": 0,
                "reply": "I could not resolve that request, so I created a support ticket.",
                "escalated": True,
                "ticket": ticket,
            }
        return {
            "intent": intent,
            "confidence": confidence,
            "reply": article["answer"],
            "escalated": False,
        }
