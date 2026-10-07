from pathlib import Path
from typing import Dict, Any, List

from .config import load_schema
from .exporter import (
    ensure_directory,
    load_json,
    save_json,
    save_csv,
)
from .validator import validate_manifest, validate_table


def create_run_directory(config: Dict[str, Any]) -> Path:
    """
    Create a directory for the current PaperPilot run.
    """

    project_name = config["project_name"]

    safe_name = (
        project_name.lower()
        .replace(" ", "_")
        .replace("/", "_")
    )

    output_root = Path(config["paths"]["output_dir"])
    run_dir = output_root / safe_name

    ensure_directory(str(run_dir))
    ensure_directory(str(run_dir / "reviews"))

    return run_dir


def check_manifest(config: Dict[str, Any]) -> List[str]:
    """
    Check whether Claude Code successfully found and verified
    all requested papers.
    """

    manifest_path = config["paths"]["manifest_file"]

    manifest = load_json(manifest_path)

    problems = validate_manifest(
        manifest=manifest,
        expected_methods=config["algorithms"],
    )

    return problems


def save_initial_table(
    rows: List[Dict[str, Any]],
    schema: Dict[str, Any],
    run_dir: Path,
) -> None:
    """
    Save the initial extraction as table_v0.csv.
    """

    columns = list(schema["columns"].keys())

    save_csv(
        rows=rows,
        output_path=str(run_dir / "table_v0.csv"),
        columns=columns,
    )


def validate_current_table(
    rows: List[Dict[str, Any]],
    schema: Dict[str, Any],
    config: Dict[str, Any],
) -> List[str]:
    """
    Run deterministic validation on a comparison table.
    """

    return validate_table(
        rows=rows,
        schema=schema,
        expected_methods=config["algorithms"],
    )


def prepare_pipeline(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare the PaperPilot run.

    This loads the schema, creates output directories,
    and validates the paper manifest.

    Claude Code stages will later plug into this pipeline.
    """

    schema = load_schema(config["schema_file"])

    run_dir = create_run_directory(config)

    manifest_problems = check_manifest(config)

    result = {
        "schema": schema,
        "run_dir": run_dir,
        "manifest_problems": manifest_problems,
    }

    return result


def describe_pipeline(config: Dict[str, Any]) -> None:
    """
    Print the pipeline that will be executed.
    """

    level = config["level"]

    print()
    print("PaperPilot")
    print("=" * 40)

    print("Stage 0: Find and verify papers")
    print("Stage 1: Initial Claude extraction")

    for iteration in range(1, level + 1):
        print(
            f"Level {iteration}: "
            "critic -> Claude revision"
        )

    print("Final stage: validate and export")
    print()


def run_pipeline(config: Dict[str, Any]) -> None:
    """
    Main PaperPilot pipeline controller.

    At this stage of development, this function prepares
    and validates the workflow.

    Claude Code execution and critic iterations will be
    connected later.
    """

    describe_pipeline(config)

    state = prepare_pipeline(config)

    run_dir = state["run_dir"]

    print(f"Output directory: {run_dir}")

    problems = state["manifest_problems"]

    if problems:
        print()
        print("Paper manifest is not ready:")

        for problem in problems:
            print(f"  - {problem}")

        print()
        print(
            "Paper discovery must complete before "
            "the extraction stage can run."
        )

        return

    print()
    print("All requested papers are verified.")
    print("PaperPilot is ready for extraction.")