import json
import re
from datetime import timedelta

from utils.CLI import Step, exec, format_duration, print_info

BLOCKS = [
    " ",
    "▁",
    "▂",
    "▃",
    "▄",
    "▅",
    "▆",
    "▇",
    "█",
]


def generate_ninja_trace(
    workspace: str, cmake_build_dir: str, trace_filename="trace.json"
):
    with Step(
        text="Generating Ninja trace...",
        success_text=f"Generated `{workspace}/{trace_filename}`",
    ):
        trace = exec(
            command=["ninjatracing", f"{cmake_build_dir}/.ninja_log"],
            workspace=workspace,
        )

        with open(f"{workspace}/{trace_filename}", "w+") as trace_log:
            trace_log.write(trace)


def parse_ninja_trace(
    workspace: str,
    trace_filename="trace.json",
    filter_in_regexes=[r".*\.o$"],
    filter_out_regexes=[r"a^"],
):
    filter_in_patterns = [re.compile(regex) for regex in filter_in_regexes]
    filter_out_patterns = [re.compile(regex) for regex in filter_out_regexes]

    with Step(
        text=f"Parsing `{trace_filename}`...",
        success_text=f"Parsed `{workspace}/{trace_filename}`",
    ):
        with open(f"{workspace}/{trace_filename}", "r") as trace_log:
            trace = json.loads(trace_log.read())

        for pattern in filter_in_patterns:
            trace = [entry for entry in trace if pattern.match(entry["name"])]

        for pattern in filter_out_patterns:
            trace = [entry for entry in trace if not pattern.match(entry["name"])]

        durations = sorted(
            [timedelta(microseconds=float(entry["dur"])) for entry in trace]
        )
        min_duration = min(durations)
        max_duration = max(durations)
        mean_duration = timedelta(
            seconds=sum([x.total_seconds() for x in durations]) / len(durations)
        )
        median_duration = durations[len(durations) // 2]

        duration_range = max_duration - min_duration

        distribution_width = 23
        quantised_durations = [
            (
                round(
                    (
                        (duration - min_duration) / duration_range
                        if duration_range.total_seconds() > 0
                        else 0.5
                    )
                    * (distribution_width - 1)
                )
            )
            for duration in durations
        ]
        counts = [quantised_durations.count(i) for i in range(distribution_width)]
        normalised_counts = [count / max(counts) for count in counts]
        distribution = "".join(
            [BLOCKS[round(count * (len(BLOCKS) - 1))] for count in normalised_counts]
        )

    def entry_with_duration(duration: timedelta):
        return next(
            entry["name"]
            for entry in trace
            if timedelta(microseconds=float(entry["dur"])) == duration
        )

    print_info(
        f"Min:          {format_duration(min_duration)}  `{entry_with_duration(min_duration)}`"
    )
    print_info(
        f"Max:          {format_duration(max_duration)}  `{entry_with_duration(max_duration)}`"
    )
    print_info(
        f"Median:       {format_duration(median_duration)}  `{entry_with_duration(median_duration)}`"
    )
    print_info(f"Mean:         {format_duration(mean_duration)}")
    print_info(f"Distribution:   |{distribution}|")
    print_info(f"TU Count:       {len(trace)}")
