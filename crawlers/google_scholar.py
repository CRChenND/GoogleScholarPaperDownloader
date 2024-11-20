import requests
from bs4 import BeautifulSoup
import random
import time
import logging
from utils import read_from_csv, save_to_csv
import re

class GoogleScholarCrawler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

    def _get_headers(self):
        return {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }

    def _get_page(self, url):
        """Get the page content."""
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                self.logger.warning(f"Failed to fetch page. Status code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error occurred while fetching the page: {e}")
            return None

    def get_total_results(self, query):
        """Get the total number of papers from Google Scholar."""
        search_url = f'https://scholar.google.com/scholar?hl=en&q={query}'
        page_content = self._get_page(search_url)
        if not page_content:
            return 0
        
        soup = BeautifulSoup(page_content, 'html.parser')
        result_text = soup.find('div', {'id': 'gs_ab_md'}).get_text(strip=True)
        
        try:
            raw_total_results = result_text.split(' ')[1].replace(',', '').replace('.', '')
            total_results = int(raw_total_results)
            self.logger.info(f"Total results found: {total_results}")
            return total_results
        except (AttributeError, ValueError) as e:
            self.logger.error(f"Error parsing total results: {e}")
            return 0

    def crawl(self, query, max_results=None, csv_file="data/papers.csv"):
        """Crawl Google Scholar papers based on a query."""
        self.logger.info(f"Starting Google Scholar search for query: {query}")
        
        total_results = self.get_total_results(query)
        if total_results == 0:
            self.logger.info("No results found.")
            return []

        max_pages = total_results // 10 + (1 if total_results % 10 > 0 else 0)
        results = read_from_csv(csv_file)
        total_fetched = 0

        for page_num in range(0, max_pages):
            # If max_results is specified and total fetched results meet or exceed it, stop crawling
            if max_results is not None and total_fetched >= max_results:
                break

            self.logger.info(f"Fetching page {page_num + 1} of {max_pages}...")
            page_url = f'https://scholar.google.com/scholar?hl=en&q={query}&start={page_num * 10}'
            page_content = self._get_page(page_url)

            if not page_content:
                continue

            soup = BeautifulSoup(page_content, 'html.parser')

            for result in soup.find_all('div', class_='gs_ri'):
                # If max_results is specified and total fetched results meet or exceed it, stop crawling
                if max_results is not None and total_fetched >= max_results:
                    break

                title_tag = result.find('h3', class_='gs_rt')
                title = title_tag.get_text(strip=True) if title_tag else 'No Title'
                
                # Clean title by removing content in [], e.g., [HTML] and [PDF]
                title = re.sub(r'\[.*?\]', '', title).strip()

                url = title_tag.a['href'] if title_tag and title_tag.a else None

                results.append({
                    'title': title,
                    'url': url
                })
                total_fetched += 1

                self.logger.info(f"Fetched paper: {title}")

            # Save results to CSV after processing each page
            save_to_csv(results, csv_file)

            time.sleep(random.uniform(2, 5))

        self.logger.info(f"Total papers fetched: {total_fetched}")
        return 0
