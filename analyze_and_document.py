from utils.crawl_local_files import crawl_local_files
import os
import json
import argparse

def create_microservice_documentation(files):
    """Analyze files and create documentation structure"""
    documentation = {
        "project_name": "E-Commerce Microservice",
        "microservices": {},
        "shared_libraries": {},
        "architecture": {
            "services": [],
            "dependencies": []
        }
    }
    
    # Organize files by microservice
    for filepath, content in files.items():
        parts = filepath.split('/')
        if len(parts) < 2:
            continue
            
        service_name = parts[0]
        if service_name == "shared-token-validation-lib":
            if service_name not in documentation["shared_libraries"]:
                documentation["shared_libraries"][service_name] = {
                    "description": "Shared library for JWT token validation",
                    "components": []
                }
            documentation["shared_libraries"][service_name]["components"].append(filepath)
        else:
            if service_name not in documentation["microservices"]:
                documentation["microservices"][service_name] = {
                    "main_class": "",
                    "controllers": [],
                    "services": [],
                    "repositories": [],
                    "models": [],
                    "config": []
                }
            
            # Categorize files
            if "controller" in filepath.lower() or "api" in filepath.lower():
                documentation["microservices"][service_name]["controllers"].append(filepath)
            elif "service" in filepath.lower():
                documentation["microservices"][service_name]["services"].append(filepath)
            elif "repository" in filepath.lower():
                documentation["microservices"][service_name]["repositories"].append(filepath)
            elif "model" in filepath.lower() or "entity" in filepath.lower():
                documentation["microservices"][service_name]["models"].append(filepath)
            elif "config" in filepath.lower():
                documentation["microservices"][service_name]["config"].append(filepath)
            elif "Application.java" in filepath:
                documentation["microservices"][service_name]["main_class"] = filepath

    # Add services to architecture
    documentation["architecture"]["services"] = list(documentation["microservices"].keys())
    
    return documentation

def generate_markdown(documentation):
    """Generate markdown documentation"""
    md = []
    
    # Project Header
    md.append("# E-Commerce Microservice Documentation\n")
    md.append("## Project Overview\n")
    md.append("This is a microservices-based e-commerce application with the following components:\n")
    
    # Architecture Overview
    md.append("## Architecture\n")
    md.append("### Services\n")
    for service in documentation["architecture"]["services"]:
        md.append(f"- {service}\n")
    
    # Detailed Service Documentation
    md.append("\n## Microservices\n")
    for service_name, service_info in documentation["microservices"].items():
        md.append(f"### {service_name}\n")
        
        if service_info["main_class"]:
            md.append(f"**Main Class:** `{service_info['main_class']}`\n")
        
        if service_info["controllers"]:
            md.append("\n#### Controllers\n")
            for controller in service_info["controllers"]:
                md.append(f"- `{controller}`\n")
        
        if service_info["services"]:
            md.append("\n#### Services\n")
            for service in service_info["services"]:
                md.append(f"- `{service}`\n")
        
        if service_info["repositories"]:
            md.append("\n#### Repositories\n")
            for repo in service_info["repositories"]:
                md.append(f"- `{repo}`\n")
        
        if service_info["models"]:
            md.append("\n#### Domain Models\n")
            for model in service_info["models"]:
                md.append(f"- `{model}`\n")
        
        md.append("\n")
    
    # Shared Libraries
    if documentation["shared_libraries"]:
        md.append("## Shared Libraries\n")
        for lib_name, lib_info in documentation["shared_libraries"].items():
            md.append(f"### {lib_name}\n")
            md.append(f"{lib_info['description']}\n\n")
            md.append("#### Components\n")
            for component in lib_info["components"]:
                md.append(f"- `{component}`\n")
    
    return "\n".join(md)

def analyze_directory(directory_path):
    """Analyze a directory and generate documentation"""
    # Crawl the files
    print("Crawling Java files...")
    result = crawl_local_files(
        directory=directory_path,
        include_patterns={"*.java"},
        use_relative_paths=True
    )
    
    # Get the files dictionary
    files = result["files"]
    print(f"\nFound {len(files)} Java files")
    
    # Analyze and create documentation
    print("\nAnalyzing files and generating documentation...")
    documentation = create_microservice_documentation(files)
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save raw documentation structure as JSON
    with open(os.path.join(output_dir, "documentation.json"), "w") as f:
        json.dump(documentation, f, indent=2)
    
    # Generate and save markdown documentation
    markdown_content = generate_markdown(documentation)
    with open(os.path.join(output_dir, "documentation.md"), "w") as f:
        f.write(markdown_content)
    
    print("\nDocumentation generated successfully!")
    print(f"- JSON structure: {os.path.join(output_dir, 'documentation.json')}")
    print(f"- Markdown documentation: {os.path.join(output_dir, 'documentation.md')}")
    
    return documentation

def main():
    parser = argparse.ArgumentParser(description="Generate documentation for a Java microservice project")
    parser.add_argument("--dir", required=True, help="Path to the Java project directory")
    args = parser.parse_args()
    
    analyze_directory(args.dir)

if __name__ == "__main__":
    main() 