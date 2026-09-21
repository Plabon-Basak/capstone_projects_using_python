import unittest

from alerts import WeatherAlerts
from monitoring import WeatherMonitor
from stations import WeatherStation


class WeatherMonitorTest(unittest.TestCase):
    def setUp(self):
        self.monitor = WeatherMonitor(
            [WeatherStation("Austin"), WeatherStation("Houston")]
        )

    def test_ingest_returns_reading_with_timestamp(self):
        reading = self.monitor.ingest("Austin", 80, 50, 10, "Sunny")
        self.assertEqual(reading.station, "Austin")
        self.assertTrue(reading.observed_at)

    def test_ingest_unknown_station_raises(self):
        with self.assertRaises(LookupError):
            self.monitor.ingest("Dallas", 80, 50, 10, "Sunny")

    def test_ingest_out_of_range_temperature_raises(self):
        with self.assertRaises(ValueError):
            self.monitor.ingest("Austin", 200, 50, 10, "Sunny")

    def test_ingest_out_of_range_humidity_raises(self):
        with self.assertRaises(ValueError):
            self.monitor.ingest("Austin", 80, 150, 10, "Sunny")

    def test_ingest_negative_wind_raises(self):
        with self.assertRaises(ValueError):
            self.monitor.ingest("Austin", 80, 50, -5, "Sunny")

    def test_dashboard_returns_latest_per_station(self):
        self.monitor.ingest("Austin", 97, 42, 14, "Sunny")
        self.monitor.ingest("Houston", 88, 74, 34, "Thunderstorm")
        dashboard = self.monitor.dashboard()
        self.assertEqual(len(dashboard["stations"]), 2)
        self.assertEqual(dashboard["stations"][0]["station"], "Austin")
        self.assertEqual(dashboard["stations"][1]["station"], "Houston")


class WeatherAlertsTest(unittest.TestCase):
    def test_heat_advisory_above_threshold(self):
        reading = WeatherMonitor([WeatherStation("Austin")]).ingest(
            "Austin", 96, 40, 10, "Sunny"
        )
        self.assertIn("Heat advisory", WeatherAlerts.evaluate(reading))

    def test_high_wind_advisory(self):
        reading = WeatherMonitor([WeatherStation("Austin")]).ingest(
            "Austin", 80, 40, 35, "Sunny"
        )
        self.assertIn("High wind advisory", WeatherAlerts.evaluate(reading))

    def test_severe_weather_watch_for_storm(self):
        reading = WeatherMonitor([WeatherStation("Austin")]).ingest(
            "Austin", 80, 90, 20, "Thunderstorm"
        )
        self.assertIn("Severe weather watch", WeatherAlerts.evaluate(reading))

    def test_no_alerts_reports_clear(self):
        reading = WeatherMonitor([WeatherStation("Austin")]).ingest(
            "Austin", 80, 50, 10, "Sunny"
        )
        self.assertEqual(WeatherAlerts.evaluate(reading), ["No active alerts"])


if __name__ == "__main__":
    unittest.main()