import unittest
from datetime import date

from goals import GoalService
from reports import FitnessReport
from workouts import WorkoutService


class WorkoutServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = WorkoutService()

    def test_log_assigns_incrementing_ids(self):
        first = self.service.log("Running", 35, 360)
        second = self.service.log("Cycling", 50, 420)
        self.assertEqual((first.id, second.id), (1, 2))

    def test_log_uses_default_today_date(self):
        workout = self.service.log("Running", 35, 360)
        self.assertEqual(workout.workout_date, date.today().isoformat())

    def test_log_non_positive_duration_raises(self):
        with self.assertRaises(ValueError):
            self.service.log("Running", 0, 360)

    def test_log_negative_calories_raises(self):
        with self.assertRaises(ValueError):
            self.service.log("Running", 35, -1)

    def test_log_blank_activity_raises(self):
        with self.assertRaises(ValueError):
            self.service.log("", 35, 360)


class FitnessReportTest(unittest.TestCase):
    def test_build_aggregates_workouts(self):
        service = WorkoutService()
        service.log("Running", 35, 360)
        service.log("Strength Training", 45, 280)
        service.log("Cycling", 50, 420)
        report = FitnessReport.build(service.workouts, GoalService())
        self.assertEqual(report["total_workouts"], 3)
        self.assertEqual(report["total_minutes"], 130)
        self.assertEqual(report["total_calories"], 1060)
        self.assertEqual(
            report["activities"], ["Cycling", "Running", "Strength Training"]
        )


class GoalServiceTest(unittest.TestCase):
    def test_progress_percentages(self):
        service = WorkoutService()
        service.log("Running", 130, 500)
        progress = GoalService(150, 4).progress(service.workouts)
        self.assertEqual(progress["minutes"]["percent"], 86.7)
        self.assertEqual(progress["workouts"]["percent"], 25.0)

    def test_progress_caps_at_one_hundred(self):
        service = WorkoutService()
        service.log("Running", 300, 500)
        progress = GoalService(150, 4).progress(service.workouts)
        self.assertEqual(progress["minutes"]["percent"], 100.0)


if __name__ == "__main__":
    unittest.main()