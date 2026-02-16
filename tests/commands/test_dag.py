import os
import tempfile
import yaml
from io import StringIO
from unittest import TestCase
from gluepy.exec import Task, DAG, DAG_REGISTRY, TASK_REGISTRY
from gluepy.commands.dag import run_dag
from gluepy.files.storages import default_storage


class DagCommandTestCase(TestCase):
    def setUp(self) -> None:
        for k in list(DAG_REGISTRY.keys()):
            del DAG_REGISTRY[k]
        for k in list(TASK_REGISTRY.keys()):
            del TASK_REGISTRY[k]

        class NoopTask(Task):
            label = "noop"

            def run(self):
                default_storage.touch("noop.txt", StringIO("done"))

        class TestDAG(DAG):
            label = "test_local_patch"
            tasks = [NoopTask]

        self.NoopTask = NoopTask
        self.TestDAG = TestDAG
        return super().setUp()

    def test_run_dag_with_local_patch(self):
        patch_data = {"foo": 2}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(patch_data, f)
            patch_path = f.name

        try:
            run_dag("test_local_patch", local_patch=[patch_path])
            from gluepy.conf import default_context

            self.assertEqual(default_context.foo, 2)
        finally:
            os.unlink(patch_path)

    def test_run_dag_with_local_patch_absolute_path(self):
        patch_data = {"foo": 99}
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, dir=tempfile.gettempdir()
        ) as f:
            yaml.dump(patch_data, f)
            patch_path = os.path.abspath(f.name)

        try:
            run_dag("test_local_patch", local_patch=[patch_path])
            from gluepy.conf import default_context

            self.assertEqual(default_context.foo, 99)
        finally:
            os.unlink(patch_path)

    def test_run_dag_with_local_patch_missing_file(self):
        with self.assertLogs("gluepy.commands.dag", level="WARNING") as cm:
            run_dag("test_local_patch", local_patch=["/nonexistent/patch.yaml"])
        self.assertTrue(any("was not found" in msg for msg in cm.output))

    def test_run_dag_with_both_patch_and_local_patch(self):
        local_data = {"foo": 42}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(local_data, f)
            local_path = f.name

        try:
            # Storage patch that doesn't exist will be warned and skipped,
            # local patch should still be applied.
            run_dag(
                "test_local_patch",
                patch=["nonexistent_storage_patch.yaml"],
                local_patch=[local_path],
            )
            from gluepy.conf import default_context

            self.assertEqual(default_context.foo, 42)
        finally:
            os.unlink(local_path)
