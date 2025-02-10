from src.script_metadata import ScriptMetadata


def create_script_metadata(
    start: int, end: int, path: str, extraction_part: str | None = None, content: str = ""
) -> ScriptMetadata:
    """
    Creates a ScriptMetadata object with the provided parameters.

    :param start: The starting line number of the script in the README.
    :param end: The ending line number of the script in the README.
    :param path: The path to the script file.
    :param extraction_part: An optional section identifier for the script.
    :param content: The content of the script.
    :return: A ScriptMetadata object containing the script's metadata.
    """
    return ScriptMetadata(
        readme_start=start,
        readme_end=end,
        path=path,
        extraction_part=extraction_part,
        content=content,
    )