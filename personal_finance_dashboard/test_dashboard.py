import unittest

from accounts import AccountService
from dashboard import DashboardService
from transactions import TransactionService


class AccountServiceTest(unittest.TestCase):
    def test_list_returns_all_accounts(self):
        accounts = AccountService()
        self.assertEqual(len(accounts.list()), 3)
        account_names = {account.name for account in accounts.list()}
        self.assertIn("Everyday Checking", account_names)

    def test_get_known_account(self):
        self.assertEqual(AccountService().get(102).name, "Emergency Savings")

    def test_get_unknown_account_raises(self):
        with self.assertRaises(LookupError):
            AccountService().get(999)

    def test_net_worth_sums_balances(self):
        self.assertEqual(AccountService().net_worth(), 15350.00)


class TransactionServiceTest(unittest.TestCase):
    def setUp(self):
        self.accounts = AccountService()
        self.transactions = TransactionService(self.accounts)

    def test_add_credit_updates_balance(self):
        before = self.accounts.get(101).balance
        self.transactions.add(101, "Salary", "Income", 2500.00)
        self.assertEqual(self.accounts.get(101).balance, before + 2500.00)

    def test_add_debit_updates_balance(self):
        before = self.accounts.get(101).balance
        self.transactions.add(101, "Groceries", "Food", -120.50)
        self.assertEqual(self.accounts.get(101).balance, round(before - 120.50, 2))

    def test_amount_zero_raises(self):
        with self.assertRaises(ValueError):
            self.transactions.add(101, "Testing", "Other", 0)

    def test_blank_description_raises(self):
        with self.assertRaises(ValueError):
            self.transactions.add(101, "  ", "Other", -10)


class DashboardServiceTest(unittest.TestCase):
    def setUp(self):
        self.accounts = AccountService()
        self.transactions = TransactionService(self.accounts)

    def test_summary_income_expenses_and_cash_flow(self):
        self.transactions.add(101, "Salary", "Income", 3000)
        self.transactions.add(101, "Rent", "Housing", -1200)
        self.transactions.add(101, "Groceries", "Food", -200)
        summary = DashboardService(self.accounts, self.transactions).summary(
            {"Food": 250}
        )
        self.assertEqual(summary["monthly_income"], 3000.0)
        self.assertEqual(summary["monthly_expenses"], 1400.0)
        self.assertEqual(summary["monthly_cash_flow"], 1600.0)
        self.assertEqual(summary["spending_by_category"]["Food"], 200.0)

    def test_summary_savings_rate(self):
        self.transactions.add(101, "Salary", "Income", 2000)
        self.transactions.add(101, "Groceries", "Food", -500)
        summary = DashboardService(self.accounts, self.transactions).summary({})
        self.assertEqual(summary["savings_rate_percent"], 75.0)

    def test_budget_status_reports_over_budget(self):
        self.transactions.add(101, "Groceries", "Food", -300)
        summary = DashboardService(self.accounts, self.transactions).summary(
            {"Food": 250}
        )
        status = summary["budget_status"][0]
        self.assertEqual(status["status"], "over budget")
        self.assertEqual(status["remaining"], -50.0)


if __name__ == "__main__":
    unittest.main()