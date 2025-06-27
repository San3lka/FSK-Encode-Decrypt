---

## 📑 Table of Contents

- [🚀 Overview](#-overview)
- [✨ Features](#-features)
- [🗂 Project Structure](#-project-structure)
  - [File Index](#file-index)
- [🚀 Getting Started](#-getting-started)
  - [✅ Prerequisites](#-prerequisites)
  - [⚙️ Installation](#-installation)
  - [🖥 Usage](#-usage)
  - [🧪 Testing](#-testing)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)

---

## 🚀 Overview

**Secure Audio Codec** turns your text into a WAV file by assigning every character its own tone (frequency). The exact mapping is shuffled with a secret key or a SHA‑256 hash, so only someone who knows the key can re‑assemble the tones back into readable text. The whole workflow – encoding, decoding, and a dark‑theme GUI – sits in a single `secure_audio_codec.py` file.

---

## ✨ Features

- **Key‑Based Encryption** – Any string works as a key; a built‑in dialog can hash it to SHA‑256 for extra entropy.
- **Text ↔ Audio** – Encode messages to `.wav`; decode them back to plain text.
- **Unicode Friendly** – Supports ASCII, digits, punctuation, and Czech diacritics out of the box.
- **Minimal Dependencies** – Only `numpy`, `soundfile`, and the Python standard library.
- **Clean Dark GUI** – Built with `tkinter`, so it runs everywhere Python does.

---

## 🗂 Project Structure

```txt
secure-audio-codec/
├── README.md          # ← you are here
└── secure_audio_codec.py
```

### File Index

| File                    | Purpose                                                 |
| ----------------------- | ------------------------------------------------------- |
| `secure_audio_codec.py` | Core logic **and** GUI (encode, decode, SHA‑256 helper) |

---

## 🚀 Getting Started

### ✅ Prerequisites

- **Python 3.8 or newer**

### ⚙️ Installation

Install the two run‑time dependencies in one go:

```bash
pip install numpy soundfile
```

> **Tip ▶︎** If you like reproducible installs, drop this into a `requirements.txt` and run `pip install -r requirements.txt`:
>
> ```
> numpy
> soundfile
> ```

---

### 🖥 Usage

Start the app:

```bash
python secure_audio_codec.py
```

#### GUI Walkthrough

1. **Choose Mode** – `Encrypt` **or** `Decrypt`.
2. **Enter / Generate Key** – Type anything or click *Generate SHA‑256*.
3. **Encrypt Mode**
   - Type a message in the bottom pane.
   - Press **Run**, pick a filename, and a WAV pops out.
4. **Decrypt Mode**
   - After choosing the mode, a file dialog opens – pick the WAV you want to read.
   - Press **Run** to reveal the hidden text.

---

### 🧪 Testing

No automated tests (yet), but you can sanity‑check manually:

1. Launch the program.
2. Encrypt the string `Hello world!` using key `test123`.
3. Decrypt the saved WAV with the same key.
4. Verify the output equals `Hello world!`.

---

## 🛣 Roadmap

-

---

## 🤝 Contributing

1. **Fork** → **Clone** → **Create Branch**
2. Commit clear, scoped changes.
3. Open a **Pull Request** – all ideas & fixes welcome!

---

## 📄 License

Released under the MIT License – see `LICENSE` for details.

---

## 🙏 Acknowledgments

- [`numpy`](https://numpy.org/)
- [`soundfile`](https://pysoundfile.readthedocs.io/)
- [`tkinter`](https://docs.python.org/3/library/tkinter.html)

> Inspired by classic “acoustic modem” experiments and the need for a dead‑simple, GUI‑friendly proof of concept.

