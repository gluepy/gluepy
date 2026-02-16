import os
import shutil
import click
from . import cli


TARGET_DIRS = {
    "github": os.path.join(".github", "skills", "gluepy"),
    "claude": os.path.join(".claude", "skills", "gluepy"),
    "cursor": os.path.join(".cursor", "skills", "gluepy"),
}


@cli.command()
@click.argument("target", type=click.Choice(["github", "claude", "cursor"]))
def skill(target):
    """Generate Gluepy SKILL.md agent skill in the project."""
    source_dir = os.path.join(os.path.dirname(__file__), "..", "templates", "skill")
    source_dir = os.path.normpath(source_dir)
    dest_dir = TARGET_DIRS[target]

    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    shutil.copytree(source_dir, dest_dir)
    click.secho(f"Created skill files in '{dest_dir}'")
