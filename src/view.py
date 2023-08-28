import click
from controller import MadeController


controller = MadeController()


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enables verbose mode.")
def list(verbose: bool) -> None:
    controller.verbose = verbose


@list.command()
def jobs() -> None:
    """List all jobs"""

    click.secho("Usage: made <job>", fg="green", bold=True)
    click.secho("Jobs:", fg="white", bold=True)
    jobs = controller.get_jobs()
    for id, job in jobs.items():
        click.secho(f"\t{job.id}", bold=True, fg="green", nl=False)
        click.secho(f"\t{job.help}", fg="blue")


# cli = click.CommandCollection(sources=[list, controller.register_job_commands])
cli = controller.register_job_commands()
