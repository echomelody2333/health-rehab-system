import unittest
from backend.health_metrics import HealthMetricService

class HealthMetricServiceTest(unittest.TestCase):
    def setUp(self):
        self.service = HealthMetricService()

    def test_add_normal_metric(self):
        metric = self.service.add_metric(
            member_id=1,
            metric_type="收缩压",
            value=128,
            measured_at="2026-09-08T08:30:00",
        )
        self.assertEqual(metric["unit"], "mmHg")
        self.assertFalse(metric["abnormal"])

    def test_high_blood_pressure_is_marked_abnormal(self):
        metric = self.service.add_metric(
            member_id=1,
            metric_type="收缩压",
            value=165,
        )
        self.assertTrue(metric["abnormal"])

    def test_out_of_range_value_is_rejected(self):
        with self.assertRaises(ValueError):
            self.service.add_metric(
                member_id=1,
                metric_type="收缩压",
                value=400,
            )

if __name__ == "__main__":
    unittest.main()
