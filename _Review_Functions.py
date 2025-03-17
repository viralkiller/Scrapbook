import os
import re
from pathlib import Path
from datetime import datetime

class CodeAggregator:
    def __init__(self, root_dir='.', output_filename='project_directory_full_code.txt',
                 compact=False, excluded_extensions=None, include_files=None, exclude_files=None,
                 description_text=""):
        self.root_dir = Path(root_dir)
        self.output_filename = output_filename
        self.compact = compact
        # Set excluded extensions; if none provided, use an empty list
        self.excluded_extensions = excluded_extensions if excluded_extensions is not None else []
        # Set include/exclude file lists; if none provided, use empty lists
        self.include_files = include_files if include_files is not None else []
        self.exclude_files = exclude_files if exclude_files is not None else []
        self.description_text = description_text

    def append_file_content(self, content_list, file_path):
        header = f"\no_o This file: {file_path} | Contents:\n\n"
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
        elif extension == '.json':
            # For JSON, we just remove empty lines
            lines = content.splitlines()
            new_lines = [line.rstrip() for line in lines if line.strip()]
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
        files = directory.rglob('*') if recursive else directory.glob('*')
        # Add current file path to exclude it from aggregation
        current_file = Path(__file__).resolve()

        for file in files:
            # Skip the aggregator file itself
            if file.resolve() == current_file:
                continue
            # Ensure it's a file
            if not file.is_file():
                continue

            # Skip if the file is explicitly excluded by its filename
            if file.name in self.exclude_files:
                continue

            # If the file is explicitly included by its filename, include regardless of extension.
            if file.name in self.include_files:
                self.append_file_content(contents, file)
            # Otherwise, include only if its extension is allowed and not excluded.
            elif file.suffix in extensions and file.suffix not in self.excluded_extensions:
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

        # Process JSON files in the static/json folder
        json_path = self.root_dir / 'static' / 'json'
        if json_path.is_dir():
            contents.extend(self.aggregate_files(json_path, ['.json']))

        # Add a description header with timestamp at the top if provided.
        if self.description_text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"Description:\n{self.description_text}\n\nAggregated on: {timestamp}\n{'=' * 80}\n\n"
            contents.insert(0, header)

        # Write all aggregated content into one text file
        with open(self.output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(contents))

if __name__ == "__main__":
    # Example settings: exclude .css and .json files by extension,
    # include specific files by exact filename, and exclude certain filenames.
    multiline_description = (
        "This is the Nodes-GPT project.\n"
        "Like Nuke with video editing, it allows node based AI operations to be carried out for fun possibilities.\n"
        "For the duration of this chat o_o will symbolize separation, i.e. between different files, or text and user queries.\n"
        "^_^ will be the symbol that tells you where your main task to solve is, if it exists."
    )
    aggregator = CodeAggregator(compact=True,
                                excluded_extensions=['.json', '.css'],
                                include_files=['how_it_works.txt'],
                                exclude_files=['credits.js','copy_clear_etc.js','image_strip.js','simulate_move.js','resize_input.js',\
                                'resize_output.js','cv.js','upload_files.js','_Image_Functions.py'],
                                description_text=multiline_description)
    aggregator.aggregate()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Aggregated code has been written to {aggregator.output_filename}")
