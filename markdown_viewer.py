import tkinter as tk
from tkinter import filedialog
import markdown
import webbrowser
import os
from bs4 import BeautifulSoup


class MarkdownViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Markdown Viewer")
        self.geometry("300x200")

        # Create a button to open file
        self.open_button = tk.Button(
            self, text="Open Markdown File", command=self.open_file
        )
        self.open_button.pack(expand=True)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                markdown_text = file.read()
                html = self.convert_to_html_with_padding(
                    markdown_text, os.path.dirname(file_path)
                )
                self.show_html(html)

    def convert_to_html_with_padding(self, markdown_text, base_path):
        # Convert Markdown to HTML with extra extensions to handle lists and other elements
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
        return self.update_image_paths(styled_html, base_path)

    def update_image_paths(self, html_content, base_path):
        soup = BeautifulSoup(html_content, "html.parser")
        for img in soup.find_all("img"):
            src = img["src"]
            if not src.startswith(("http://", "https://")):
                # Create an absolute path to the image
                img["src"] = "file://" + os.path.realpath(
                    os.path.join(base_path, src.strip("/"))
                )
        return str(soup)

    def show_html(self, html_content):
        # Save the HTML content to a temporary file
        temp_file = os.path.join(os.getcwd(), "temp.html")
        with open(temp_file, "w", encoding="utf-8") as file:
            file.write(html_content)

        # Open the HTML file in the default web browser
        webbrowser.open("file://" + os.path.realpath(temp_file))


if __name__ == "__main__":
    app = MarkdownViewer()
    app.mainloop()
