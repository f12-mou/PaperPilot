import csv
import json
from pathlib import Path
from typing import Any, Dict, List


def ensure_directory(path: str) -> Path:
    """
    Create a directory if it does not already exist.
    """
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_json(data: Any, output_path: str) -> None:
    """
    Save Python data as formatted JSON.
    """
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def load_json(input_path: str) -> Any:
    """
    Load JSON data from disk.
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {input_path}")

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_csv(
    rows: List[Dict[str, Any]],
    output_path: str,
    columns: List[str],
) -> None:
    """
    Save comparison-table rows as CSV.

    The column order is determined by the active schema.
    """
    path = Path(output_path)

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def save_changelog(
    changes: List[Dict[str, Any]],
    output_path: str,
) -> None:
    """
    Save revision history as CSV.
    """

    columns = [
        "method",
        "field",
        "previous_value",
        "new_value",
        "reason",
        "critic_level",
        "evidence",
        "revision_status",
    ]

    save_csv(
        rows=changes,
        output_path=output_path,
        columns=columns,
    )