import os
import xml.etree.ElementTree as ET


def sanitize_filename(name):
    """Replace invalid filename characters with underscores."""
    return (
        name.replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .replace("*", "_")
        .replace("?", "_")
        .replace('"', "_")
        .replace("<", "_")
        .replace(">", "_")
        .replace("|", "_")
    )


def extract_text_from_html(element, in_code_block=False):
    """Recursively extract and format text from HTML for Markdown."""
    markdown = ""

    tag = element.tag.split("}")[-1]

    if tag == "p":
        if not in_code_block:
            markdown += "\n"
        for child in element:
            markdown += extract_text_from_html(child, in_code_block)
        if element.text:
            markdown += element.text
        markdown += "\n"

    elif tag == "br":
        markdown += "\n"

    elif tag in ("pre", "code"):
        content = "".join(extract_text_from_html(child, True) for child in element)
        if element.text:
            content = element.text + content
        if not in_code_block:
            markdown += f"\n```\n{content.strip()}\n```\n"
        else:
            markdown += content

    else:
        if element.text:
            markdown += element.text
        for child in element:
            markdown += extract_text_from_html(child, in_code_block)
        if element.tail:
            markdown += element.tail

    return markdown


def parse_xml_to_files(xml_file, output_dir):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Function to recursively process topics
    def process_topic(topic, parent_path):
        text_element = topic.find("ap:Text", namespaces)
        if text_element is not None:
            topic_text = text_element.get("PlainText")
            sanitized_topic_text = sanitize_filename(topic_text)
        else:
            sanitized_topic_text = "Untitled_Topic"

        subtopics = topic.find("ap:SubTopics", namespaces)
        has_subtopics = (
            subtopics is not None and len(subtopics.findall("ap:Topic", namespaces)) > 0
        )

        if has_subtopics:
            topic_dir = os.path.join(parent_path, sanitized_topic_text)
            os.makedirs(topic_dir, exist_ok=True)
            topic_path = os.path.join(topic_dir, f"{sanitized_topic_text}.md")
        else:
            topic_dir = parent_path
            topic_path = os.path.join(parent_path, f"{sanitized_topic_text}.md")

        with open(topic_path, "w", encoding="utf-8") as topic_file:
            notes_group = topic.find("ap:NotesGroup", namespaces)
            if notes_group is not None:
                notes_data = notes_group.find("ap:NotesXhtmlData", namespaces)
                if notes_data is not None:
                    html_content = notes_data.find(
                        ".//{http://www.w3.org/1999/xhtml}html"
                    )
                    if html_content is not None:
                        topic_file.write(
                            extract_text_from_html(html_content).strip() + "\n"
                        )

        if has_subtopics:
            for subtopic in subtopics.findall("ap:Topic", namespaces):
                process_topic(subtopic, topic_dir)

    # Namespaces
    namespaces = {
        "ap": "http://schemas.mindjet.com/MindManager/Application/2003",
        "cor": "http://schemas.mindjet.com/MindManager/Core/2003",
        "pri": "http://schemas.mindjet.com/MindManager/Primitive/2003",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    }

    # Start processing from the root topic
    main_topic = root.find(".//ap:OneTopic", namespaces)
    if main_topic is not None:
        topic = main_topic.find("ap:Topic", namespaces)
        if topic is not None:
            process_topic(topic, output_dir)


# Example usage
xml_file_path = "MapFile.xmmap"
output_directory_path = "output_directory"
parse_xml_to_files(xml_file_path, output_directory_path)
