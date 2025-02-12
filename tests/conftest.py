from src.script_metadata import ScriptMetadata


class ScriptMetadataFactory:
    @staticmethod
    def create(
        start: int, end: int, path: str, extraction_part: str | None = None
    ) -> ScriptMetadata:
        return ScriptMetadata(
            readme_start=start,
            readme_end=end,
            path=path,
            extraction_part=extraction_part,
            content="",
        )