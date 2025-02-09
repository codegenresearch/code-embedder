from src.script_metadata import ScriptMetadata


def generate_script_metadata(
    start_line: int, end_line: int, file_path: str, extraction_section: str | None = None
) -> ScriptMetadata:
    """
    Generates a ScriptMetadata object with the provided parameters.

    :param start_line: The starting line number of the script in the README.
    :param end_line: The ending line number of the script in the README.
    :param file_path: The path to the script file.
    :param extraction_section: An optional section identifier for the script.
    :return: A ScriptMetadata object containing the script's metadata.
    """
    return ScriptMetadata(
        readme_start=start_line,
        readme_end=end_line,
        path=file_path,
        extraction_part=extraction_section,
        content="",
    )