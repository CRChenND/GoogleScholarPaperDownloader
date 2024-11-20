import requests
import logging
from utils import read_from_csv, save_to_csv

class DatabaseCrawler:
    def __init__(self, api_key, cse_id):
        """
        初始化 DatabaseCrawler。
        :param api_key: Google Custom Search API key
        :param cse_id: Google Custom Search Engine ID
        """
        self.api_key = api_key
        self.cse_id = cse_id
        self.logger = logging.getLogger(__name__)

    def crawl(self, database, query, max_results=None, csv_file="data/papers.csv"):
        """
        使用 Google Custom Search API 搜索 database。
        :param database: 要查询的database域名，如 dl.acm.org， aclanthology.org，ieeexplore.ieee.org
        :param query: 查询字符串
        :param max_results: 最大返回结果数，若为 None 则抓取所有结果
        :return: 包含搜索结果的列表
        """
        results = read_from_csv(csv_file)
        retrieved_paper_num = 0
        try:
            # API URL
            url = "https://customsearch.googleapis.com/customsearch/v1"
            start_index = 1  # Google Custom Search 每次最多返回 10 个结果，分页从 1 开始

            while max_results is None or retrieved_paper_num < max_results:
                params = {
                    "key": self.api_key,
                    "cx": self.cse_id,
                    "q": f"site:{database} {query}", 
                    "start": start_index
                }

                self.logger.info(f"Querying Google Custom Search API: {params}")
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                # 解析结果
                if "items" in data:
                    for item in data["items"]:
                        title = item.get("title")
                        link = item.get("link")

                        # 日志中记录标题
                        self.logger.info(f"Found result: {title}")

                        # 添加到结果列表
                        results.append({
                            "title": title,
                            "url": link,
                        })

                        retrieved_paper_num += 1

                        # 若 max_results 不为 None 并且达到了限制，停止抓取
                        if max_results is not None and retrieved_paper_num >= max_results:
                            break
                    save_to_csv(results)

                # 检查是否有更多结果
                if "nextPage" in data.get("queries", {}):
                    start_index = data["queries"]["nextPage"][0]["startIndex"]
                else:
                    break  # 没有更多结果，终止循环

        except Exception as e:
            self.logger.error(f"Error during Google Custom Search: {str(e)}")
        return 0
