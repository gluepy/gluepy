# Context System

The context system provides hierarchical, YAML-based configuration that is available throughout a DAG run.

## `default_context`

Access the current context anywhere:

```python
from gluepy.conf import default_context

# Access nested values using dot notation
run_id = default_context.gluepy.run_id
run_folder = default_context.gluepy.run_folder
created_at = default_context.gluepy.created_at

# Access custom config values
my_param = default_context.training.learning_rate
```

The context is a `Box` object (from python-box), supporting dot-notation access on nested dicts.

## CONFIG_PATH

YAML files in the `CONFIG_PATH` directory (default: `configs/`) are loaded and merged as the base configuration. Example:

```yaml
# configs/context.yaml
training:
  learning_rate: 0.01
  epochs: 100
  batch_size: 32
```

All `.yaml` and `.yml` files in `CONFIG_PATH` are loaded and merged.

## Run Metadata

Each run automatically gets metadata under `gluepy.*`:

- `gluepy.run_id` - Unique UUID for the run
- `gluepy.run_folder` - Path like `runs/2024/1/15/<run_id>`
- `gluepy.created_at` - UTC timestamp of run creation

## Patch System

Patches override base config values. They are merged left-to-right (later wins):

1. Base configs from `CONFIG_PATH`
2. `--patch` files (loaded via storage backend)
3. `--local-patch` files (loaded from local filesystem)
4. Run metadata

### Storage-based patches (`--patch` / `-p`)
Loaded via `default_storage`. Useful when patch files are stored alongside data (e.g., on GCS or S3).

```bash
python manage.py dag my_dag -p configs/experiment_a.yaml
```

### Local patches (`--local-patch` / `-lp`)
Loaded directly from the local filesystem. Useful for development or when working with remote storage backends.

```bash
python manage.py dag my_dag -lp ./local_overrides.yaml
python manage.py dag my_dag -lp /absolute/path/to/patch.yaml
```

Multiple patches can be combined:
```bash
python manage.py dag my_dag -p remote_patch.yaml -lp ./local_patch.yaml
```

## Retry

When retrying a run, the context from the original run is loaded:

```bash
python manage.py dag my_dag --retry runs/2024/1/15/<run_id>
```

Patches can be applied on top of a retried context.

## DefaultContextManager

The `DefaultContextManager` class handles context creation and loading:

- `create_context()` - Creates a new context from CONFIG_PATH files + patches
- `load_context(path)` - Loads a previously saved context (e.g., for retries)
- `get_run_meta()` - Generates run metadata (run_id, run_folder, created_at)

Custom context managers can be configured via `CONTEXT_BACKEND` setting.
