<div id="top"></div>

<!-- [![Contributors][contributors-shield]][contributors-url] -->
<!--[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
 -->
<!-- PROJECT LOGO -->

<br />
<div align="center">
    <img src="https://www.orbiosolutions.com/images/orbioLogo.png" alt="Logo"> 
  </a>

  <h3 align="center">Ottix-How | Proof Of Concept </h3>
    <a href="https://github.com/Orbioadmin/OrbioOttixHow">View Demo</a>
    ·
    <a href="https://github.com/Orbioadmin/OrbioOttixHow/issues">Report Bug</a>
    ·
    <a href="https://github.com/Orbioadmin/OrbioOttixHow/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <!-- <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
OttixHow is an analytics-based platform used by the brand owners, retailers, and distributers etc irrespective of any Industry to analyze their products and sales. Platform allows the organization to upload their product and sales data for detail analysis to be performed. Platform also extracts data, transform analyze and present it for the organizations to automate their competitive and strategic decision making. The in-built intelligence engine provides various analysis which includes competitor analysis promotional and pricing analysis.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Scrapy](https://scrapy.org/)
* [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

* Clone the repo
  ```sh
  git clone https://github.com/Orbioadmin/OrbioOttixHow.git
  ```
* Initialize pipenv
  ```sh
  pipenv shell
  ```

### Prerequisites

- Create a virtual environment with python 3.9.13.
- Install pre commit hook, add `flake8` as a pre-commit hook.
- Install [Mongodb 6.0.1](https://www.mongodb.com/docs/manual/installation/)

### Installation

* Install dependencies
  ```sh
  pip install ottixhow/requirements.txt
  ```


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage
* Always run migrations after pulling the latest code.
  ```sh
  cd ottixhow
  python manage.py migrate
  ```
* start development server
  ```sh
  python manage.py runserver
  ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap
- [ ] Back end
  - [ ] Back end support for dashboard APIs
  - [ ] Back end support for user management
  - [ ] Back end for crawls management
- [ ] Crawlers
  - [ ] Dynamic crawling using keyword
    - [ ] amazon.in
    - [ ] flipkart.com
    - [ ] Myntra.com
  - [ ] Integration with backend
- [ ] User Interface
  - [ ] Dashboard
    - [ ] Add new dashboard
    - [ ] Input a keyword/category item
    - [ ] Select products to monitor
  - [ ] Remove a dashboard
  - [ ] User login
  - [ ] User creation

See the [open issues](https://github.com/Orbioadmin/OrbioOttixHow/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

Your Name - [@your_twitter](https://twitter.com/your_username) - email@example.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#top">back to top</a>)</p>

## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Malven's Flexbox Cheatsheet](https://flexbox.malven.co/)
* [Malven's Grid Cheatsheet](https://grid.malven.co/)
* [Img Shields](https://shields.io)
* [GitHub Pages](https://pages.github.com)
* [Font Awesome](https://fontawesome.com)
* [React Icons](https://react-icons.github.io/react-icons/search)

<p align="right">(<a href="#top">back to top</a>)</p>



MARKDOWN LINKS & IMAGES
https://www.markdownguide.org/basic-syntax/#reference-style-links

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/Orbioadmin/OrbioOttixHow/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/Orbioadmin/OrbioOttixHow/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/Orbioadmin/OrbioOttixHow/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/Orbioadmin/OrbioOttixHow/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/Orbioadmin/OrbioOttixHow/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png -->