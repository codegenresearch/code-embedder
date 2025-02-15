from loguru import logger

from src.script_content_reader import ScriptContentReaderInterface
from src.script_metadata import ScriptMetadata
from src.script_metadata_extractor import ScriptMetadataExtractorInterface


class CodeEmbedder:
    def __init__(
        self,
        readme_paths: list[str],
        script_metadata_extractor: ScriptMetadataExtractorInterface,
        script_content_reader: ScriptContentReaderInterface,
    ) -> None:
        self._readme_paths = readme_paths
        self._script_metadata_extractor = script_metadata_extractor
        self._script_content_reader = script_content_reader

    def __call__(self) -> None:
        for readme_path in self._readme_paths:
            self._process_readme(readme_path)

    def _process_readme(self, readme_path: str) -> None:
        readme_content = self._read_readme(readme_path)
        if not readme_content:
            logger.info(f"Empty README in path {readme_path}. Skipping.")
            return

        scripts = self._extract_scripts(readme_content=readme_content, readme_path=readme_path)
        if not scripts:
            return

        script_contents = self._script_content_reader.read(scripts=scripts)

        self._update_readme(
            script_contents=script_contents,
            readme_content=readme_content,
            readme_path=readme_path,
        )

    def _read_readme(self, readme_path: str) -> list[str]:
        if not readme_path.endswith(".md"):
            logger.error("README path must end with .md")
            raise ValueError("README path must end with .md")

        with open(readme_path) as readme_file:
            return readme_file.readlines()

    def _extract_scripts(
        self, readme_content: list[str], readme_path: str
    ) -> list[ScriptMetadata] | None:
        scripts = self._script_metadata_extractor.extract(readme_content=readme_content)
        if not scripts:
            logger.info(f"No script paths found in README in path {readme_path}. Skipping.")
            return None
        logger.info(
            f"""Found script paths in README in path {readme_path}:
            {set(script.path for script in scripts)}"""
        )
        return scripts

    def _update_readme(
        self,
        script_contents: list[ScriptMetadata],
        readme_content: list[str],
        readme_path: str,
    ) -> None:
        updated_readme = []
        readme_content_cursor = 0

        for script in sorted(script_contents, key=lambda x: x.readme_start):
            updated_readme += readme_content[readme_content_cursor : script.readme_start + 1]
            updated_readme += script.content + "\n"

            readme_content_cursor = script.readme_end

        updated_readme += readme_content[readme_content_cursor:]

        with open(readme_path, "w") as readme_file:
            readme_file.writelines(updated_readme)
