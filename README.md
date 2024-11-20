# Paper Crawler

**Paper Crawler** is a tool for retrieving academic papers from multiple databases, including Google Scholar, ACM Digital Library, IEEE Xplore, ACL Anthology, and Arxiv.

## Features

- Supports crawling from popular academic databases.
- Retrieves paper titles and links and saves them to CSV format for further analysis.
- Includes customizable configuration to support additional databases via Google Custom Search API.

## How to Use

### 1. Clone the Repository

Clone this repository to your local folder:

```bash
git clone https://github.com/CRChenND/PaperCrawler.git
cd PaperCrawler
```

### 2. Install Dependencies
Ensure you have Python installed. Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

### 3. Configuration
1. Locate the ```config.template.json``` file in the root directory.
2. Make a copy of this file and rename it to ```config.json```:

```bash
cp config.template.json config.json
```

3. Open config.json and replace the placeholder values with your actual credentials and settings. 
4. Important: To avoid exposing sensitive information, ensure that ```config.json``` is excluded from version control. This file is already included in ```.gitignore```.
   
### 4. Querying Additional Databases
To query additional databases, ensure you have:
- A valid [Google Custom Search API Key](https://developers.google.com/custom-search/v1/overview).
- A [Google Custom Search Engine ID](https://support.google.com/programmable-search/answer/12499034?hl=en) configured to include your target database.
Update the ```config.json``` file with these credentials.

### 5. Run the Tool
Run the tool by executing:

```bash
python main.py
```

### 6.Output
- Retrieved paper data will be saved in: ```data/papers.csv```.
- Logs for the crawling process can be found in: ```data/crawler.log```.


## Acknowledgements
This project is released under the MIT License. Feel free to use, modify, and share. If you'd like to cite this project, please use the following BibTeX entry:
```bibtex
@misc{paper_crawler,
  author       = {Chaoran Chen},
  title        = {Paper Crawler: A tool for academic paper retrieval},
  year         = {2024},
  publisher    = {GitHub},
  journal      = {GitHub Repository},
  howpublished = {\url{https://github.com/CRChenND/PaperCrawler.git}}
}
```

