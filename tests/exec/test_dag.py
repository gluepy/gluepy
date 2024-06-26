from unittest import TestCase
from gluepy.exec import Task, DAG
from gluepy.commands.dag import run_dag


class DAGTestCase(TestCase):

    def test_dag_execution(self):
        class TaskA(Task):
            def run(self):
                pass
        class TaskB(Task):
            def run(self):
                pass

        class TestDAG(DAG):
            label = "test"
            tasks = [TaskA, TaskB]

        run_dag(label="test")
