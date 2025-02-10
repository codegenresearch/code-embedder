import argparse
from loguru import logger

from src.code_embedding import CodeEmbedder
from src.script_metadata_extractor import ScriptMetadataExtractor
from src.script_content_reader import ScriptContentReader

def main():
    parser = argparse.ArgumentParser(description="Embed code snippets into README files.")
    parser.add_argument(
        "--readme-paths", 
        nargs="+", 
        type=str, 
        help="Paths to README files", 
        default=["README.md"]
    )
    args = parser.parse_args()

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()
    
    code_embedder = CodeEmbedder(
        readme_paths=args.readme_paths,
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )
    
    code_embedder()
    logger.info("Code Embedder finished successfully.")

if __name__ == "__main__":
    main()