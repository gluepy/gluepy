import sys
from unittest import TestCase, mock


class WorkerCommandTestCase(TestCase):
    def setUp(self):
        self.mock_celery_module = mock.MagicMock()
        self.patcher = mock.patch.dict(
            "sys.modules", {"celery": self.mock_celery_module}
        )
        self.patcher.start()
        if "gluepy.exec.celery" in sys.modules:
            del sys.modules["gluepy.exec.celery"]
        return super().setUp()

    def tearDown(self):
        self.patcher.stop()
        if "gluepy.exec.celery" in sys.modules:
            del sys.modules["gluepy.exec.celery"]
        return super().tearDown()

    def test_worker_creates_celery_app(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        from gluepy.exec.celery import create_celery_app

        app = create_celery_app()
        self.mock_celery_module.Celery.assert_called()
        self.assertEqual(app, mock_app)

    def test_worker_passes_concurrency(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        with mock.patch("gluepy.exec.celery.create_celery_app") as mock_create_app:
            mock_create_app.return_value = mock_app
            from click.testing import CliRunner
            from gluepy.commands import cli

            runner = CliRunner()
            runner.invoke(cli, ["worker", "--concurrency", "4"])
            mock_app.worker_main.assert_called_once()
            argv = mock_app.worker_main.call_args[0][0]
            self.assertIn("--concurrency", argv)
            self.assertIn("4", argv)

    def test_worker_passes_queues(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        with mock.patch("gluepy.exec.celery.create_celery_app") as mock_create_app:
            mock_create_app.return_value = mock_app
            from click.testing import CliRunner
            from gluepy.commands import cli

            runner = CliRunner()
            runner.invoke(cli, ["worker", "--queues", "high,low"])
            mock_app.worker_main.assert_called_once()
            argv = mock_app.worker_main.call_args[0][0]
            self.assertIn("--queues", argv)
            self.assertIn("high,low", argv)

    def test_worker_passes_pool(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        with mock.patch("gluepy.exec.celery.create_celery_app") as mock_create_app:
            mock_create_app.return_value = mock_app
            from click.testing import CliRunner
            from gluepy.commands import cli

            runner = CliRunner()
            runner.invoke(cli, ["worker", "--pool", "solo"])
            mock_app.worker_main.assert_called_once()
            argv = mock_app.worker_main.call_args[0][0]
            self.assertIn("--pool", argv)
            self.assertIn("solo", argv)
