import unittest

from kitchen import Kitchen
from menu import Menu
from orders import OrderService


class OrderServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = OrderService(Menu())

    def test_create_returns_incremented_order_ids(self):
        first = self.service.create(12)
        second = self.service.create(3)
        self.assertEqual(first.id, "ORD-0001")
        self.assertEqual(second.id, "ORD-0002")

    def test_add_item_appends_line_and_snapshots_price(self):
        order = self.service.create(12)
        self.service.add_item(order.id, 1, 2)
        self.assertEqual(order.items[0]["name"], "Margherita Pizza")
        self.assertEqual(order.items[0]["price"], 14.5)
        self.assertEqual(order.items[0]["quantity"], 2)

    def test_total_multiplies_price_by_quantity(self):
        order = self.service.create(12)
        self.service.add_item(order.id, 1, 2)
        self.service.add_item(order.id, 3, 1)
        self.assertEqual(order.total, 35.5)

    def test_add_item_unknown_order_raises(self):
        with self.assertRaises(LookupError):
            self.service.add_item("ORD-9999", 1, 1)

    def test_add_item_unavailable_item_raises(self):
        order = self.service.create(1)
        with self.assertRaises(LookupError):
            self.service.add_item(order.id, 999, 1)

    def test_add_item_non_positive_quantity_raises(self):
        order = self.service.create(1)
        with self.assertRaises(ValueError):
            self.service.add_item(order.id, 1, 0)


class KitchenTest(unittest.TestCase):
    def test_advance_follows_state_machine(self):
        order = OrderService(Menu()).create(12)
        states = []
        for _ in range(4):
            states.append(Kitchen.advance(order)["status"])
        self.assertEqual(states, ["submitted", "preparing", "ready", "served"])

    def test_advance_complete_order_raises(self):
        order = OrderService(Menu()).create(12)
        for _ in range(4):
            Kitchen.advance(order)
        with self.assertRaises(ValueError):
            Kitchen.advance(order)


if __name__ == "__main__":
    unittest.main()