import argparse
from loguru import logger
from src.code_embedding import CodeEmbedder, ScriptMetadataExtractor, ScriptContentReader

class CommandLineInterface:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument(
            "--readme-paths", nargs="+", type=str, help="Paths to Readme files", default=["README.md"]
        )
        self.args = self.parser.parse_args()

    def run(self):
        script_metadata_extractor = ScriptMetadataExtractor()
        script_content_reader = ScriptContentReader()
        code_embedder = CodeEmbedder(
            readme_paths=self.args.readme_paths,
            script_metadata_extractor=script_metadata_extractor,
            script_content_reader=script_content_reader,
        )
        code_embedder()
        logger.info("Code Embedder finished successfully.")

if __name__ == "__main__":
    cli = CommandLineInterface()
    cli.run()