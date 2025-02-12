import argparse
from typing import List

from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractorInterface
from src.script_content_reader import ScriptContentReaderInterface


class CommandLineInterface:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--readme-paths",
            nargs="+",
            type=str,
            help="Paths to Readme files",
            default=["README.md"]
        )

    def parse_arguments(self) -> argparse.Namespace:
        return self.parser.parse_args()


class Application:
    def __init__(
        self,
        readme_paths: List[str],
        script_metadata_extractor: ScriptMetadataExtractorInterface,
        script_content_reader: ScriptContentReaderInterface,
    ) -> None:
        self.code_embedder = CodeEmbedder(
            readme_paths=readme_paths,
            script_metadata_extractor=script_metadata_extractor,
            script_content_reader=script_content_reader,
        )

    def run(self) -> None:
        self.code_embedder()
        logger.info("Code Embedder finished successfully.")


if __name__ == "__main__":
    cli = CommandLineInterface()
    args = cli.parse_arguments()

    script_metadata_extractor = ScriptMetadataExtractorInterface()
    script_content_reader = ScriptContentReaderInterface()

    app = Application(
        readme_paths=args.readme_paths,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    app.run()