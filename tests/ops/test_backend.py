from unittest import TestCase
from gluepy.ops.backend import BaseOpsBackend, LoggingOpsBackend


class BaseOpsBackendTestCase(TestCase):
    def test_get_metrics_raises_not_implemented(self):
        backend = BaseOpsBackend()
        with self.assertRaises(NotImplementedError):
            backend.get_metrics()


class LoggingOpsBackendTestCase(TestCase):
    def setUp(self):
        self.backend = LoggingOpsBackend()

    def test_log_metric_stores_metrics(self):
        self.backend.log_metric("accuracy", 0.95)
        self.assertEqual(self.backend.get_metrics(), {"accuracy": 0.95})

    def test_get_metrics_returns_all(self):
        self.backend.log_metric("mape", 12.5)
        self.backend.log_metric("bias", -0.03)
        metrics = self.backend.get_metrics()
        self.assertEqual(metrics, {"mape": 12.5, "bias": -0.03})

    def test_duplicate_key_returns_last_value(self):
        self.backend.log_metric("mape", 15.0)
        self.backend.log_metric("mape", 12.5)
        self.assertEqual(self.backend.get_metrics()["mape"], 12.5)

    def test_get_metrics_returns_copy(self):
        self.backend.log_metric("mape", 12.5)
        metrics = self.backend.get_metrics()
        metrics["mape"] = 99.0
        self.assertEqual(self.backend.get_metrics()["mape"], 12.5)

    def test_create_run_resets_metrics(self):
        self.backend.log_metric("mape", 12.5)
        self.backend.create_run(dag="test")
        self.assertEqual(self.backend.get_metrics(), {})
