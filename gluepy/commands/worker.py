import click
from . import cli


@cli.command()
@click.option(
    "--concurrency",
    "-c",
    type=int,
    default=None,
    help="Number of concurrent worker processes/threads.",
)
@click.option("--loglevel", "-l", type=str, default="info", help="Logging level.")
@click.option(
    "--queues",
    "-Q",
    type=str,
    default=None,
    help="Comma-separated list of queues to consume from.",
)
@click.option(
    "--pool",
    type=str,
    default=None,
    help="Worker pool type (prefork, solo, eventlet, gevent).",
)
def worker(concurrency, loglevel, queues, pool):
    """Start a Celery worker that serves Gluepy DAGs."""
    from gluepy.exec.celery import create_celery_app

    app = create_celery_app()
    argv = ["worker", "--loglevel", loglevel]
    if concurrency:
        argv += ["--concurrency", str(concurrency)]
    if queues:
        argv += ["--queues", queues]
    if pool:
        argv += ["--pool", pool]
    app.worker_main(argv)
