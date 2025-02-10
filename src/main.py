import argparse
from typing import List

from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_content_reader import ScriptContentReaderInterface
from src.script_metadata_extractor import ScriptMetadataExtractorInterface


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--readme-paths", nargs="+", type=str, help="Paths to Readme files", default=["README.md"]
    )
    return parser.parse_args()


def main(readme_paths: List[str]) -> None:
    script_metadata_extractor: ScriptMetadataExtractorInterface = ScriptMetadataExtractorInterface()
    script_content_reader: ScriptContentReaderInterface = ScriptContentReaderInterface()
    code_embedder = CodeEmbedder(
        readme_paths=readme_paths,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    code_embedder()
    logger.info("Code Embedder finished successfully.")


if __name__ == "__main__":
    args = parse_arguments()
    main(args.readme_paths)