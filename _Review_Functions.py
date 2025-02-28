import os
import re
from pathlib import Path

class CodeAggregator:
    def __init__(self, root_dir='.', output_filename='viralkiller_project_directory.txt', compact=False):
        self.root_dir = Path(root_dir)
        self.output_filename = output_filename
        self.compact = compact

    def append_file_content(self, content_list, file_path):
        header = f"#### #### #### #### This file: {file_path} #### #### #### #### Contents:\n\n"
        try:
            file_content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            file_content = f"Error reading file: {e}\n"
        if self.compact:
            file_content = self.compact_content(file_content, file_path.suffix)
        content_list.append(header + file_content + "\n" + "=" * 80 + "\n")

    def compact_content(self, content: str, extension: str) -> str:
        if extension == '.py':
            # Remove full-line comments and inline comments (naively)
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                stripped = line.strip()
                if not stripped or stripped.startswith('#'):
                    continue
                line = line.split('#', 1)[0]
                if line.strip():
                    new_lines.append(line.rstrip())
            return "\n".join(new_lines)
        elif extension == '.html':
            # Remove HTML comments <!-- ... -->
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
            lines = content.splitlines()
            new_lines = [line.rstrip() for line in lines if line.strip()]
            return "\n".join(new_lines)
        elif extension == '.js':
            # Remove JS block comments /* ... */ and inline comments //
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                line = line.split('//', 1)[0]
                if line.strip():
                    new_lines.append(line.rstrip())
            return "\n".join(new_lines)
        elif extension == '.css':
            # Remove CSS block comments
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            lines = content.splitlines()
            new_lines = [line.rstrip() for line in lines if line.strip()]
            return "\n".join(new_lines)
        else:
            lines = content.splitlines()
            new_lines = [line.rstrip() for line in lines if line.strip()]
            return "\n".join(new_lines)

    def aggregate_files(self, directory, extensions, recursive=False):
        contents = []
        if recursive:
            files = directory.rglob('*')
        else:
            files = directory.glob('*')
        
        # Add current file path to exclude it from aggregation
        current_file = Path(__file__).resolve()
        
        for file in files:
            # Skip the aggregator file itself
            if file.resolve() == current_file:
                continue
            if file.suffix in extensions and file.is_file():
                self.append_file_content(contents, file)
        return contents

    def aggregate(self):
        contents = []
        # Process .py files in the root directory
        contents.extend(self.aggregate_files(self.root_dir, ['.py']))

        # Process HTML files in the templates folder (recursive)
        templates_path = self.root_dir / 'templates'
        if templates_path.is_dir():
            contents.extend(self.aggregate_files(templates_path, ['.html'], recursive=True))

        # Process CSS files in the static/css folder
        css_path = self.root_dir / 'static' / 'css'
        if css_path.is_dir():
            contents.extend(self.aggregate_files(css_path, ['.css']))

        # Process JS files in the static/js folder
        js_path = self.root_dir / 'static' / 'js'
        if js_path.is_dir():
            contents.extend(self.aggregate_files(js_path, ['.js']))

        # Write all aggregated content into one text file
        with open(self.output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(contents))

if __name__ == "__main__":
    # Set compact=True to remove blank lines and comments
    aggregator = CodeAggregator(compact=True)
    aggregator.aggregate()
    print(f"Aggregated code has been written to {aggregator.output_filename}")
