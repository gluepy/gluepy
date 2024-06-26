import os

BASE_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(BASE_DIR, "")
INSTALLED_MODULES = []
STORAGE_BACKEND = "gluepy.files.storages.LocalStorage"
STORAGE_ROOT = os.path.join(BASE_DIR, "data")
DATA_BACKEND = "gluepy.files.data.PandasDataManager"
CONTEXT_BACKEND = "gluepy.conf.context.DefaultContextManager"
START_TASK = "gluepy.exec.tasks.BootstrapTask"
AIRFLOW_DAG_PREFIX = ""
AIRFLOW_TEMPLATE = None
AIRFLOW_IMAGE = "python:3.9-slim"
AIRFLOW_CONFIGMAPS = []
AIRFLOW_POD_RESOURCES = {"requests": {"cpu": "1000m", "memory": "128Mi"}}
AIRFLOW_KUBERNETES_CONFIG = "~/.kube/config"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{levelname} {asctime} {module} - {message}", "style": "{"}
    },
    "handlers": {
        "stream": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        }
    },
    "loggers": {
        "gluepy": {
            "handlers": [
                "stream",
            ],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
