# Document Reader - Text to Speech

A simple, offline desktop application that converts documents into spoken audio using **pyttsx3**.

Currently supports saving documents as MP3 files (with automatic filenames).  
Live reading mode is **coming soon**.

https://github.com/tekfed-Llins/doc_reader

## ✨ Features

- Load & preview documents
- Supported formats: **.txt**, **.pdf**, **.docx**, **.epub**, **.html / .htm**
- Choose voice and speaking speed
- Save the entire document as an MP3 file (auto-generated filename)
- Clean, scrollable Tkinter GUI

**Live speak mode (read aloud with pause/resume) is planned for a future release.**

## 📸 Screenshots

![Main window](docs/main-window.png)  

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/tekfed-Llins/doc_reader.git
cd doc_reader
```

### 2. Install dependencies

```bash
# Recommended: use a virtual environment
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows

# Install required packages
pip install -r requirements.txt
```

### 3. Run the application

```bash
python main.py
```

## Supported Formats

| Format   | Extension(s)       | Status   |
|----------|--------------------|----------|
| Plain Text | `.txt`            | ✅       |
| PDF      | `.pdf`            | ✅       |
| Word     | `.docx`           | ✅       |
| EPUB     | `.epub`           | ✅       |
| HTML     | `.html`, `.htm`   | ✅       |

## Requirements

See [requirements.txt](requirements.txt) for the full list.

Minimum Python version: **3.8+**  
(Tested up to Python 3.12)

## Planned Features

- Live speak mode (real-time reading with pause/resume)
- Keyboard shortcuts for play/pause/stop
- Progress bar during MP3 generation for long documents
- Volume control
- Dark mode toggle

## Contributing

Contributions are welcome!  
If you want to help with live speak mode, bug fixes, or new formats:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please open an issue first if you're planning major changes.

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with:
- [pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- [PyPDF2](https://github.com/py-pdf/PyPDF2)
- [python-docx](https://github.com/python-openxml/python-docx)
- [ebooklib](https://github.com/aerkalov/ebooklib)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

Made with ❤️ and lots of ☕
