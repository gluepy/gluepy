from unittest import TestCase
from gluepy.exec import Task, EvaluationTask, DAG, TASK_REGISTRY, DAG_REGISTRY


class EvaluationTaskTestCase(TestCase):
    def setUp(self):
        for k in list(TASK_REGISTRY.keys()):
            del TASK_REGISTRY[k]
        for k in list(DAG_REGISTRY.keys()):
            del DAG_REGISTRY[k]

    def test_evaluation_task_is_subclass_of_task(self):
        self.assertTrue(issubclass(EvaluationTask, Task))

    def test_evaluation_task_registers_in_task_registry(self):
        class MyEvalTask(EvaluationTask):
            label = "my_eval"

            def run(self):
                pass

        self.assertIn("my_eval", TASK_REGISTRY)
        self.assertIs(TASK_REGISTRY["my_eval"], MyEvalTask)

    def test_dag_eval_tasks_defaults_to_empty(self):
        class TestDAG(DAG):
            label = "test_default"
            tasks = []

        dag = TestDAG()
        self.assertEqual(dag.eval_tasks, [])

    def test_inject_tasks_includes_eval_tasks(self):
        class WorkTask(Task):
            label = "work"

            def run(self):
                pass

        class EvalTask(EvaluationTask):
            label = "eval"

            def run(self):
                pass

        class TestDAG(DAG):
            label = "test_inject"
            tasks = [WorkTask]
            eval_tasks = [EvalTask]

        dag = TestDAG()
        tasks = dag.inject_tasks()
        self.assertIn(WorkTask, tasks)
        self.assertIn(EvalTask, tasks)
        self.assertGreater(tasks.index(EvalTask), tasks.index(WorkTask))

    def test_inject_tasks_skip_eval(self):
        class WorkTask2(Task):
            label = "work2"

            def run(self):
                pass

        class EvalTask2(EvaluationTask):
            label = "eval2"

            def run(self):
                pass

        class TestDAG(DAG):
            label = "test_skip"
            tasks = [WorkTask2]
            eval_tasks = [EvalTask2]

        dag = TestDAG()
        tasks = dag.inject_tasks(skip_eval=True)
        self.assertIn(WorkTask2, tasks)
        self.assertNotIn(EvalTask2, tasks)

    def test_inject_tasks_eval_only(self):
        class WorkTask3(Task):
            label = "work3"

            def run(self):
                pass

        class EvalTask3(EvaluationTask):
            label = "eval3"

            def run(self):
                pass

        class TestDAG(DAG):
            label = "test_eval_only"
            tasks = [WorkTask3]
            eval_tasks = [EvalTask3]

        dag = TestDAG()
        tasks = dag.inject_tasks(eval_only=True)
        self.assertNotIn(WorkTask3, tasks)
        self.assertIn(EvalTask3, tasks)

    def test_inject_tasks_backward_compat(self):
        """DAG without eval_tasks works exactly as before."""

        class WorkTask4(Task):
            label = "work4"

            def run(self):
                pass

        class TestDAG(DAG):
            label = "test_compat"
            tasks = [WorkTask4]

        dag = TestDAG()
        tasks = dag.inject_tasks()
        self.assertIn(WorkTask4, tasks)
        # Should have start task + work task
        self.assertEqual(len(tasks), 2)
