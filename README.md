# MindManager XML to Markdown Converter

This Python script converts a MindManager `.xmmap` XML file into a structured directory of Markdown (`.md`) files, preserving the hierarchy and notes of topics.

## Features

- Extracts the main topic and subtopics from a MindManager map.
- Creates a directory tree reflecting the topic structure.
- Converts notes from each topic into Markdown files.
- Preserves formatting such as paragraphs, line breaks, and code blocks.

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Preparation

Before running the script, you must convert your `.mmap` file to the `.xmmap` format:

> **In MindManager:**  
> Go to **File → Save As**  
> Choose **MindManager Map (XML)** as the format (`.xmmap`)

## Usage

1. Save your MindManager map as an `.xmmap` XML file.
2. Place the script in the same directory or update the file paths accordingly.
3. Run the script with:

```python
xml_file_path = 'MapFile.xmmap'  # Path to your MindManager XML file
output_directory_path = 'output_directory'  # Target directory for Markdown files
parse_xml_to_files(xml_file_path, output_directory_path)

## Output
The script will generate:
- A top-level folder named after the main topic.
- Nested folders for each subtopic that contains children.
- A .md Markdown file for each topic containing the notes.

## Limitations
- Non-textual content such as images, icons, and tags are not supported.
- Assumes a single root topic (<ap:OneTopic>) in the map file.
- Does not convert relationships, callouts, or visual formatting.
