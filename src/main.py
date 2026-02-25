# main.py
"""Application entry point."""

from gui import DocumentReaderGUI


if __name__ == "__main__":
    app = DocumentReaderGUI()
    app.root.mainloop()