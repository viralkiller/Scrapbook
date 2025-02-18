import os

class CodeAggregator:
    def __init__(self, root_dir='.', output_filename='full_code_review.txt'):
        self.root_dir = root_dir
        self.output_filename = output_filename

    def append_file_content(self, content_list, file_path):
        header = f"#### #### #### #### This file: {file_path} #### #### #### #### Contents:\n\n"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
        except Exception as e:
            file_content = f"Error reading file: {e}\n"
        content_list.append(header + file_content + "\n" + "=" * 80 + "\n")

    def aggregate(self):
        contents = []

        # Process .py files in the root directory
        for file in os.listdir(self.root_dir):
            if file.endswith('.py'):
                file_path = os.path.join(self.root_dir, file)
                if os.path.isfile(file_path):
                    self.append_file_content(contents, file_path)

        # Process HTML files in the templates folder
        templates_path = os.path.join(self.root_dir, 'templates')
        if os.path.isdir(templates_path):
            for root, _, files in os.walk(templates_path):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(root, file)
                        self.append_file_content(contents, file_path)

        # Process CSS files in the static/css folder
        css_path = os.path.join(self.root_dir, 'static', 'css')
        if os.path.isdir(css_path):
            for file in os.listdir(css_path):
                if file.endswith('.css'):
                    file_path = os.path.join(css_path, file)
                    if os.path.isfile(file_path):
                        self.append_file_content(contents, file_path)

        # Process JS files in the static/js folder
        js_path = os.path.join(self.root_dir, 'static', 'js')
        if os.path.isdir(js_path):
            for file in os.listdir(js_path):
                if file.endswith('.js'):
                    file_path = os.path.join(js_path, file)
                    if os.path.isfile(file_path):
                        self.append_file_content(contents, file_path)

        # Write all aggregated content into one text file
        with open(self.output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(contents))

if __name__ == "__main__":
    aggregator = CodeAggregator()
    aggregator.aggregate()
    print(f"Aggregated code has been written to {aggregator.output_filename}")
