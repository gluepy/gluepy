import os
import logging
from io import StringIO

from gluepy.conf import default_settings

logger = logging.getLogger(__name__)


def create_celery_app():
    from celery import Celery

    app = Celery(
        "gluepy",
        broker=default_settings.CELERY_BROKER_URL,
        backend=getattr(default_settings, "CELERY_RESULT_BACKEND", None),
    )
    # Apply any CELERY_ prefixed settings.
    # Use dir() + getattr() instead of vars() because default_settings
    # is a LazyProxy — vars() returns the proxy's __dict__, not the
    # wrapped Settings object's attributes.
    app.config_from_object(
        {
            k: getattr(default_settings, k)
            for k in dir(default_settings)
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
        from gluepy.files.storages import default_storage

        bootstrap()

        from gluepy.conf import default_context

        run_folder = default_context.gluepy.run_folder

        try:
            run_dag(
                label,
                retry=retry,
                patch=patch,
                local_patch=local_patch,
                from_task=from_task,
                task=task,
            )
        except Exception as e:
            logger.error(f"DAG '{label}' failed: {e}", exc_info=True)
            try:
                signal_path = os.path.join(run_folder, ".dag_failed")
                default_storage.touch(signal_path, StringIO(str(e)))
                logger.info(f"Wrote failure signal to {signal_path}")
            except Exception as signal_error:
                logger.error(
                    f"Failed to write failure signal: {signal_error}", exc_info=True
                )
            raise

        signal_path = os.path.join(run_folder, ".dag_success")
        default_storage.touch(signal_path, StringIO("success"))
        logger.info(f"Wrote success signal to {signal_path}")

        return {
            "status": "success",
            "run_id": default_context.gluepy.run_id,
            "run_folder": run_folder,
        }

    return app


def submit_dag(label, **kwargs):
    app = create_celery_app()
    return app.send_task("gluepy.run_dag", kwargs={"label": label, **kwargs})
