import pytest

from src.code_embedding import CodeEmbedder, ScriptMetadata, ScriptPathExtractor


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
def test_script_path_extractor(
    readme_content: list[str], expected: list[ScriptMetadata]
) -> None:
    script_path_extractor = ScriptPathExtractor()
    result = script_path_extractor.extract(readme_content=readme_content)
    assert result == expected


def test_code_embedder_read_script_content() -> None:
    code_embedder = CodeEmbedder(
        readme_paths=["tests/data/readme.md"],
        script_path_extractor=ScriptPathExtractor(),
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

    temp_readme_paths = [tmp_path / f"readme{i}.md" for i in range(len(original_paths))]
    for original_path, temp_readme_path in zip(original_paths, temp_readme_paths):
        temp_readme_path.write_text(open(original_path).read())

    code_embedder = CodeEmbedder(
        readme_paths=[str(p) for p in temp_readme_paths],
        script_path_extractor=ScriptPathExtractor(),
    )

    code_embedder()

    for expected_path, temp_readme_path in zip(expected_paths, temp_readme_paths):
        expected_content = open(expected_path).readlines()
        updated_content = open(temp_readme_path).readlines()
        assert expected_content == updated_content