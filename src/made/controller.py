from pprint import pformat
import click
import yaml

from . import model as m
from .command import MadeCommand


class MadeController:
    verbose: bool = False

    def __init__(self) -> None:
        self.load_schema()

    def load_schema(self) -> None:
        with open("made-file.yaml") as made_file:
            made_config = yaml.safe_load(made_file)

        self.model = m.MadeModel.from_dict(made_config)
        if self.verbose:
            print(f"model: {pformat(self.model)}")

    def get_jobs(self) -> m.JobModelCollection:
        return self.model.jobs

    def register_job_commands(self) -> click.Group:
        cli = click.Group("commands")
        for job in self.model.jobs.values():
            command = MadeCommand(job=job)
            cli.add_command(command)

        return cli
