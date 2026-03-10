import os
import json
import logging
from io import StringIO
from pathlib import Path
from typing import List, Optional
import time
import yaml
import click
from gluepy.conf import default_context_manager, default_context
from gluepy.files.storages import default_storage
from gluepy.ops import default_mlops
from . import cli

logger = logging.getLogger(__name__)


@cli.command()
@click.option("--task", type=str)
@click.option("--from-task", type=str)
@click.option("--patch", "-p", type=str, multiple=True)
@click.option("--local-patch", "-lp", type=str, multiple=True)
@click.option("--retry", type=str)
@click.option("--skip-eval", is_flag=True, default=False, help="Skip evaluation tasks")
@click.option(
    "--eval-only",
    is_flag=True,
    default=False,
    help="Run only evaluation tasks (requires --retry)",
)
@click.option(
    "--compare", type=str, multiple=True, help="Compare metrics across run folders"
)
@click.argument("label")
def dag(
    label,
    retry: Optional[str] = None,
    patch: Optional[List[str]] = None,
    local_patch: Optional[List[str]] = None,
    from_task: Optional[str] = None,
    task: Optional[str] = None,
    skip_eval: bool = False,
    eval_only: bool = False,
    compare: Optional[tuple] = None,
):
    """Wrapper around run_dag function to expose to CLI"""
    run_dag(
        label,
        retry,
        patch,
        from_task,
        task,
        local_patch=local_patch,
        skip_eval=skip_eval,
        eval_only=eval_only,
        compare=compare,
    )


def run_dag(
    label,
    retry: Optional[str] = None,
    patch: Optional[List[str]] = None,
    from_task: Optional[str] = None,
    task: Optional[str] = None,
    local_patch: Optional[List[str]] = None,
    skip_eval: bool = False,
    eval_only: bool = False,
    compare: Optional[tuple] = None,
):
    """Command to run a DAG by its label.

    Args:
        label (str): The label of the DAG to execute.
        retry (Optional[str], optional): Path to existing run_folder of a run to retry.
          Defaults to None.
        patch (Optional[List[str]], optional): Path to patch YAML file to override
            context with. Defaults to None.
        from_task (Optional[str], optional): Label of task in DAG to retry from.
            Defaults to None.
        task (Optional[str], optional): Label of task if only want to execute a
            single task in DAG. Defaults to None.
        local_patch (Optional[List[str]], optional): Path to local patch YAML files
            to override context with. Defaults to None.
        skip_eval (bool): If True, skip evaluation tasks.
        eval_only (bool): If True, run only evaluation tasks (requires retry).
        compare (Optional[tuple]): Run folders to compare metrics across.

    """
    DAG = _get_dag_by_label(label)
    assert not (from_task and task), "Only one of --from-task or --task can be set."
    assert not (
        skip_eval and eval_only
    ), "--skip-eval and --eval-only are mutually exclusive."
    assert not (eval_only and not retry), "--eval-only requires --retry."
    retry = retry if retry is None else retry.strip(default_storage.separator)

    if compare:
        _compare_runs(label, list(compare))
        return

    local_patch_dicts = []
    if local_patch:
        for lp in local_patch:
            lp_path = Path(lp) if os.path.isabs(lp) else Path(os.getcwd()) / lp
            if not lp_path.exists():
                logger.warning(f"Local patch '{lp}' was not found.")
                continue
            with open(lp_path) as f:
                local_patch_dicts.append(yaml.load(f, Loader=yaml.SafeLoader))

    if retry and default_storage.exists(os.path.join(retry, "context.yaml")):
        default_context_manager.load_context(
            os.path.join(retry, "context.yaml"),
            patches=list(patch),
            local_patches=local_patch_dicts or None,
        )
    elif retry:
        # Retry a run folder path that does not exist by creating it.
        default_context_manager.create_context(
            run_id=os.path.basename(retry),
            run_folder=retry,
            patches=list(patch) if patch else None,
            local_patches=local_patch_dicts or None,
            evaluate_lazy=True,
        )
    elif patch or local_patch_dicts:
        default_context_manager.create_context(
            patches=list(patch) if patch else None,
            local_patches=local_patch_dicts or None,
            evaluate_lazy=True,
        )

    dag_instance = DAG()
    tasks = dag_instance.inject_tasks(skip_eval=skip_eval, eval_only=eval_only)

    if task:
        tasks = [_get_task_by_label(task)]

    if from_task:
        Task = _get_task_by_label(from_task)
        for i, t in enumerate(tasks):
            if t is Task:
                pos = i
                break
        else:
            raise ValueError(f"Task '{from_task}' not found in DAG list of tasks.")
        tasks = tasks[pos:]

    default_mlops.create_run(dag=label, config=default_context.to_dict())

    for t in tasks:
        logger.info(f"---------- Started task '{t.__name__}'")
        time_start = time.time()
        t().run()
        time_end = time.time()
        logger.info(
            f"---------- Completed task '{t.__name__}' in "
            f"{'{:f}'.format(time_end-time_start)} seconds"
        )

    if (not skip_eval and dag_instance.eval_tasks) or eval_only:
        metrics = default_mlops.get_metrics()
        if metrics:
            print("=== GLUEPY METRICS ===")
            for key, value in metrics.items():
                print(f"metric:{key}={value}")
            print("=== END METRICS ===")
            default_storage.touch(
                default_storage.runpath("metrics.json"),
                StringIO(json.dumps(metrics, indent=2)),
            )


def _compare_runs(label, run_folders):
    """Compare metrics across multiple run folders."""
    all_metrics = {}
    all_keys = set()
    for folder in run_folders:
        folder = folder.strip(default_storage.separator)
        metrics_path = os.path.join(folder, "metrics.json")
        if default_storage.exists(metrics_path):
            content = default_storage.open(metrics_path, mode="r")
            metrics = json.loads(content)
            all_metrics[folder] = metrics
            all_keys.update(metrics.keys())
        else:
            logger.warning(f"No metrics.json found in '{folder}'")
            all_metrics[folder] = {}

    if not all_keys:
        print("No metrics found in any of the specified run folders.")
        return

    sorted_keys = sorted(all_keys)
    header = "run_folder\t" + "\t".join(sorted_keys)
    print(header)
    for folder in run_folders:
        folder = folder.strip(default_storage.separator)
        values = [str(all_metrics[folder].get(k, "N/A")) for k in sorted_keys]
        print(f"{folder}\t" + "\t".join(values))


def _get_dag_by_label(label):
    from gluepy.exec import DAG_REGISTRY

    try:
        DAG = DAG_REGISTRY[label]
    except KeyError:
        raise ValueError(f"DAG with label '{label}' was not found in registry.")

    return DAG


def _get_task_by_label(label):
    from gluepy.exec import TASK_REGISTRY

    try:
        Task = TASK_REGISTRY[label]
    except KeyError:
        raise ValueError(f"Task with label '{label}' was not found in registry.")

    return Task
