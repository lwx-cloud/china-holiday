import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timedelta, tzinfo
from tempfile import mkstemp
from typing import Iterator
from zipfile import ZipFile

from tqdm import tqdm

from fetch import CustomJSONEncoder, fetch_holiday
from generate_ics import generate_ics
from filetools import workspace_path


class ChinaTimezone(tzinfo):
    def tzname(self, dt):
        return "UTC+8"

    def utcoffset(self, dt):
        return timedelta(hours=8)

    def dst(self, dt):
        return timedelta()


def update_data(year: int) -> Iterator[str]:
    json_filename = workspace_path(f"{year}.json")
    ics_filename = workspace_path(f"{year}.ics")
    with open(json_filename, "w", encoding="utf-8", newline="\n") as f:
        data = fetch_holiday(year)

        json.dump(
            dict(
                (
                    (
                        "$schema",
                        "https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/schema.json",
                    ),
                    (
                        "$id",
                        f"https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/{year}.json",
                    ),
                    *data.items(),
                )
            ),
            f,
            indent=4,
            ensure_ascii=False,
            cls=CustomJSONEncoder,
        )

    yield json_filename
    generate_ics(data["days"], ics_filename)
    yield ics_filename


def update_all_ics(fr_year, to_year):
    all_days = []
    all_papers = set()
    for year in range(fr_year, to_year + 1):
        filename = workspace_path(f"{year}.json")
        if not os.path.isfile(filename):
            continue
        with open(filename, "r", encoding="utf8") as inf:
            data = json.loads(inf.read())
            all_days.extend(data.get("days"))
            all_papers.update(data.get("papers", []))

    filename = workspace_path("all.ics")
    generate_ics(
        all_days,
        filename,
    )
    return filename


def update_all_json(fr_year, to_year):
    all_days = []
    all_papers = []
    for year in range(fr_year, to_year + 1):
        filename = workspace_path(f"{year}.json")
        if not os.path.isfile(filename):
            continue
        with open(filename, "r", encoding="utf8") as inf:
            data = json.loads(inf.read())
            all_days.extend(data.get("days"))
            all_papers.extend(data.get("papers", []))

    all_papers = sorted(list(set(all_papers)))
    all_days = sorted(all_days, key=lambda x: x["date"])

    all_data = {
        "years": {"start": fr_year, "end": to_year},
        "papers": all_papers,
        "days": all_days,
    }

    filename = workspace_path("all.json")
    with open(filename, "w", encoding="utf-8", newline="\n") as f:
        json.dump(
            dict(
                (
                    (
                        "$schema",
                        "https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/all_schema.json",
                    ),
                    (
                        "$id",
                        "https://raw.githubusercontent.com/lwx-cloud/china-holiday/main/all.json",
                    ),
                    *all_data.items(),
                )
            ),
            f,
            indent=4,
            ensure_ascii=False,
            cls=CustomJSONEncoder,
        )
    return filename


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        action="store_true",
        help="Update all years since 2016",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="create new release if repository data is not up to date",
    )
    args = parser.parse_args()

    now = datetime.now(ChinaTimezone())
    is_release = args.release

    start_year = 2016 if args.all else now.year
    filenames = []
    progress = tqdm(range(start_year, now.year + 2))
    for i in progress:
        progress.set_description(f"Updating {i} data")
        filenames += list(update_data(i))
    progress.set_description("Updating all.ics")
    filenames.append(update_all_ics(2016, now.year + 1))
    progress.set_description("Updating all.json")
    filenames.append(update_all_json(2016, now.year + 1))
    print("")

    subprocess.run(["git", "add", *filenames], check=True)
    diff = subprocess.run(
        ["git", "diff", "--stat", "--cached", "*.json", "*.ics"],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    ).stdout
    if not diff:
        print("Already up to date.")
        return

    if not is_release:
        print("Updated repository data, skip release since not specified `--release`")
        return

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            "chore(release): update holiday data",
            "-m",
            "[skip ci]",
        ],
        check=True,
    )
    subprocess.run(["git", "push"], check=True)

    tag = now.strftime("%Y.%m.%d")
    temp_note_fd, temp_note_name = mkstemp()
    with open(temp_note_fd, "w", encoding="utf-8") as f:
        f.write(tag + "\n\n```diff\n" + diff + "\n```\n")
    os.makedirs(workspace_path("dist"), exist_ok=True)
    zip_path = workspace_path("dist", f"china-holiday-{tag}.zip")
    pack_data(zip_path)

    subprocess.run(
        [
            "gh",
            "release",
            "create",
            "-F",
            temp_note_name,
            tag,
            f"{zip_path}#JSON数据",
        ],
        check=True,
    )
    os.unlink(temp_note_name)


def pack_data(file):
    zip_file = ZipFile(file, "w")
    for i in os.listdir(workspace_path()):
        if not re.match(r"\d+\.json", i):
            continue
        zip_file.write(workspace_path(i), i)


if __name__ == "__main__":
    main()
