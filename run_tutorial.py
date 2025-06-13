import dotenv
import os
from flow import create_tutorial_flow

dotenv.load_dotenv()

DEFAULT_INCLUDE_PATTERNS = {
    # Language files at any depth
    "**/*.py", "**/*.js", "**/*.jsx", "**/*.ts", "**/*.tsx",
    "**/*.go", "**/*.java", "**/*.pyi", "**/*.pyx",
    "**/*.c", "**/*.cc", "**/*.cpp", "**/*.h",
    "*.md", "*.rst", "Dockerfile", "Makefile", "**/*.yaml", "**/*.yml",
}

DEFAULT_EXCLUDE_PATTERNS = {
    "*test*", "tests/*", "docs/*", "examples/*", "v1/*",
    "dist/*", "build/*", "experimental/*", "deprecated/*",
    "legacy/*", ".git/*", ".github/*", ".next/*", ".vscode/*",
    "obj/*", "bin/*", "node_modules/*", "*.log"
}

def generate_tutorial(
    repo_url=None,
    local_dir=None,
    project_name=None,
    token=None,
    output="output",
    include=None,
    exclude=None,
    max_size=100000,
    language="english"
):
    """
    Runs the tutorial-generation ﬂow on the given repo or local dir.
    Returns the path to the folder containing the generated .md.
    """
    shared = {
        "repo_url": repo_url,
        "local_dir": local_dir,
        "project_name": project_name,
        "github_token": token or os.environ.get("GITHUB_TOKEN"),
        "output_dir": output,
        "include_patterns": set(include) if include else DEFAULT_INCLUDE_PATTERNS,
        "exclude_patterns": set(exclude) if exclude else DEFAULT_EXCLUDE_PATTERNS,
        "max_file_size": max_size,
        "language": language,
        # outputs populated by the flow
        "files": [], "abstractions": [], "relationships": {},
        "chapter_order": [], "chapters": [], "final_output_dir": None
    }

    print(f"🛠️ Generating tutorial for {repo_url or local_dir} in {language}")
    flow = create_tutorial_flow()
    flow.run(shared)
    return shared["final_output_dir"]


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a tutorial for a GitHub codebase or local directory."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--repo", help="URL of the public GitHub repository.")
    source_group.add_argument("--dir", help="Path to local directory.")

    parser.add_argument("-n", "--name",
                        help="Project name (optional, derived if omitted).")
    parser.add_argument("-t", "--token",
                        help="GitHub personal access token (or uses GITHUB_TOKEN env var).")
    parser.add_argument("-o", "--output", default="output",
                        help="Directory for output (default ./output).")
    parser.add_argument("-i", "--include", nargs="+",
                        help="Include file patterns (e.g. '*.py').")
    parser.add_argument("-e", "--exclude", nargs="+",
                        help="Exclude patterns (e.g. 'tests/*').")
    parser.add_argument("-s", "--max-size", type=int, default=100000,
                        help="Max file size in bytes (default 100000).")
    parser.add_argument("--language", default="english",
                        help="Language for the tutorial (default: english).")

    args = parser.parse_args()

    generate_tutorial(
        repo_url=args.repo,
        local_dir=args.dir,
        project_name=args.name,
        token=args.token,
        output=args.output,
        include=args.include,
        exclude=args.exclude,
        max_size=args.max_size,
        language=args.language,
    )
