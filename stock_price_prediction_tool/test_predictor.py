import unittest

from evaluation import backtest
from predictor import TrendPredictor


class TrendPredictorTest(unittest.TestCase):
    def test_predict_extends_beyond_last_observation(self):
        prices = [101.2, 102.8, 102.1, 104.6, 105.4, 106.9, 108.1]
        model = TrendPredictor().fit(prices)
        self.assertGreater(model.predict_next(), prices[-1])

    def test_fit_requires_two_prices(self):
        with self.assertRaises(ValueError):
            TrendPredictor().fit([100.0])

    def test_moving_average_uses_last_window(self):
        model = TrendPredictor().fit([1.0, 1.0, 1.0])
        self.assertEqual(model.moving_average([1.0, 2.0, 3.0, 4.0]), 3.0)

    def test_moving_average_insufficient_data_raises(self):
        model = TrendPredictor().fit([1.0, 2.0])
        with self.assertRaises(ValueError):
            model.moving_average([10.0])


class BacktestTest(unittest.TestCase):
    def test_returns_mae_and_point_count(self):
        prices = [101.2, 102.8, 102.1, 104.6, 105.4, 106.9, 108.1]
        result = backtest(prices, TrendPredictor)
        self.assertEqual(result["test_points"], 4)
        self.assertGreater(result["mean_absolute_error"], 0)

    def test_insufficient_history_raises(self):
        with self.assertRaises(ValueError):
            backtest([101.2, 102.8, 102.1], TrendPredictor)


if __name__ == "__main__":
    unittest.main()