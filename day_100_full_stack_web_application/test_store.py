import unittest

from store import TaskStore


class TaskStoreTest(unittest.TestCase):
    def setUp(self):
        self.store = TaskStore()

    def test_list_returns_seeded_tasks(self):
        self.assertEqual(len(self.store.list()), 2)

    def test_create_adds_task_with_next_id(self):
        task = self.store.create("Write tests")
        self.assertEqual(task["id"], 3)
        self.assertEqual(task["title"], "Write tests")
        self.assertFalse(task["completed"])
        self.assertEqual(len(self.store.list()), 3)

    def test_create_strips_title(self):
        task = self.store.create("  Trim me  ")
        self.assertEqual(task["title"], "Trim me")

    def test_create_blank_title_raises(self):
        with self.assertRaises(ValueError):
            self.store.create("   ")

    def test_toggle_flips_completion(self):
        before = self.store.toggle(1)["completed"]
        after = self.store.toggle(1)["completed"]
        self.assertNotEqual(before, after)

    def test_toggle_unknown_task_raises(self):
        with self.assertRaises(LookupError):
            self.store.toggle(999)


if __name__ == "__main__":
    unittest.main()