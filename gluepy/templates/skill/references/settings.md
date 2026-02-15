# Settings System

Gluepy settings are defined in a Python module and loaded via the `GLUEPY_SETTINGS_MODULE` environment variable.

## Configuration

Set the environment variable to point to your settings module:

```bash
export GLUEPY_SETTINGS_MODULE=configs.settings
```

Or in `manage.py`:
```python
import os
os.environ.setdefault("GLUEPY_SETTINGS_MODULE", "configs.settings")
```

## Accessing Settings

```python
from gluepy.conf import default_settings

storage_root = default_settings.STORAGE_ROOT
config_path = default_settings.CONFIG_PATH
```

## Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `BASE_DIR` | Project root | Base directory of the project |
| `CONFIG_PATH` | `<BASE_DIR>/configs` | Directory containing YAML config files |
| `INSTALLED_MODULES` | `[]` | List of module dotted paths to auto-discover DAGs, Tasks, and commands |
| `STORAGE_BACKEND` | `gluepy.files.storages.local.LocalStorage` | Dotted path to storage backend class |
| `STORAGE_ROOT` | `<BASE_DIR>/data` | Root path for storage operations |
| `DATA_BACKEND` | `gluepy.files.data.PandasDataManager` | Dotted path to data manager class |
| `CONTEXT_BACKEND` | `gluepy.conf.context.DefaultContextManager` | Dotted path to context manager class |
| `MLOPS_BACKEND` | `gluepy.ops.backend.LoggingOpsBackend` | Dotted path to MLOps backend class |
| `START_TASK` | `gluepy.exec.tasks.BootstrapTask` | Dotted path to task prepended to all DAGs |
| `LOGGING` | Standard logging config | Python `logging.config.dictConfig` compatible dict |
| `AIRFLOW_DAG_PREFIX` | `""` | Prefix for generated Airflow DAG IDs |
| `AIRFLOW_TEMPLATE` | `None` | Custom Airflow DAG template |
| `AIRFLOW_IMAGE` | `python:3.9-slim` | Docker image for Airflow KubernetesPodOperator |
| `AIRFLOW_CONFIGMAPS` | `[]` | Kubernetes configmaps to mount |
| `AIRFLOW_POD_RESOURCES` | `{"requests": {"cpu": "1000m", "memory": "128Mi"}}` | Pod resource requests |
| `AIRFLOW_KUBERNETES_CONFIG` | `~/.kube/config` | Path to kubeconfig |
| `CELERY_BROKER_URL` | *(not set)* | Celery message broker URL (requires `gluepy[celery]`) |
| `CELERY_RESULT_BACKEND` | *(not set)* | Celery result backend URL |

## Settings by Environment

Use different settings files per environment:

```bash
# Development
export GLUEPY_SETTINGS_MODULE=configs.settings_dev

# Production
export GLUEPY_SETTINGS_MODULE=configs.settings_prod
```

```python
# configs/settings_dev.py
from configs.settings import *
STORAGE_BACKEND = "gluepy.files.storages.local.LocalStorage"
STORAGE_ROOT = "./data"
```

```python
# configs/settings_prod.py
from configs.settings import *
STORAGE_BACKEND = "gluepy.files.storages.google.GoogleStorage"
STORAGE_ROOT = "gs://prod-bucket/data"
```
