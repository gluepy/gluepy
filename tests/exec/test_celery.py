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

    def _create_app_and_capture_task(self):
        """
        Helper to create celery app and capture the registered
        run_dag_task function.
        """
        mock_app = mock.Mock()
        self.mock_celery_module.Celery.return_value = mock_app

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
        return captured_func

    def test_run_dag_task(self):
        captured_func = self._create_app_and_capture_task()
        self.assertIsNotNone(captured_func)

        with mock.patch("gluepy.exec.boot.bootstrap") as mock_bootstrap, mock.patch(
            "gluepy.commands.dag.run_dag"
        ) as mock_run_dag, mock.patch("gluepy.files.storages.default_storage") as _:
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

    def test_run_dag_task_writes_success_signal(self):
        captured_func = self._create_app_and_capture_task()

        with mock.patch("gluepy.exec.boot.bootstrap"), mock.patch(
            "gluepy.commands.dag.run_dag"
        ), mock.patch("gluepy.files.storages.default_storage") as mock_storage:
            result = captured_func(
                None,
                "test_label",
                retry=None,
                patch=None,
                local_patch=None,
                from_task=None,
                task=None,
            )

            # Verify .dag_success signal was written to the run folder
            mock_storage.touch.assert_called_once()
            signal_path = mock_storage.touch.call_args[0][0]
            signal_content = mock_storage.touch.call_args[0][1]
            self.assertTrue(signal_path.endswith(".dag_success"))
            self.assertEqual(signal_content.read(), "success")
            self.assertEqual(result["status"], "success")

    def test_run_dag_task_reads_run_folder_after_run_dag(self):
        """
        Ensure run_folder is read from default_context AFTER run_dag()
        completes, not before. This prevents a stale run_folder when
        run_dag() sets up its own context (e.g. via retry path).
        """
        captured_func = self._create_app_and_capture_task()

        pre_run_folder = "stale/pre/run_folder"
        post_run_folder = "correct/post/run_folder"

        mock_context = mock.MagicMock()
        mock_context.gluepy.run_folder = pre_run_folder

        def simulate_run_dag(*args, **kwargs):
            # Simulate run_dag changing the context's run_folder
            mock_context.gluepy.run_folder = post_run_folder

        with mock.patch("gluepy.exec.boot.bootstrap"), mock.patch(
            "gluepy.commands.dag.run_dag", side_effect=simulate_run_dag
        ), mock.patch("gluepy.files.storages.default_storage") as mock_storage, mock.patch(
            "gluepy.conf.default_context", mock_context
        ):
            result = captured_func(
                None,
                "test_label",
                retry=None,
                patch=None,
                local_patch=None,
                from_task=None,
                task=None,
            )

            # Signal must use the POST-run_dag run_folder, not the stale one
            signal_path = mock_storage.touch.call_args[0][0]
            self.assertIn(post_run_folder, signal_path)
            self.assertNotIn(pre_run_folder, signal_path)
            self.assertEqual(result["run_folder"], post_run_folder)

    def test_run_dag_task_writes_failure_signal(self):
        captured_func = self._create_app_and_capture_task()

        with mock.patch("gluepy.exec.boot.bootstrap"), mock.patch(
            "gluepy.commands.dag.run_dag", side_effect=RuntimeError("task exploded")
        ), mock.patch("gluepy.files.storages.default_storage") as mock_storage:
            with self.assertRaises(RuntimeError):
                captured_func(
                    None,
                    "test_label",
                    retry=None,
                    patch=None,
                    local_patch=None,
                    from_task=None,
                    task=None,
                )

            # Verify .dag_failed signal was written with the error message
            mock_storage.touch.assert_called_once()
            signal_path = mock_storage.touch.call_args[0][0]
            signal_content = mock_storage.touch.call_args[0][1]
            self.assertTrue(signal_path.endswith(".dag_failed"))
            self.assertEqual(signal_content.read(), "task exploded")

    def test_run_dag_task_reads_run_folder_after_run_dag_on_failure(self):
        """
        Ensure run_folder is read from default_context AFTER run_dag()
        sets up context, even when run_dag() raises an exception.
        """
        captured_func = self._create_app_and_capture_task()

        pre_run_folder = "stale/pre/run_folder"
        post_run_folder = "correct/post/run_folder"

        mock_context = mock.MagicMock()
        mock_context.gluepy.run_folder = pre_run_folder

        def simulate_run_dag_failure(*args, **kwargs):
            # Simulate run_dag changing context before failing
            mock_context.gluepy.run_folder = post_run_folder
            raise RuntimeError("task exploded")

        with mock.patch("gluepy.exec.boot.bootstrap"), mock.patch(
            "gluepy.commands.dag.run_dag", side_effect=simulate_run_dag_failure
        ), mock.patch("gluepy.files.storages.default_storage") as mock_storage, mock.patch(
            "gluepy.conf.default_context", mock_context
        ):
            with self.assertRaises(RuntimeError):
                captured_func(
                    None,
                    "test_label",
                    retry=None,
                    patch=None,
                    local_patch=None,
                    from_task=None,
                    task=None,
                )

            # Signal must use the POST-run_dag run_folder, not the stale one
            signal_path = mock_storage.touch.call_args[0][0]
            self.assertIn(post_run_folder, signal_path)
            self.assertNotIn(pre_run_folder, signal_path)

    def test_run_dag_task_reraises_on_failure(self):
        """
        Ensure the original exception is re-raised after
        writing the failure signal.
        """
        captured_func = self._create_app_and_capture_task()

        with mock.patch("gluepy.exec.boot.bootstrap"), mock.patch(
            "gluepy.commands.dag.run_dag", side_effect=ValueError("bad input")
        ), mock.patch("gluepy.files.storages.default_storage"):
            with self.assertRaises(ValueError) as cm:
                captured_func(
                    None,
                    "test_label",
                    retry=None,
                    patch=None,
                    local_patch=None,
                    from_task=None,
                    task=None,
                )
            self.assertEqual(str(cm.exception), "bad input")
