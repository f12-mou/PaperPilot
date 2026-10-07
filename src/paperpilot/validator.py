from typing import Dict, List, Any


ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def validate_table(
    rows: List[Dict[str, Any]],
    schema: Dict,
    expected_methods: List[str],
) -> List[str]:
    """
    Validate the extracted comparison table.

    Returns
    -------
    list[str]
        A list of validation problems.
        An empty list means no problems were found.
    """

    problems = []

    columns = list(schema["columns"].keys())

    if not rows:
        problems.append("The comparison table is empty.")
        return problems

    # Check that every expected method appears exactly once.
    seen_methods = []

    for row in rows:
        method = row.get("method")

        if not method:
            problems.append("A row is missing the 'method' field.")
        else:
            seen_methods.append(method)

    for method in expected_methods:
        count = seen_methods.count(method)

        if count == 0:
            problems.append(f"Missing row for method: {method}")

        elif count > 1:
            problems.append(f"Duplicate rows found for method: {method}")

    # Check every row against the active schema.
    for row_number, row in enumerate(rows, start=1):
        method = row.get("method", f"row_{row_number}")

        for column in columns:
            if column not in row:
                problems.append(
                    f"{method}: missing column '{column}'."
                )
                continue

            value = row[column]

            if value is None or value == "":
                problems.append(
                    f"{method}: empty value for '{column}'."
                )

        # Validate confidence if present in the schema.
        if "confidence" in columns:
            confidence = row.get("confidence")

            if confidence not in ALLOWED_CONFIDENCE:
                problems.append(
                    f"{method}: invalid confidence value "
                    f"'{confidence}'. Expected high, medium, or low."
                )

        # Validate manual verification flag.
        if "needs_manual_verification" in columns:
            flag = row.get("needs_manual_verification")

            if not isinstance(flag, bool):
                problems.append(
                    f"{method}: 'needs_manual_verification' "
                    f"must be true or false."
                )

    return problems


def validate_manifest(
    manifest: Dict,
    expected_methods: List[str],
) -> List[str]:
    """
    Validate the paper manifest.
    """

    problems = []

    for method in expected_methods:

        if method not in manifest:
            problems.append(
                f"No manifest entry found for method: {method}"
            )
            continue

        entry = manifest[method]

        status = entry.get("status")

        if status != "verified":
            problems.append(
                f"{method}: paper status is '{status}', not 'verified'."
            )

        if status == "verified":

            required_metadata = [
                "title",
                "authors",
                "year",
                "venue",
                "source_url",
                "local_file",
            ]

            for field in required_metadata:
                if not entry.get(field):
                    problems.append(
                        f"{method}: manifest is missing '{field}'."
                    )

    return problems