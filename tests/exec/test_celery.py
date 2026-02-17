import sys
from unittest import TestCase, mock


class CeleryTestCase(TestCase):
    def setUp(self):
        # Create a mock celery module so imports work without celery installed
        self.mock_celery_module = mock.MagicMock()
        self.patcher = mock.patch.dict(
            "sys.modules", {"celery": self.mock_celery_module}
        )
        self.patcher.start()
        # Clear cached module so create_celery_app reimports
        if "gluepy.exec.celery" in sys.modules:
            del sys.modules["gluepy.exec.celery"]
        return super().setUp()

    def tearDown(self):
        self.patcher.stop()
        if "gluepy.exec.celery" in sys.modules:
            del sys.modules["gluepy.exec.celery"]
        return super().tearDown()

    def test_create_celery_app(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        from gluepy.exec.celery import create_celery_app
        from gluepy.conf import default_settings

        app = create_celery_app()
        self.mock_celery_module.Celery.assert_called_with(
            "gluepy",
            broker=default_settings.CELERY_BROKER_URL,
            backend=getattr(default_settings, "CELERY_RESULT_BACKEND", None),
        )
        self.assertEqual(app, mock_app)

    def test_create_celery_app_forwards_celery_settings(self):
        """Ensure CELERY_ prefixed settings are forwarded via config_from_object.

        This verifies the fix for using dir()+getattr() instead of vars()
        on the LazyProxy default_settings.
        """
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        from gluepy.exec.celery import create_celery_app

        # Add a custom CELERY_ setting to the test settings module
        import settings as test_settings

        test_settings.CELERY_TASK_SERIALIZER = "json"
        try:
            # Reset default_settings so it picks up the new attribute
            from gluepy.conf import default_settings
            from gluepy.utils.loading import empty

            default_settings._wrapped = empty

            create_celery_app()

            # config_from_object should have been called with a dict
            # containing our custom setting (but not BROKER_URL/RESULT_BACKEND)
            mock_app.config_from_object.assert_called_once()
            config = mock_app.config_from_object.call_args[0][0]
            self.assertEqual(config["CELERY_TASK_SERIALIZER"], "json")
            self.assertNotIn("CELERY_BROKER_URL", config)
            self.assertNotIn("CELERY_RESULT_BACKEND", config)
        finally:
            # Clean up the test setting we added
            del test_settings.CELERY_TASK_SERIALIZER

    def test_submit_dag(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app
        mock_app.task.return_value = lambda f: f

        from gluepy.exec.celery import submit_dag

        submit_dag("my_dag", retry="some/path")
        mock_app.send_task.assert_called_once_with(
            "gluepy.run_dag",
            kwargs={"label": "my_dag", "retry": "some/path"},
        )

    def test_run_dag_task(self):
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app

        # Capture the decorated function
        captured_func = None

        def capture_task(**kwargs):
            def decorator(f):
                nonlocal captured_func
                captured_func = f
                return f

            return decorator

        mock_app.task = capture_task

        from gluepy.exec.celery import create_celery_app

        create_celery_app()
        self.assertIsNotNone(captured_func)

        with mock.patch("gluepy.exec.boot.bootstrap") as mock_bootstrap, mock.patch(
            "gluepy.commands.dag.run_dag"
        ) as mock_run_dag:
            captured_func(
                None,
                "test_label",
                retry=None,
                patch=None,
                local_patch=None,
                from_task=None,
                task=None,
            )
            mock_bootstrap.assert_called_once()
            mock_run_dag.assert_called_once_with(
                "test_label",
                retry=None,
                patch=None,
                local_patch=None,
                from_task=None,
                task=None,
            )
