from utils.crawl_local_files import crawl_local_files

# Directory path
directory = "/Users/netrapawar/Downloads/E-Commerce-Microservice-master"

# Crawl the files
result = crawl_local_files(
    directory=directory,
    include_patterns={"*.java"},  # Only include Java files
    use_relative_paths=True
)

# Get the files dictionary
files = result["files"]

# Print summary
print(f"\nFound {len(files)} Java files:")
print("-" * 50)

# Print each file path
for filepath in sorted(files.keys()):
    print(f"- {filepath}") 