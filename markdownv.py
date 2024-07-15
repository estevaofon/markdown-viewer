import argparse
import markdown
import webbrowser
import os
from bs4 import BeautifulSoup
import time


def convert_to_html_with_padding(markdown_text, base_path):
    html_content = markdown.markdown(markdown_text, extensions=["extra"])
    styled_html = f"""
    <html>
    <head>
    <style>
        body {{
            padding-left: 30%;
            padding-right: 30%;
            padding-top: 20px;
            font-family: Arial, sans-serif;
        }}
         .content {{
            background-color: white;
            border: 1px solid #e1e4e8;
            border-radius: 6px;
            padding: 20px;
            max-width: 800px;
            width: 100%;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }}
          pre {{
            background-color: #f6f8fa;
            padding: 10px;
            border-radius: 5px;
            overflow: auto;
        }}
        code {{
            background-color: #f6f8fa;
            padding-left: 2px 4px;
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
            img["src"] = "file://" + os.path.realpath(os.path.join(base_path, src.strip("/")))
    return str(soup)


def show_html(html_content):
    temp_file = os.path.join(os.getcwd(), "temp.html")
    with open(temp_file, "w", encoding="utf-8") as file:
        file.write(html_content)
    webbrowser.open("file://" + os.path.realpath(temp_file))

    # Wait a few seconds to ensure the browser has time to open the file
    time.sleep(1)

    # Delete the temporary file
    os.remove(temp_file)


def main():
    parser = argparse.ArgumentParser(description="View Markdown files as HTML")
    parser.add_argument("filepath", help="Path to the Markdown file")
    args = parser.parse_args()

    file_path = args.filepath
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_text = file.read()
            html = convert_to_html_with_padding(markdown_text, os.path.dirname(file_path))
            show_html(html)
    else:
        print(f"The file {file_path} does not exist")


if __name__ == "__main__":
    main()
