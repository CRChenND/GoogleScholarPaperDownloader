import argparse
import json
import os
from utils import setup_logging, read_from_csv, save_to_csv, remove_duplicates
from crawlers.google_scholar import GoogleScholarCrawler
from crawlers.database import DatabaseCrawler

# Function to load config file
def load_config(config_file="config.json"):
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file '{config_file}' not found.")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Validate config
    if not isinstance(config.get("query"), str):
        raise ValueError("Query must be a string.")
    
    if not isinstance(config.get("sources"), list):
        raise ValueError("Sources must be a list.")
    
    if not all(source in ["google_scholar", "acm", "ieee", "acl", "arxiv"] for source in config["sources"]):
        raise ValueError("Invalid source in sources list.")

    return config

# Function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Fetch research papers from various databases.")
    parser.add_argument("-c", "--config", type=str, default="config.json", help="Path to the config file.")
    parser.add_argument("--query", type=str, help="The query to search papers with.")
    parser.add_argument("--sources", type=str, nargs="+", choices=["google_scholar", "acm", "ieee", "acl", "arxiv"], 
                        help="The sources to fetch papers from.")
    parser.add_argument("--max_results", type=str, default=None, help="The max results for the query. Default is None.")
    parser.add_argument("--csv_file", type=str, help="Path to save the CSV file.")
    parser.add_argument("--log_file", type=str, help="Path to save the log file.")
    parser.add_argument("--api_key", type=str, help="Your Google custom search api key.")
    parser.add_argument("--cse_id", type=str, help="Your Google custom search engine id.")
    
    return parser.parse_args()

# Main function to fetch papers
def main(config):
    csv_file = config.get("csv_file", "data/papers.csv")
    max_results = config["max_results"]
    query = config["query"]

    # Setup logging (log file path is now configurable)
    setup_logging(config.get("log_file", "data/crawler.log"))

    database = {
        "acm": "dl.acm.org",
        "acl": "aclanthology.org",
        "ieee": "ieeexplore.ieee.org",
        "arxiv": "arxiv.org" 
    }

    if "google_scholar" in config["sources"]:
        gs_crawler = GoogleScholarCrawler()
        gs_crawler.crawl(query, max_results)

    for db_key in database:
        if db_key in config["sources"]:
            api_key = config.get("api_key")
            cse_id = config.get("cse_id")
            if not api_key or not cse_id:
                raise ValueError(f"api_key and cse_id are required for crawling {db_key}.")

            db_crawler = DatabaseCrawler(api_key, cse_id)
            db_crawler.crawl(database[db_key], query, max_results, csv_file)

    all_papers = read_from_csv(csv_file)

    # 去重
    unique_papers = remove_duplicates(all_papers)

    # 保存结果 (save CSV to the user-defined path or default to "papers.csv")
    save_to_csv(unique_papers, csv_file)
    print(f"Fetched and saved {len(unique_papers)} unique papers to {csv_file}.")

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Load config from file
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
    
    # Override config with command-line arguments if provided
    if args.query:
        config["query"] = args.query
    if args.sources:
        config["sources"] = args.sources
    if args.max_results:
        config["max_results"] = args.max_results
    if args.csv_file:
        config["csv_file"] = args.csv_file
    if args.log_file:
        config["log_file"] = args.log_file
    if args.api_key:
        config["api_key"] = args.api_key
    if args.cse_id:
        config["cse_id"] = args.cse_id

    # Validate max_results
    try:
        if config["max_results"] == "None":
            config["max_results"] = None
        else:
            config["max_results"] = int(config["max_results"])
            if config["max_results"] <= 0:
                raise ValueError("max_results must be a positive integer or None.")
    except ValueError as e:
        print(f"Error: max_results must be a positive integer or None. {e}")
        exit(1)

    # Run the main function
    main(config)
