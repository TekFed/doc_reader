<div align="center">

  <h1>📖 Document Reader - Text to Speech</h1>

  <p>
    <strong>A beautiful offline desktop app that turns your documents into spoken audio</strong><br>
    Currently focused on saving MP3 files — live reading mode coming soon! 🚀
  </p>

  <p>
    <a href="https://github.com/TekFed/doc_reader/stargazers">
      <img src="https://img.shields.io/github/stars/TekFed/doc_reader?style=social" alt="GitHub stars">
    </a>
    <a href="https://github.com/TekFed/doc_reader/issues">
      <img src="https://img.shields.io/github/issues/TekFed/doc_reader" alt="Open issues">
    </a>
    <a href="LICENSE">
      <img src="https://img.shields.io/github/license/TekFed/doc_reader?color=blue" alt="MIT License">
    </a>
    <a href="https://www.python.org">
      <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python&logoColor=white" alt="Python 3.8+">
    </a>
  </p>

  <img src="docs/main-window.png" alt="App Screenshot" width="800" />

</div>

## ✨ Features

- 📄 Load & preview documents instantly
- 🎙️ Convert documents to natural-sounding MP3 files
- ⚙️ Choose voice and speaking speed
- 📁 Auto-generated filenames (e.g. `report_spoken_20260225_1048.mp3`)
- 🖥️ Clean, modern, scrollable Tkinter interface
- 🔌 Completely offline — no internet needed

> **Live speak mode (read aloud with pause/resume) → Coming soon!** ⏳

## 🚀 Quick Start

### Clone & install

```bash
git clone https://github.com/tekfed-Llins/document-reader.git
cd document-reader

# Recommended: virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Run the app

```bash
python main.py
```

1. Click **Browse** → choose your document (.txt, .pdf, .docx, .epub, .html)
2. Click **Load & Preview**
3. Select voice & speed
4. Choose **Save to MP3** mode
5. Hit **Start** — MP3 saved automatically!

## 📊 Supported Formats

| Icon | Format       | Extensions            | Status |
|------|--------------|-----------------------|--------|
| 📝   | Plain Text   | `.txt`                | ✅     |
| 📄   | PDF          | `.pdf`                | ✅     |
| 📘   | Word         | `.docx`               | ✅     |
| 📚   | EPUB eBook   | `.epub`               | ✅     |
| 🌐   | HTML/Webpage | `.html`, `.htm`       | ✅     |

## 🛠️ Tech Stack

- **Python** 3.8+
- **Tkinter** (GUI)
- **pyttsx3** (offline TTS)
- **PyPDF2** • **python-docx** • **ebooklib** • **BeautifulSoup4** (document parsing)

## 🗺️ Roadmap

- ✅ Save to MP3 with auto filename
- ⏳ Live speak mode (real-time reading + pause/resume)
- 🔊 Volume control
- 🌙 Dark mode toggle
- ⌨️ Keyboard shortcuts
- 📊 Progress bar for long documents

## Contributing

Pull requests are welcome!  
Especially excited for help with:

- Implementing live speak mode
- Improving voice stability on Windows
- Adding new document formats

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/live-speak`)
3. Commit your changes (`git commit -m 'Add live speak mode'`)
4. Push to the branch (`git push origin feature/live-speak`)
5. Open a Pull Request

## 📄 License

Released under the **MIT License**  
See [LICENSE](LICENSE) for full details.

---

<div align="center">

  Made with ❤️ and lots of ☕ 
  © 2026 Collins (@tekfed_Llins)

</div>
