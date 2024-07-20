import argparse
import markdown
import os
import sys
import time
import webbrowser
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from pathlib import Path


def convert_to_html_with_padding(markdown_text, base_path, scale_percentage):
    html_content = markdown.markdown(markdown_text, extensions=["extra"])
    font_size = 16 * (scale_percentage / 100.0)
    styled_html = f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-size: {font_size}px;
            font-family: Arial, sans-serif;
            overflow-x: hidden;
            padding-top: 40px;
        }}
        .content {{
            background-color: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            padding: 20px;
            
            max-width: 800px;
            margin: 20px auto;
            width: calc(100% - 40px);
            box-sizing: border-box;
        }}
        pre {{
            background-color: #f6f8fa;
            padding: 10px;
            border-radius: 5px;
            overflow: auto;
        }}
        code {{
            background-color: #f6f8fa;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        img {{
            max-width: 80%;
            height: auto;
        }}
    </style>
    </head>
    <body>
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """
    return update_image_paths(styled_html, base_path)


def update_image_paths(html_content, base_path):
    soup = BeautifulSoup(html_content, "html.parser")
    for img in soup.find_all("img"):
        src = img["src"]
        if not src.startswith(("http://", "https://")):
            img_path = Path(base_path) / src.strip("/")
            if img_path.is_file():
                img["src"] = img_path.resolve().as_uri()
                print(
                    f"Updated image path: {img['src']}"
                )  # Debugging line to confirm image paths
            else:
                print(
                    f"Image file not found: {img_path}"
                )  # Debugging line for missing files
    return str(soup)


def show_html(html_content):
    temp_file = Path(os.getcwd()) / "temp.html"
    with open(temp_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(
        f"Temporary HTML file created at: {temp_file}"
    )  # Debugging line to confirm file creation
    webbrowser.open(temp_file.as_uri())

    # Wait a few seconds to ensure the browser has time to open the file
    time.sleep(1)

    # Delete the temporary file
    temp_file.unlink()


class MarkdownViewer(QMainWindow):
    def __init__(self, html_content, base_path):
        super().__init__()
        self.setWindowTitle("Markdown Viewer")
        self.setGeometry(100, 100, 900, 800)
        if Path("icon.png").is_file():
            self.setWindowIcon(QIcon("icon.png"))

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.web_view = QWebEngineView()

        # Create a temporary file to load the HTML content with correct paths

        temp_file = Path(base_path) / "temp.html"
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(
            f"Temporary HTML file created at: {temp_file}"
        )  # Debugging line to confirm file creation

        self.web_view.setUrl(QUrl.fromLocalFile(str(temp_file)))
        layout.addWidget(self.web_view)
        self.setCentralWidget(central_widget)

        # Delete the temporary file when the window is closed
        self.temp_file = temp_file

    def closeEvent(self, event):
        if self.temp_file.is_file():
            print(
                f"Deleting temporary file: {self.temp_file}"
            )  # Debugging line to confirm file deletion
            self.temp_file.unlink()
        event.accept()


def show_gui(html_content, base_path):
    app = QApplication(sys.argv)
    print(f"Base path: {base_path}")  # Debugging line to confirm base path
    viewer = MarkdownViewer(html_content, base_path)
    viewer.show()
    sys.exit(app.exec_())


def main():
    parser = argparse.ArgumentParser(description="View Markdown files as HTML")
    parser.add_argument("filepath", help="Path to the Markdown file")
    parser.add_argument(
        "-w",
        "--web",
        action="store_true",
        help="Display the page in a GUI window using PyQt",
    )
    parser.add_argument(
        "-s",
        "--scale",
        type=int,
        default=130,
        help="Scale percentage for the GUI display",
    )
    args = parser.parse_args()

    file_path = Path(args.filepath)
    if file_path.is_file():
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            html = convert_to_html_with_padding(
                markdown_text, file_path.parent, args.scale
            )
            base_path = os.getcwd()
            if args.web:
                show_gui(html, base_path)
            else:
                show_html(html)
    else:
        print(f"The file {file_path} does not exist")


if __name__ == "__main__":
    main()
