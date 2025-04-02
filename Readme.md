<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!-- Contributors -->
<!-- [![Contributors][contributors-shield]][contributors-url] -->

<!-- Forks -->
<!-- [![Forks][forks-shield]][forks-url] -->

<!-- Stars -->
<!-- [![Stargazers][stars-shield]][stars-url] -->

<!-- Issues -->
<!-- [![Issues][issues-shield]][issues-url] -->

<!-- License -->
[![License][license-shield]][license-url]

<!-- LinkedIn -->
[![LinkedIn][linkedin-shield]][linkedin-url]


<br />
<div align="center">
<!-- PROJECT LOGO -->
  <!-- <a href="https://git.oth-aw.de/b566/translation-tool">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<h3 align="center">Translation Tool</h3>

  <p align="center">
    A web-based tool for translating XML and MBZ files, optimized for Moodle content.
    <br />
    <a href="https://git.oth-aw.de/b566/translation-tool"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://git.oth-aw.de/b566/translation-tool">View Demo</a>
    ·
    <a href="https://git.oth-aw.de/b566/translation-tool/issues/new?labels=bug">Report Bug</a>
    ·
    <a href="https://git.oth-aw.de/b566/translation-tool/issues/new?labels=enhancement">Request Feature</a>
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

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

* [Docker](https://www.docker.com/)
* [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate)
* [Flask](https://flask.palletsprojects.com/)
* [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
* [eventlet](https://pypi.org/project/eventlet/)
* [Bootstrap](https://getbootstrap.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- WSL2 (on Windows, required for Docker Desktop)

### Installation

Clone the repository:

```bash
git clone https://git.oth-aw.de/b566/translation-tool
cd translation-tool
```

Then start the container:

```bash
docker compose up --build -d
```

Development mode:

```bash
docker compose -f docker-compose.dev.yml up --build -d
```

> `--build` ensures a fresh build. `-d` runs it in detached mode.

### Environment Configuration

You can limit which language models LibreTranslate loads by setting the `LT_LOAD_ONLY` variable in `env/prod.env` or `env/dev.env`:

```env
LT_LOAD_ONLY=de,en
```

> ⚠️ If you do **not** set `LT_LOAD_ONLY`, **all models will be loaded**.  
> This slows down the **very first container startup after a fresh build**, as all models are downloaded and initialized.  
> **After the first startup, the models are cached and subsequent starts are much faster.**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Once the containers are running:

- Visit [http://localhost](http://localhost) in your browser
- Or open Docker Desktop and click on the mapped port (usually `80:5000`)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

- [X] Upload progress bar
- [ ] Drag & Drop upload UI
- [ ] Persistent translation history
- [ ] User authentication
- [ ] Glossary / translation memory

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Wolfgang Weigl – [LinkedIn](https://linkedin.com/in/wolfgang-weigl-933885236/)  
Project Link: [https://git.oth-aw.de/b566/translation-tool](https://git.oth-aw.de/b566/translation-tool)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/b566/translation-tool.svg?style=for-the-badge -->
<!-- [contributors-url]: https://git.oth-aw.de/b566/translation-tool/graphs/contributors -->
<!-- [forks-shield]: https://img.shields.io/github/forks/b566/translation-tool.svg?style=for-the-badge -->
<!-- [forks-url]: https://git.oth-aw.de/b566/translation-tool/network/members -->
<!-- [stars-shield]: https://img.shields.io/github/stars/b566/translation-tool.svg?style=for-the-badge -->
<!-- [stars-url]: https://git.oth-aw.de/b566/translation-tool/stargazers -->
<!-- [issues-shield]: https://img.shields.io/github/issues/b566/translation-tool.svg?style=for-the-badge -->
<!-- [issues-url]: https://git.oth-aw.de/b566/translation-tool/issues -->
[license-shield]: https://img.shields.io/badge/license-MIT-blue
[license-url]: https://git.oth-aw.de/b566/translation-tool/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/wolfgang-weigl-933885236/
