from pprint import pformat
import click
import yaml

from made.model import MadeModel, JobModelCollection
from made.command import MadeCommand


class MadeController:
    verbose: bool = False

    def __init__(self) -> None:
        self.load_schema()

    def load_schema(self) -> None:
        with open("made-file.yaml") as made_file:
            made_config = yaml.safe_load(made_file)

        self.schema = MadeModel.from_dict(made_config)
        if self.verbose:
            print(f"schema: {pformat(self.schema)}")

    def get_jobs(self) -> JobModelCollection:
        return self.schema.jobs

    def register_job_commands(self) -> click.Group:
        cli = click.Group()
        for job in self.schema.jobs.values():
            command = MadeCommand(job=job)
            cli.add_command(command)

        return cli
