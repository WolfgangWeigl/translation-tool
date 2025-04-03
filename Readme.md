<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]


<br />
<div align="center">
<!-- PROJECT LOGO -->
  <a href="https://www.oth-aw.de/forschung/forschungsprofil/forschungs-und-entwicklungsprojekte/ideal/">
    <img src="app/static/images/ideal-logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Translation Tool</h3>

  <p align="center">
    A web-based tool for translating XML and MBZ files, optimized for Moodle content.
    <br />
    <a href="https://github.com/WolfgangWeigl/translation-tool"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/WolfgangWeigl/translation-tool">View Demo</a>
    ·
    <a href="https://github.com/WolfgangWeigl/translation-tool/issues/new?labels=bug">Report Bug</a>
    ·
    <a href="https://github.com/WolfgangWeigl/translation-tool/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

A simple and powerful Flask-based app for translating XML and MBZ files via LibreTranslate API. Built with production readiness in mind using Docker.

### Built With

[![Docker][Docker]][Docker-url]
[![LibreTranslate][LibreTranslate]][LibreTranslate-url]
[![FLASK][FLASK]][Flask-url]
[![Flask-SocketIO][Flask-SocketIO]][Flask-SocketIO-url]
[![eventlet][eventlet]][eventlet-url]
[![Bootstrap][Bootstrap]][Bootstrap-url]

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- WSL2 (on Windows, required for Docker Desktop)

### Installation

#### 1. Clone the repository

```bash
git clone https://github.com/WolfgangWeigl/translation-tool
cd translation-tool
```
#### 2. Start the container

##### Production Mode

Builds an optimized setup for deployment:

```bash
docker compose up --build -d
```
##### Development Mode (with Hot Reload)

Ideal for local development – your code is mounted into the container, enabling **hot reload** behavior.  
No rebuild is required after code changes unless dependencies change.

```bash
docker compose -f docker-compose.dev.yml up --build -d
```
Changes to the code are applied immediately without restarting the container.

##### Testing Mode

Runs the test environment and stops on the first failing container:

```bash
docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
```

####  Notes

- `--build` ensures a fresh image build (useful when dependencies are updated).
- `-d` runs the containers in detached (background) mode.


### Environment Configuration

You can limit which language models LibreTranslate loads by setting the `LT_LOAD_ONLY` variable in `env/prod.env` or `env/dev.env`:

```env
LT_LOAD_ONLY=de,en
```

> ⚠️ If you do **not** set `LT_LOAD_ONLY`, **all models will be loaded**.  
> This slows down the **very first container startup after a fresh build**, as all models are downloaded and initialized.  
> **After the first startup, the models are cached and subsequent starts are much faster.**

## Usage

Once the containers are running:

- Visit [http://localhost](http://localhost) in your browser
- Or open Docker Desktop and click on the mapped port (usually `80:5000`)

## Roadmap

- [X] Upload progress bar
- [X] Translation progress bar
- [ ] Drag & Drop upload UI
- [ ] MBZ support
- [ ] Editor view without XML tags (only relevant STACK fields)
- [ ] URL highlighting in editor view

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Wolfgang Weigl – [LinkedIn](https://linkedin.com/in/wolfgang-weigl-933885236/)  
Project Website: [Projekt IdeaL | OTH Amberg-Weiden](https://www.oth-aw.de/forschung/forschungsprofil/forschungs-und-entwicklungsprojekte/ideal/)  
Repository: [https://github.com/WolfgangWeigl/translation-tool](https://github.com/WolfgangWeigl/translation-tool)


<!-- MARKDOWN LINKS & **IMAGES** -->
[contributors-shield]: https://img.shields.io/github/contributors/WolfgangWeigl/translation-tool.svg?style=for-the-badge
[contributors-url]: https://git.oth-aw.de/WolfgangWeigl/translation-tool/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/WolfgangWeigl/translation-tool.svg?style=for-the-badge
[forks-url]: https://git.oth-aw.de/WolfgangWeigl/translation-tool/network/members
[stars-shield]: https://img.shields.io/github/stars/WolfgangWeigl/translation-tool.svg?style=for-the-badge
[stars-url]: https://git.oth-aw.de/WolfgangWeigl/translation-tool/stargazers
[issues-shield]: https://img.shields.io/github/issues/WolfgangWeigl/translation-tool.svg?style=for-the-badge
[issues-url]: https://git.oth-aw.de/WolfgangWeigl/translation-tool/issues
[license-shield]: https://img.shields.io/badge/license-MIT-blue?style=for-the-badge
[license-url]: https://git.oth-aw.de/WolfgangWeigl/translation-tool/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&colorB=0a66c2
[linkedin-url]: https://linkedin.com/in/wolfgang-weigl-933885236/
[Docker]: https://img.shields.io/badge/docker-555?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[LibreTranslate]: https://img.shields.io/badge/libretranslate-555?style=for-the-badge
[LibreTranslate-url]: https://github.com/LibreTranslate/LibreTranslate
[FLASK]: https://img.shields.io/badge/Flask-555?style=for-the-badge&logo=Flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[Flask-SocketIO]: https://img.shields.io/badge/Socket.io-555?style=for-the-badge&logo=Socket.io&logoColor=white
[Flask-SocketIO-url]: https://flask-socketio.readthedocs.io/
[eventlet]: https://img.shields.io/badge/eventlet-555?style=for-the-badge
[eventlet-url]: https://pypi.org/project/eventlet/
[Bootstrap]: https://img.shields.io/badge/Bootstrap-555?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com/