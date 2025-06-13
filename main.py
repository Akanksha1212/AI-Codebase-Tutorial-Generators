from run_tutorial import generate_tutorial

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a tutorial for a GitHub codebase or local directory."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--repo", help="URL of the public GitHub repository.")
    source_group.add_argument("--dir",  help="Path to local directory.")

    parser.add_argument("-n", "--name",
                        help="Project name (optional, derived if omitted).")
    parser.add_argument("-t", "--token",
                        help="GitHub token (or uses GITHUB_TOKEN env var).")
    parser.add_argument("-o", "--output", default="output",
                        help="Directory for output (default ./output).")
    parser.add_argument("-i", "--include", nargs="+",
                        help="Include file patterns.")
    parser.add_argument("-e", "--exclude", nargs="+",
                        help="Exclude file patterns.")
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
