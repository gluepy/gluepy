---
name: gluepy
description: Gluepy is a Python framework for building data pipelines using DAGs and Tasks, with pluggable storage, context management, and data backends.
---

# Gluepy Framework

Gluepy is a framework for data scientists and engineers to build reproducible data pipelines. It provides a structured way to define DAGs (directed acyclic graphs) of Tasks, manage configuration via a context system, and interact with storage and data backends.

## Core Concepts

### DAGs and Tasks
A **DAG** is an ordered sequence of **Tasks** that execute in order. Each Task performs a unit of work in its `run()` method. DAGs and Tasks auto-register via `__init_subclass__`, so simply defining a subclass makes it available.

See [references/dags.md](references/dags.md) for details.

### Context
The **context** system provides hierarchical YAML-based configuration. Configs are loaded from `CONFIG_PATH`, optionally patched via `--patch` (storage-based) or `--local-patch` (filesystem-based), and merged left-to-right.

See [references/context.md](references/context.md) for details.

### Storage
The **storage** backend abstracts file operations (read, write, copy, list, delete) across local filesystem, GCS, S3, and in-memory backends.

See [references/storage.md](references/storage.md) for details.

### Data Manager
The **data manager** provides `read()` and `write()` methods for DataFrames, routing through the configured storage backend.

See [references/data.md](references/data.md) for details.

### Settings
All configuration is driven by a Python settings module, pointed to by the `GLUEPY_SETTINGS_MODULE` environment variable.

See [references/settings.md](references/settings.md) for details.

## Quick Start

```python
# mymodule/tasks.py
from gluepy.exec import Task

class ExtractTask(Task):
    label = "extract"
    def run(self):
        # your extraction logic
        pass

class TransformTask(Task):
    label = "transform"
    def run(self):
        # your transformation logic
        pass
```

```python
# mymodule/dags.py
from gluepy.exec import DAG
from .tasks import ExtractTask, TransformTask

class MyPipeline(DAG):
    label = "my_pipeline"
    tasks = [ExtractTask, TransformTask]
```

Run via CLI:
```bash
python manage.py dag my_pipeline
```

## Project Structure

A typical Gluepy project:
```
myproject/
  manage.py                # CLI entrypoint
  configs/
    settings.py            # Settings module
    context.yaml           # Base context config
  mymodule/
    dags.py                # DAG definitions
    tasks.py               # Task definitions
    commands.py            # Custom CLI commands (optional)
  data/                    # Default STORAGE_ROOT
```
