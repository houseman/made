from __future__ import annotations

import click
import subprocess
import typing as t

if t.TYPE_CHECKING:
    from . import model as m


class MadeCommand(click.Command):
    def __init__(self, job: m.JobModel):
        self.job = job
        super().__init__(name=job.id, help=job.help, callback=self.exec)

    def exec(self) -> tuple:
        click.secho(f"Execute: {self.job.help}!", bold=True)
        command = None
        if self.job.run:
            command = self.job.run
            if self.job.args:
                command = f"{command} {' '.join(self.job.args)}"

        if not command:
            raise Exception(f"Could not resolve command {self.job.id}")
        click.secho(command, bold=True, fg="red")
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        return process.communicate()
