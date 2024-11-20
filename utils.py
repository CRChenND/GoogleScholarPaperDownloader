import csv
import logging
import os

# Setup logging with the configurable log file path
def setup_logging(log_file="crawler.log"):
    """
    设置日志记录，输出到控制台和日志文件
    :param log_file: 日志文件路径，默认值为 'crawler.log'
    """
    # 创建一个 logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG（记录所有级别的日志）

    # 创建一个控制台日志处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # 控制台输出级别设置为 INFO

    # 创建一个文件日志处理器
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # 文件输出级别设置为 DEBUG

    # 设置日志格式
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # 将处理器添加到 logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.info(f"Logging started. Logs will be saved to {log_file}")


def read_from_csv(csv_file="data/papers.csv"):
    """
    Read list of papers from a CSV file.
    :param csv_file: Path to the CSV file to read the data from.
    :return: List of dictionaries containing paper data.
    """
    papers = []
    try:
        if not os.path.exists(csv_file):
            logging.warning(f"CSV file {csv_file} does not exist.")
            return papers

        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                papers.append({"title": row["title"], "url": row["url"]})

        logging.info(f"Read {len(papers)} paper(s) from {csv_file}.")
    except Exception as e:
        logging.error(f"Error reading from CSV file {csv_file}: {str(e)}")
    
    return papers


# Save list of papers to a CSV file
def save_to_csv(papers, csv_file="data/papers.csv"):
    """
    Save list of papers to a CSV file.
    :param papers: List of dictionaries containing paper data.
    :param csv_file: Path to the CSV file to save the data.
    """
    # Create the directory for the CSV file if it doesn't exist
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "url"])
        writer.writeheader()
        writer.writerows(papers)

    logging.info(f"Saved {len(papers)} paper(s) to {csv_file}.")

# Remove duplicates based on paper titles
def remove_duplicates(papers):
    seen_titles = set()
    unique_papers = []

    for paper in papers:
        if paper["title"] not in seen_titles:
            unique_papers.append(paper)
            seen_titles.add(paper["title"])

    logging.info(f"Removed {len(papers) - len(unique_papers)} duplicate papers.")
    return unique_papers
