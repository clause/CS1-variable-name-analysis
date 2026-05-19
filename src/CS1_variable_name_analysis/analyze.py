import asyncio
import csv
from collections.abc import Sequence
from pathlib import Path

import click
from pydantic import BaseModel, Field, TypeAdapter
from rich.progress import track


class Project(BaseModel, frozen=True):
    data: Data
    user_id: int
    model_config = {"extra": "allow"}

    class Data(BaseModel, frozen=True):
        source: str | None = Field(
            default=None,
            alias="/main.py",
        )
        model_config = {"extra": "allow"}


class Violation(BaseModel, frozen=True):
    code: str
    message: str
    location: Location
    end_location: Location
    message: str
    model_config = {"extra": "allow"}

    class Location(BaseModel, frozen=True):
        row: int
        column: int
        model_config = {"extra": "allow"}


async def run(
    subjects: Sequence[tuple[int, str]],
    output: Path,
):
    semaphore = asyncio.Semaphore(20)
    queue = asyncio.Queue[tuple[int, Sequence[Violation]]]()

    async def csv_writer_task():

        with output.open("w") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "id",
                    "code",
                    "start_row",
                    "start_column",
                    "end_row",
                    "end_column",
                    "message",
                ]
            )

            for _ in track(range(len(subjects))):
                user_id, violations = await queue.get()
                for violation in violations:
                    writer.writerow(
                        [
                            user_id,
                            violation.code,
                            violation.location.row,
                            violation.location.column,
                            violation.end_location.row,
                            violation.end_location.column,
                            violation.message,
                        ]
                    )

                queue.task_done()

    async def analysis_task(
        id: int,
        source: str,
    ):
        async with semaphore:
            process = await asyncio.create_subprocess_exec(
                "uvx",
                "ruff",
                "check",
                "-",
                "--stdin-filename",
                "main.py",
                "--output-format",
                "json",
                "--select",
                ",".join(["N"]),
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
            )
            stdout, _stdin = await process.communicate(input=source.encode())

            if stdout:
                violations = TypeAdapter(Sequence[Violation]).validate_json(stdout)
                await queue.put((id, violations))

    async with asyncio.TaskGroup() as tg:
        for id, source in subjects:
            tg.create_task(analysis_task(id, source))

        tg.create_task(csv_writer_task())


@click.command()
@click.option(
    "-o",
    "--output",
    type=click.Path(writable=True, dir_okay=False, path_type=Path),
    default=None,
    help="Output file (defaults to <INPUT>.csv)",
)
@click.argument(
    "input",
    type=click.Path(exists=True, readable=True, dir_okay=False, path_type=Path),
)
def main(
    output: Path | None,
    input: Path,
) -> None:

    output = output or input.with_suffix(".csv")

    projects = TypeAdapter(Sequence[Project]).validate_json(input.read_bytes())

    subjects = [
        (project.user_id, project.data.source)
        for project in projects
        if project.data.source
    ]

    asyncio.run(run(subjects, output))


if __name__ == "__main__":
    main()
