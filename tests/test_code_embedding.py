import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor


@pytest.mark.parametrize(
    "readme_content, expected",
    [
        (
            [":main.py", "print('Hello, World!')", ""],
            [ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content="print('Hello, World!')\n")],
        ),
        (["", "print('Hello, World!')", ""], []),
        ([], []),
        (["", "print('Hello, World!')", ""], []),
        (
            [
                ":example.py",
                "import os",
                "print('Hello, World!')",
                "",
                "",
                "print('Do not replace')",
                "",
            ],
            [ScriptMetadata(readme_start=0, readme_end=3, path="example.py", content="import os\nprint('Hello, World!')\n")],
        ),
        (
            [
                ":main.py",
                "print('Hello, World!')",
                "",
                ":example.py",
                "import os",
                "print('Hello, World!')",
                "",
                "",
                "print('Do not replace')",
                "",
            ],
            [
                ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content="print('Hello, World!')\n"),
                ScriptMetadata(readme_start=3, readme_end=6, path="example.py", content="import os\nprint('Hello, World!')\n"),
            ],
        ),
    ],
    ids=[
        "one_tagged_script",
        "one_untagged_script",
        "empty_readme",
        "one_untagged_script_language_specified",
        "one_tagged_script_one_untagged_script",
        "two_tagged_scripts_one_untagged_script",
    ],
)
def test_script_metadata_extractor(
    readme_content: list[str], expected: list[ScriptMetadata]
) -> None:
    script_metadata_extractor = ScriptMetadataExtractor()
    result = script_metadata_extractor.extract(readme_content=readme_content)
    assert result == expected


def test_code_embedder(tmp_path) -> None:
    original_paths = [
        "tests/data/readme0.md",
        "tests/data/readme1.md",
        "tests/data/readme2.md",
    ]
    expected_paths = [
        "tests/data/expected_readme0.md",
        "tests/data/expected_readme1.md",
        "tests/data/expected_readme2.md",
    ]

    # Create a temporary copy of the original file
    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        with open(original_path) as readme_file:
            temp_readme_path.write_text(readme_file.read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(temp_readme_path) for temp_readme_path in temp_readme_paths],
        script_metadata_extractor=ScriptMetadataExtractor(),
        script_content_reader=ScriptContentReader(),
    )

    code_embedder()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path) as expected_file:
            expected_readme_content = expected_file.readlines()

        with open(temp_readme_path) as updated_file:
            updated_readme_content = updated_file.readlines()

        assert expected_readme_content == updated_readme_content


To address the feedback on the `ScriptMetadataExtractor`, I have updated the test cases to expect the correct content with newline characters. The `extract` method in `ScriptMetadataExtractor` should be implemented to correctly parse the `readme_content` and extract the script metadata as described in the feedback. Here is a possible implementation for the `extract` method:


class ScriptMetadataExtractor:
    def extract(self, readme_content: list[str]) -> list[ScriptMetadata]:
        metadata_list = []
        current_metadata = None
        content_lines = []

        for index, line in enumerate(readme_content):
            if line.startswith(""):
                if current_metadata:
                    current_metadata.content = "".join(content_lines)
                    metadata_list.append(current_metadata)
                    content_lines = []

                if ":" in line:
                    parts = line.split(":")
                    if len(parts) > 1:
                        path = parts[1].strip()
                        current_metadata = ScriptMetadata(readme_start=index, path=path, content="")
            elif current_metadata:
                content_lines.append(line + "\n")

        if current_metadata:
            current_metadata.content = "".join(content_lines)
            current_metadata.readme_end = len(readme_content) - 1
            metadata_list.append(current_metadata)

        return metadata_list


This implementation should correctly parse the `readme_content` and extract the script metadata as expected by the test cases.