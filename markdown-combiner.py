"""将目录下的所有markdown文件内容，按照标题重新组合，相同标题下的内容拼接在一起，最终保存为一个markdown文件"""
from pathlib import Path
import re


def combine_markdown_files(directory, output_file):
    # Dictionary to store content by headers
    content_by_header = {}

    # Regex to match headers (# to ######)
    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)

    # Convert directory to Path object
    dir_path = Path(directory)

    # Iterate through all .md files in the directory
    for file_path in dir_path.glob('*.md'):
        content = file_path.read_text(encoding='utf-8')

        # Split content by headers
        sections = header_pattern.split(content)

        for i in range(1, len(sections), 3):
            level = sections[i]
            header = sections[i+1]
            text = sections[i+2]

            full_header = f"{level} {header}"

            if full_header not in content_by_header:
                content_by_header[full_header] = []

            content_by_header[full_header].append(text.strip())

    # Combine all content
    combined_content = []
    for header, contents in content_by_header.items():
        combined_content.append(header)
        combined_content.append("\n\n\n\n".join(contents))
        combined_content.append("\n\n\n\n")  # Add extra newline for separation

    # Write to output file
    output_path = Path(output_file)
    output_path.write_text("\n".join(combined_content), encoding='utf-8')


if __name__ == "__main__":
    directory = "./input"
    output_file = "./output/combined_output.md"
    combine_markdown_files(directory, output_file)
