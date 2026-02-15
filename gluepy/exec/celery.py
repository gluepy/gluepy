from gluepy.conf import default_settings


def create_celery_app():
    from celery import Celery

    app = Celery(
        "gluepy",
        broker=default_settings.CELERY_BROKER_URL,
        backend=getattr(default_settings, "CELERY_RESULT_BACKEND", None),
    )
    # Apply any CELERY_ prefixed settings
    app.config_from_object(
        {
            k: v
            for k, v in vars(default_settings).items()
            if k.startswith("CELERY_")
            and k not in ("CELERY_BROKER_URL", "CELERY_RESULT_BACKEND")
        }
    )

    @app.task(name="gluepy.run_dag", bind=True)
    def run_dag_task(
        self, label, retry=None, patch=None, local_patch=None, from_task=None, task=None
    ):
        from gluepy.exec.boot import bootstrap
        from gluepy.commands.dag import run_dag

        bootstrap()
        run_dag(
            label,
            retry=retry,
            patch=patch,
            local_patch=local_patch,
            from_task=from_task,
            task=task,
        )
        from gluepy.conf import default_context

        return {
            "status": "success",
            "run_id": default_context.gluepy.run_id,
            "run_folder": default_context.gluepy.run_folder,
        }

    return app


def submit_dag(label, **kwargs):
    app = create_celery_app()
    return app.send_task("gluepy.run_dag", kwargs={"label": label, **kwargs})
