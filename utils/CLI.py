from datetime import datetime, timedelta
from math import floor, log10
from os import environ, getcwd
from subprocess import run

from halo import Halo
from log_symbols import LogSymbols


def exec(command: list[str], workspace=getcwd()):
    result = run(command, env=environ, capture_output=True, cwd=workspace)

    if result.returncode != 0:
        if result.stderr.decode() != "":
            raise RuntimeError(result.stderr.decode())
        else:
            raise RuntimeError(result.stdout.decode())

    return result.stdout.decode()


def format_duration(duration: timedelta, lpad=True, decimal_places=3):
    result = str(round(duration.total_seconds(), decimal_places))
    result = result + "0" * (decimal_places - len(result.split(".")[1]))
    result = " " * -(len(result) - decimal_places - 1 - 3) + result if lpad else result
    return f"{result}s"


def print_info(text: str, indent=2):
    print(f"{' ' * indent}{LogSymbols.INFO.value} {text}")


class Step:
    def __init__(self, text: str, success_text: str = "Done"):
        self.spinner = Halo(text=text, spinner="moon")
        self.success_text = success_text

    def __enter__(self):
        self.spinner.start()
        self.start = datetime.now()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.spinner.fail(str(exc_value))
        else:
            self.spinner.succeed(
                text=f"{self.success_text} in {format_duration(datetime.now() - self.start, lpad=False)}"
            )
