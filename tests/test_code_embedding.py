import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata
from src.script_content_reader import ScriptContentReader
from src.script_metadata_extractor import ScriptMetadataExtractor


def create_script_metadata(readme_start, readme_end, path, content=""):
    return ScriptMetadata(readme_start=readme_start, readme_end=readme_end, path=path, content=content)


test_cases = [
    pytest.param(
        [":main.py", "print('Hello, World!')", ""],
        [create_script_metadata(0, 2, "main.py")],
        id="one_tagged_script",
    ),
    pytest.param(["", "print('Hello, World!')", ""], [], id="one_untagged_script"),
    pytest.param([], [], id="empty_readme"),
    pytest.param(
        ["", "print('Hello, World!')", ""], [],
        id="one_untagged_script_language_specified",
    ),
    pytest.param(
        [
            ":example.py",
            "import os",
            "print('Hello, World!')",
            "",
            "",
            "print('Do not replace')",
            "",
        ],
        [create_script_metadata(0, 3, "example.py")],
        id="one_tagged_script_one_untagged_script",
    ),
    pytest.param(
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
            create_script_metadata(0, 2, "main.py"),
            create_script_metadata(3, 6, "example.py"),
        ],
        id="two_tagged_scripts_one_untagged_script",
    ),
]


@pytest.mark.parametrize("readme_content, expected", test_cases)
def test_script_path_extractor(readme_content, expected):
    script_metadata_extractor = ScriptMetadataExtractor()
    result = script_metadata_extractor.extract(readme_content=readme_content)
    assert result == expected


def test_code_embedder_read_script_content():
    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()

    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )

    scripts = code_embedder._read_script_content(
        scripts=[
            ScriptMetadata(
                readme_start=6, readme_end=7, path="tests/data/example.py", content=""
            )
        ]
    )
    assert scripts == [
        ScriptMetadata(
            readme_start=6,
            readme_end=7,
            path="tests/data/example.py",
            content='print("Hello, World! from script")\n',
        )
    ]


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

    # Create temporary copies of the original README files
    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_path in zip(original_paths, temp_readme_paths):
        with open(original_path, 'r') as original_file:
            temp_path.write_text(original_file.read())

    script_metadata_extractor = ScriptMetadataExtractor()
    script_content_reader = ScriptContentReader()

    code_embedder = CodeEmbedder(
        readme_paths=[str(p) for p in temp_readme_paths],
        script_metadata_extractor=script_metadata_extractor,
        script_content_reader=script_content_reader,
    )

    code_embedder()

    # Compare the content of the expected and updated README files
    for expected_path, temp_path in zip(expected_paths, temp_readme_paths):
        with open(expected_path, 'r') as expected_file:
            expected_content = expected_file.readlines()

        with open(temp_path, 'r') as updated_file:
            updated_content = updated_file.readlines()

        assert expected_content == updated_content


### Addressing Feedback:

1. **SyntaxError**: Removed any extraneous text or comments that were causing the `SyntaxError`.
2. **Function Signature**: Added a return type annotation (`-> None`) to the `test_code_embedder` function.
3. **Variable Naming Consistency**: Changed `temp_paths` to `temp_readme_paths` for clarity.
4. **File Handling**: Ensured consistent use of the context manager (`with` statement) for file operations.
5. **List Comprehension**: Used list comprehension for creating `temp_readme_paths` in a concise manner.
6. **Readability**: Maintained consistent spacing and formatting throughout the code.
7. **Commenting**: Added comments to explain the purpose of creating temporary copies of files.