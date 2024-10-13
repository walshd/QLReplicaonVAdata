<a id="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/walshd/QLReplicaonVAdata">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Replica Queenslander Generous Interface for V&A collection</h3>

  <p align="center">
    This is a replica of the Queenslander Generous Interface for the V&A collection. The data is sourced from the V&A API and cached in a local JSON file. 
    The idea for reproducing is to both learn about the features of generating a generous interface and to provide a useful tool for exploring the V&A collection. By using the api it has also raised a few issues (data clarity and consistency and also api request limits) to consider when createing generous interfaces.
    <!-- <br /> -->
    <!-- <a href="https://github.com/github_username/repo_name">View Demo</a> -->
  </p>
</div>




<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To set up this project locally, follow these steps:

### Prerequisites

* Python 3.7+
* pip (Python package installer)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/walshd/QLReplicaonVAdata
   ```
2. Navigate to the project directory
   ```sh
   cd QLReplicaonVAdata
   ```
3. Create a virtual environment
   ```sh
   python -m venv venv
   ```
4. Activate the virtual environment
   ```sh
   # On Windows
   venv\Scripts\activate
   # On macOS and Linux
   source venv/bin/activate
   ```
5. Install required packages
   ```sh
   pip install -r requirements.txt
   ```
6. Run the Flask application
   ```sh
   flask run
   ```

The application should now be running on `http://localhost:5000`.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

This Flask-based application provides a generous interface (attempt at a replica f Whitelaws Queenslander interface) for exploring the V&A collection. Here are some ways to use it:

1. Open your web browser and navigate to `http://localhost:5000`.
2. Browse the collection by category, material, or time period.
3. Use the search function to find specific items or themes.
4. Click on individual items to view detailed information and high-resolution images.
5. Use the timeline feature to explore the collection chronologically.

The data is sourced from the V&A API and cached locally to improve performance and manage API request limits.

<!-- For a live demo and more detailed usage instructions, please visit our [project website](https://example.com/demo). -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Basic Flask application setup
- [x] V&A API integration
- [x] Local data caching implementation
- [x] Add item grid view feature
- [x] Add timeline visualization feature
- [-] Add wordcloud visualization feature
- [ ] Improve UI/UX design
- [ ] Optimize performance for large datasets
- [ ] Add unit tests and integration tests

See the [open issues](https://github.com/walshd/QLReplicaonVAdata/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [V&A Museum](https://www.vam.ac.uk/) for providing the open access API and collection data
* [Mitchell Whitelaw](https://mtchl.net/) for his pioneering work on generous interfaces
* [Queenslander Generous Interface](https://github.com/StateLibraryQueensland/queenslander) by State Library of Queensland, which inspired this project
* [Flask](https://flask.palletsprojects.com/) for the web framework
* [Requests](https://docs.python-requests.org/) for handling API requests
* [Bootstrap](https://getbootstrap.com) for responsive design components
* [Font Awesome](https://fontawesome.com) for icons
* [GitHub Pages](https://pages.github.com) for hosting the project documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>



