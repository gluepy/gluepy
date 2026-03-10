import json
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from gluepy.exec import Task, EvaluationTask, DAG, DAG_REGISTRY, TASK_REGISTRY
from gluepy.commands.dag import run_dag
from gluepy.files.storages import default_storage
from gluepy.ops import default_mlops


class DagEvalCommandTestCase(TestCase):
    def setUp(self):
        for k in list(DAG_REGISTRY.keys()):
            del DAG_REGISTRY[k]
        for k in list(TASK_REGISTRY.keys()):
            del TASK_REGISTRY[k]

        class WorkTask(Task):
            label = "work_eval_test"

            def run(self):
                default_storage.touch("work.txt", StringIO("done"))

        class EvalTask(EvaluationTask):
            label = "eval_eval_test"

            def run(self):
                default_mlops.log_metric("mape", 12.5)
                default_mlops.log_metric("bias", -0.03)

        class TestDAG(DAG):
            label = "test_eval"
            tasks = [WorkTask]
            eval_tasks = [EvalTask]

        self.WorkTask = WorkTask
        self.EvalTask = EvalTask
        self.TestDAG = TestDAG

    def test_run_dag_with_eval_tasks(self):
        """Full run includes both work and eval tasks."""
        with patch("builtins.print") as mock_print:
            run_dag("test_eval")
        # Check that metrics were printed
        calls = [str(c) for c in mock_print.call_args_list]
        joined = " ".join(calls)
        self.assertIn("GLUEPY METRICS", joined)
        self.assertIn("metric:mape=12.5", joined)
        self.assertIn("metric:bias=-0.03", joined)

    def test_run_dag_skip_eval(self):
        """--skip-eval skips evaluation tasks."""
        with patch("builtins.print") as mock_print:
            run_dag("test_eval", skip_eval=True)
        self.assertTrue(default_storage.exists("work.txt"))
        calls = [str(c) for c in mock_print.call_args_list]
        joined = " ".join(calls)
        self.assertNotIn("GLUEPY METRICS", joined)

    def test_eval_only_requires_retry(self):
        """--eval-only without --retry raises assertion."""
        with self.assertRaises(AssertionError):
            run_dag("test_eval", eval_only=True)

    def test_skip_eval_and_eval_only_exclusive(self):
        """--skip-eval and --eval-only are mutually exclusive."""
        with self.assertRaises(AssertionError):
            run_dag("test_eval", skip_eval=True, eval_only=True, retry="some_folder")

    def test_metrics_json_written(self):
        """Metrics are persisted to metrics.json in run folder."""
        run_dag("test_eval")
        metrics_path = default_storage.runpath("metrics.json")
        self.assertTrue(default_storage.exists(metrics_path))
        content = default_storage.open(metrics_path, mode="r")
        metrics = json.loads(content)
        self.assertEqual(metrics["mape"], 12.5)
        self.assertEqual(metrics["bias"], -0.03)

    def test_backward_compat_no_eval_tasks(self):
        """DAG without eval_tasks works as before (no metrics block)."""
        for k in list(DAG_REGISTRY.keys()):
            del DAG_REGISTRY[k]
        for k in list(TASK_REGISTRY.keys()):
            del TASK_REGISTRY[k]

        class SimpleTask(Task):
            label = "simple"

            def run(self):
                default_storage.touch("simple.txt", StringIO("done"))

        class SimpleDAG(DAG):
            label = "test_simple"
            tasks = [SimpleTask]

        with patch("builtins.print") as mock_print:
            run_dag("test_simple")
        calls = [str(c) for c in mock_print.call_args_list]
        joined = " ".join(calls)
        self.assertNotIn("GLUEPY METRICS", joined)
