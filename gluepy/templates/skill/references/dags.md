# DAGs and Tasks

## DAG

A DAG (Directed Acyclic Graph) groups an ordered list of Tasks into a pipeline.

```python
from gluepy.exec import DAG
from .tasks import CleanTask, TrainTask

class TrainingPipeline(DAG):
    label = "training"
    tasks = [CleanTask, TrainTask]
```

### Key attributes
- `label` (str): Identifier used to run the DAG from CLI. Defaults to lowercase class name.
- `tasks` (list): Ordered list of Task classes to execute.
- `extra_options` (dict): Additional options specific to this DAG.

### Auto-registration
DAGs auto-register via `__init_subclass__`. When you define a DAG subclass, it is added to `DAG_REGISTRY` and becomes available to the CLI. Duplicate labels raise `KeyError`.

### `inject_tasks()`
Returns the full task list including the `START_TASK` (default: `BootstrapTask`) prepended before user-defined tasks.

## Task

A Task is a single step in a DAG. Implement the `run()` method.

```python
from gluepy.exec import Task
from gluepy.files.data import data_manager

class CleanTask(Task):
    label = "clean"
    def run(self):
        df = data_manager.read("raw/input.csv", root=True)
        df = df.dropna()
        data_manager.write("cleaned.csv", df)
```

### Auto-registration
Like DAGs, Tasks auto-register via `__init_subclass__` into `TASK_REGISTRY`.

### BootstrapTask
The default `START_TASK` (`gluepy.exec.tasks.BootstrapTask`) runs before all user tasks. It logs the run ID and run folder, and serializes the context to `context.yaml` in the run folder.

## CLI Execution

```bash
# Run a full DAG
python manage.py dag <label>

# Run a single task from a DAG
python manage.py dag <label> --task <task_label>

# Run from a specific task onwards
python manage.py dag <label> --from-task <task_label>

# Retry a previous run
python manage.py dag <label> --retry <run_folder>

# Apply config patches
python manage.py dag <label> --patch path/to/patch.yaml
python manage.py dag <label> --local-patch ./local_patch.yaml
```

## Passing Data Between Tasks

Tasks share data by writing to and reading from storage:

```python
class ProduceTask(Task):
    def run(self):
        df = pd.DataFrame({"col": [1, 2, 3]})
        data_manager.write("intermediate.csv", df)

class ConsumeTask(Task):
    def run(self):
        df = data_manager.read("intermediate.csv")
```

Files written without `root=True` are stored relative to the current run folder, keeping runs isolated.
