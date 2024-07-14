
# Markdown Viewer

A simple local Markdown viewer built with Python, Tkinter, and BeautifulSoup. This tool allows you to open and render Markdown files, displaying them with proper formatting and images.

## Features

- Open and view local Markdown files.
- Render Markdown content with images and lists correctly displayed.
- Styled code blocks with a gray background and rounded corners.
- Light gray border around the content for a cleaner look.

## Requirements

Ensure you have Python installed. Create and activate a virtual environment, then install the required dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Installation

1. Clone the repository or download the `markdown_viewer.py` file.
2. Ensure you have a virtual environment set up and activated.
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the `markdown_viewer.py` script:

```bash
python markdown_viewer.py
```

2. A window will open with a button to select a Markdown file. Click the button and choose the file you want to view.
3. The Markdown content will be displayed in your default web browser with proper formatting.

## Example

Here is an example of how the viewer renders Markdown content:

```markdown
# Sample Markdown

This is a sample Markdown file.

## Features

- Open and view local Markdown files.
- Render images correctly.

![Sample Image](path/to/image.png)

## Code Block

```python
def example_function():
    print("Hello, World!")
```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

## Requirements File

Make sure your `requirements.txt` includes the following:

```text
beautifulsoup4==4.10.0
markdown==3.3.6
```

## Project Structure

Here is an example of the project structure:

```
markdown_viewer/
├── markdown_viewer.py
├── requirements.txt
└── README.md
```
