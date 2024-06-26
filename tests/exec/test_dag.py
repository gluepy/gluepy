from io import StringIO
from unittest import TestCase
from gluepy.exec import Task, DAG, DAG_REGISTRY
from gluepy.commands.dag import run_dag
from gluepy.files.storages import default_storage


class DAGTestCase(TestCase):
    def setUp(self) -> None:
        for k in list(DAG_REGISTRY.keys()):
            del DAG_REGISTRY[k]
        return super().setUp()

    def test_dag_execution(self):
        class TaskA(Task):
            def run(self):
                default_storage.touch("taska.txt", StringIO("foo"))

        class TaskB(Task):
            def run(self):
                default_storage.touch("taskb.txt", StringIO("bar"))

        class TestDAG(DAG):
            label = "test"
            tasks = [TaskA, TaskB]

        # Test that dag is being executed, and artifact from TaskA
        # and TaskB is being created.
        run_dag(label="test")
        self.assertTrue(default_storage.exists("taska.txt"))
        self.assertTrue(default_storage.exists("taskb.txt"))

    def test_dag_duplication(self):
        """Ensure 2 DAGs cannot have the same label"""
        with self.assertRaises(KeyError):

            class TestDAG(DAG):
                label = "test"
                tasks = []

            class TestDuplicateDAG(DAG):
                label = "test"
                tasks = []
