import os
import shutil
import click
from . import cli


TARGET_DIRS = {
    "github": os.path.join(".github", "skills", "gluepy"),
    "claude": os.path.join(".claude", "skills", "gluepy"),
    "cursor": os.path.join(".cursor", "skills", "gluepy"),
}

COMMAND_DIRS = {
    "claude": os.path.join(".claude", "commands"),
    "cursor": os.path.join(".cursor", "commands"),
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

    shutil.copytree(
        source_dir,
        dest_dir,
        ignore=shutil.ignore_patterns("commands"),
    )
    click.secho(f"Created skill files in '{dest_dir}'")

    # Copy command files for targets that support commands
    if target in COMMAND_DIRS:
        commands_source = os.path.join(source_dir, "commands")
        if os.path.isdir(commands_source):
            command_dest = COMMAND_DIRS[target]
            os.makedirs(command_dest, exist_ok=True)
            for filename in os.listdir(commands_source):
                src_file = os.path.join(commands_source, filename)
                if os.path.isfile(src_file):
                    shutil.copy2(src_file, os.path.join(command_dest, filename))
            click.secho(f"Created command files in '{command_dest}'")
