from pathlib import Path
import yaml


def load_config(config_path: str) -> dict:
    """
    Load a PaperPilot YAML configuration file.

    Parameters
    ----------
    config_path : str
        Path to the configuration YAML file.

    Returns
    -------
    dict
        Parsed configuration dictionary.
    """

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Config file must contain a YAML object.")

    validate_config(config)

    return config


def validate_config(config: dict) -> None:
    """
    Perform basic validation of the configuration.
    """

    required_fields = [
        "project_name",
        "level",
        "algorithms",
        "schema_file",
        "prompts",
        "paths",
    ]

    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required config field: {field}")

    level = config["level"]

    if not isinstance(level, int):
        raise ValueError("'level' must be an integer.")

    if level < 0:
        raise ValueError("'level' cannot be negative.")

    algorithms = config["algorithms"]

    if not isinstance(algorithms, list):
        raise ValueError("'algorithms' must be a list.")

    if not algorithms:
        raise ValueError("'algorithms' cannot be empty.")

    for algorithm in algorithms:
        if not isinstance(algorithm, str) or not algorithm.strip():
            raise ValueError(
                "Every item in 'algorithms' must be a non-empty string."
            )


def load_schema(schema_path: str) -> dict:
    """
    Load the schema describing the comparison-table columns.
    """

    path = Path(schema_path)

    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")

    with path.open("r", encoding="utf-8") as file:
        schema = yaml.safe_load(file)

    if not isinstance(schema, dict):
        raise ValueError("Schema file must contain a YAML object.")

    if "columns" not in schema:
        raise ValueError("Schema must contain a 'columns' section.")

    if not isinstance(schema["columns"], dict):
        raise ValueError("'columns' must be a YAML mapping.")

    return schema