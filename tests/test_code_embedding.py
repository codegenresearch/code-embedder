import pytest
from src.code_embedding import CodeEmbedder, ScriptMetadata, ScriptPathExtractor

# Test cases for script path extraction
script_extraction_test_cases = [
    (
        [":main.py", "print('Hello, World!')", ""],
        [ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content="")],
        "one_tagged_script"
    ),
    (["", "print('Hello, World!')", ""], [], "one_untagged_script"),
    ([], [], "empty_readme"),
    (["", "print('Hello, World!')", ""], [], "one_untagged_script_language_specified"),
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
        [ScriptMetadata(readme_start=0, readme_end=3, path="example.py", content="")],
        "one_tagged_script_one_untagged_script"
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
            ScriptMetadata(readme_start=0, readme_end=2, path="main.py", content=""),
            ScriptMetadata(readme_start=3, readme_end=6, path="example.py", content=""),
        ],
        "two_tagged_scripts_one_untagged_script"
    ),
]

@pytest.mark.parametrize(
    "readme_content, expected, test_id",
    script_extraction_test_cases,
    ids=[test_id for _, _, test_id in script_extraction_test_cases]
)
def test_script_path_extractor(
    readme_content: list[str], expected: list[ScriptMetadata], test_id: str
) -> None:
    script_path_extractor = ScriptPathExtractor()
    result = script_path_extractor.extract(readme_content=readme_content)
    assert result == expected, f"Test failed for {test_id}"

# Test for reading script content
def test_code_embedder_read_script_content() -> None:
    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_path_extractor=ScriptPathExtractor(),
    )
    script_metadata = ScriptMetadata(
        readme_start=6, readme_end=7, path="tests/data/example.py", content=""
    )
    expected_metadata = ScriptMetadata(
        readme_start=6,
        readme_end=7,
        path="tests/data/example.py",
        content='print("Hello, World! from script")\n',
    )
    assert code_embedder._read_script_content(scripts=[script_metadata]) == [expected_metadata]

# Test for code embedding functionality
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

    # Create temporary copies of the original files
    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        temp_readme_path.write_text(open(original_path).read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(p) for p in temp_readme_paths],
        script_path_extractor=ScriptPathExtractor(),
    )
    code_embedder()

    # Verify the content of the updated files
    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        expected_content = open(expected_path).readlines()
        updated_content = open(temp_readme_path).readlines()
        assert updated_content == expected_content, f"Content mismatch for {temp_readme_path}"