from unittest import TestCase
from gluepy.exec import Task, TASK_REGISTRY


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        for k in list(TASK_REGISTRY.keys()):
            del TASK_REGISTRY[k]
        return super().setUp()

    def test_task_duplication(self):
        """Ensure 2 Tasks cannot have the same label"""
        with self.assertRaises(KeyError):

            class TestTask(Task):
                label = "test"

                def run(self):
                    pass

            class TestDuplicateTask(Task):
                label = "test"

                def run(self):
                    pass
