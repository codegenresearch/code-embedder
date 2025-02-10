import argparse
from typing import List

from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor


parser = argparse.ArgumentParser()
parser.add_argument(
    "--readme-paths", nargs="+", type=str, help="Paths to Readme files", default="README.md"
)


def main() -> None:
    args = parser.parse_args()
    readme_paths = args.readme_paths if isinstance(args.readme_paths, list) else [args.readme_paths]

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    code_embedder = CodeEmbedder(
        readme_paths=readme_paths,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    code_embedder()
    logger.info("Code Embedder finished successfully.")


if __name__ == "__main__":
    main()