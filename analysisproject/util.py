#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions used throughout this project.
"""


import subprocess
from datetime import datetime as dt
from pathlib import Path

import yaml

from analysisproject.definitions import PROJECT_BASE_DIRECTORY


def find_file(*args, **kwargs):
    """Return file path relative to project directory."""
    return Path(PROJECT_BASE_DIRECTORY, *args, **kwargs)


def find_data_file(*args, **kwargs):
    """Return file path relative to data/ directory."""
    return find_file("data", *args, **kwargs)


def read_config(name):
    """Read config YAML file and return contents as a dict."""
    ConfigFile = find_file("config", name).with_suffix(".yaml")
    with open(ConfigFile) as f:
        config = yaml.safe_load(f)
    return config


def run_command(command):
    """Run shell command in project directory and capture output."""
    process = subprocess.run(
        command, cwd=find_file(), stdout=subprocess.PIPE
    )
    return process.stdout.decode("utf8").strip()


def get_git_hash():
    """Get the identifier of the last commit in the repo."""
    return run_command(["git", "rev-parse", "HEAD"])


def get_last_commit_date():
    """Get the date of the last commit in the repo."""
    return run_command(["git", "log", "-1", "--format=%cd"])


def make_description():
    """Create a string including the script name and git info."""
    import __main__
    script = Path(__main__.__file__).resolve()  # get script name
    git_hash = get_git_hash()
    date = get_last_commit_date()
    return f"{script} @ {git_hash} (last commit date: {date})"


def save_plot(fig, title, *, subdir=".", formats=(".png", ".pdf")):
    """Save figure in multiple formats to fig directory."""

    # Create directory, and don't complain if it already exists
    directory = find_file("fig", subdir)
    directory.mkdir(parents=True, exist_ok=True)

    metadata = {"Creator": make_description()}
    for fmt in formats:
        filename = (directory / title).with_suffix(fmt)
        fig.savefig(filename, metadata=metadata)
        print(f"Wrote {filename}")


def save_plot_with_date(*args, **kwargs):
    today = dt.strftime(dt.today(), "%Y%m%d")
    save_plot(*args, subdir=today, **kwargs)


if __name__ == "__main__":
    # Print a small example if this file is run
    print("config/datasets.yaml contains the following:\n    ", read_config("datasets"))
    print("Example description string:\n    ", make_description())
