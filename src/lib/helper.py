import csv
import re
import sys
from datetime import datetime
from itertools import islice
from time import time

import requests
from pathlib import Path
from typing import List, Optional, Dict, Any, Iterator

from bs4 import BeautifulSoup


def current_date_str() -> str:
    dt = datetime.today()
    return "%04d%02d%02d" % (dt.year, dt.month, dt.day)


def find_latest_version(pattern: str, parent_dir: Path) -> Path:
    version_dirs: List[Path] = [
        path for path in parent_dir.iterdir() if re.search(pattern, str(path))
    ]
    version_dirs = sorted(version_dirs, key=lambda path: str(path), reverse=True)
    return version_dirs[0]


def find_filepath(parent_dir: Path, suffix: str) -> Optional[Path]:
    for path in parent_dir.iterdir():
        if path.is_file() and path.suffix == suffix:
            return path


def find_latest_source_file(parent_dir: Path, suffix: str) -> Path:
    version_dir: Path = find_latest_version("[\d]{8}$", parent_dir)
    file = find_filepath(parent_dir=version_dir, suffix=suffix)
    assert file
    return file


def read_html(url: str) -> str:
    r = requests.get(url)
    return r.text


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")


def parse_cache_html(filepath: Path) -> BeautifulSoup:
    html: str = filepath.open().read()
    return parse_html(html)


def import_dicts_from_csv(filepath: Path) -> List[Dict[str, Any]]:
    with filepath.open("r") as f:
        reader = csv.DictReader(f)
        return [r for r in reader]


def export_dicts_to_csv(
    filepath: Path, records: Iterator[Dict[str, Any]], fieldnames: List[str] = None
):
    first = records.__next__()
    if fieldnames is None:
        fieldnames = [k for k in first.keys()]

    with filepath.open("w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(first)
        for i, record in enumerate(records):
            print("\r {0:d} ".format(i + 1), end="")
            writer.writerow(record)

def split_every(n, iterable) -> Iterator[List]:
    i = iter(iterable)
    piece = list(islice(i, n))
    count = 0
    while piece:
        count += len(piece)
        print("\r {0:d} ".format(count), end="")
        yield piece
        piece = list(islice(i, n))


def make_now() -> datetime:
    return datetime.now()


class Timer:
    def __init__(self):
        self.start_time = 0
        self.stop_time = 0
        self.lap_time = 0
        self.lap_times = {}

    def start(self):
        self.start_time = time()

    def stop(self):
        if self.start_time == 0:
            print("First call start()!!!")
            sys.exit()

        self.stop_time = time()

    def print_time(self):
        if self.start_time == 0:
            print("First call start()!!!")
            sys.exit()
        elif self.stop_time == 0:
            self.stop_time = time()

        processing_time = self.stop_time - self.start_time
        print("Time:{0}s".format(round(processing_time)))

    def lap(self, process_name: str):
        if self.start_time == 0:
            print("First call start()!!!")
            sys.exit()

        self.lap_time = time()
        self.lap_times[process_name] = round(self.lap_time - self.start_time)

    def print_processing_times(self):
        print("")
        print("##### processing time")
        cumulative_time = 0
        for process_name, lap_time in self.lap_times.items():
            print(process_name, "{0}s".format(lap_time - cumulative_time))
            cumulative_time = lap_time
