from __future__ import annotations

import subprocess
import typing as t

import click

if t.TYPE_CHECKING:
    from . import model as m


class JobRunner:
    COMMANDS: dict[str, MadeCommand] = {}

    @classmethod
    def add_command(cls, command: MadeCommand) -> None:
        cls.COMMANDS[command.job.id] = command


class MadeCommand(click.Command):
    def __init__(self, job: m.JobModel):
        self.job = job
        self.executable = self.build_executable()
        super().__init__(name=job.id, help=job.help, callback=self.exec)
        JobRunner.add_command(command=self)

    def build_executable(self) -> t.Optional[str]:
        print(f"JOB: {self.job}")
        if self.job.run:
            if isinstance(self.job.run, str):
                executable = self.job.run
                if self.job.args:
                    executable = f"{executable} {' '.join(self.job.args)}"

                return executable
            return None
        raise Exception("Could not build command")

    def exec(self) -> tuple:
        click.secho(f"Run job: {self.job.help}!", bold=True)

        if not self.executable:
            raise Exception(f"Could not resolve command for {self.job.id}")
        click.secho(self.executable, bold=True, fg="red")
        process = subprocess.Popen(self.executable, stdout=subprocess.PIPE, shell=True)

        return process.communicate()
