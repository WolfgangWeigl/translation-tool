<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">🧩 Translation Tool</h3>

  <p align="center">
    A web-based tool for translating XML and MBZ files – perfect for Moodle course content and similar use cases.
    <br />
    <a href="#">View Demo</a>
    ·
    <a href="https://github.com/your-username/translation-tool/issues">Report Bug</a>
    ·
    <a href="https://github.com/your-username/translation-tool/issues">Request Feature</a>
  </p>
</div>

---

## 📄 About The Project

This tool provides a browser-based interface to upload, translate, compare, and download XML and MBZ files. It integrates with LibreTranslate and supports both single and batch translation modes.

Key features:
- Upload and extract XML/MBZ files
- View original and translated content side by side
- Translate using the LibreTranslate API
- Download translated content
- Fully web-based interface

---

## 🏗️ Built With

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [eventlet](https://pypi.org/project/eventlet/)
- [LibreTranslatePy](https://pypi.org/project/libretranslatepy/)
- [Docker](https://www.docker.com/)

---

## 🚀 Getting Started

### 🧰 Prerequisites & Installation

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- On Windows: [WSL2](https://docs.microsoft.com/en-us/windows/wsl/) must be installed and configured (required for Docker Desktop)

Clone this repository and run:

```bash
docker compose up --build -d
```

For development, use:

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

**Flags explained:**
- `--build`: Rebuilds the image (recommended if you made code changes)
- `-d`: Runs the container in detached mode (in the background)

> These flags are optional but recommended to ensure you get the latest version and don’t block your terminal.

---

### 🌐 Environment Configuration

You can configure which language models to load by setting the `LT_LOAD_ONLY` variable in the `env/prod.env` or `env/dev.env` file:

```env
# env/prod.env
LT_LOAD_ONLY=de,en
```

> ⚠️ If you do not set `LT_LOAD_ONLY`, **all available models will be loaded**, which can **significantly slow down the container startup time**.

---

## 📦 Usage

Once the containers are running:

- Open your browser and go to [http://localhost](http://localhost)
- Or open Docker Desktop and click the forwarded port (usually `80:5000`) as shown in the container list

You should see the app interface and can begin uploading and translating files.

---

## ✅ Roadmap

- [ ] Drag & Drop upload UI
- [ ] Upload progress bar
- [ ] Persistent translation history (e.g. DB or file store)
- [ ] User authentication
- [ ] Translation memory or glossary feature

---

## 🙌 Contributing

Contributions are welcome! Fork the repo and create a pull request, or open an issue to suggest changes.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙋‍♂️ Contact

Your Name – [@your_handle](https://twitter.com/your_handle) – your.email@example.com

Project Link: [https://github.com/your-username/translation-tool](https://github.com/your-username/translation-tool)
