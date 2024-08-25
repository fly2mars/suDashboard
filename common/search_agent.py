# Copyright (c) 2024 [fly2mars@gmail.com]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
This module implements the [SearchAgent] for the suKBAgent library.

Return a dict {url: content} with {num_search} of items.
"""
# -----------------------------------------------------------------------------

from googlesearch import search
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import sys

from common.base_agent import BaseAgent

class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.num_search = 10
        self.search_time_limit = 5
        self.total_timeout = 6

    def form_intentions(self):
        self.intentions = ['perform_search', 'parse_webpages']

    def execute_intentions(self):
        if 'perform_search' in self.intentions:
            query = self.beliefs["query"]
            urls = self.perform_search(query)
            if 'parse_webpages' in self.intentions:
                return self.parse_webpages(urls)

    def perform_search(self, query):
        num_search = self.num_search
        return list(search(query, num_results=num_search))

    def parse_webpages(self, urls):
        with ThreadPoolExecutor(max_workers=len(urls)) as executor:
            future_to_url = {executor.submit(self.fetch_webpage, url): url for url in urls}
            return {url: page_text for future in as_completed(future_to_url) if (url := future.result()[0]) and (page_text := future.result()[1])}

    def fetch_webpage(self, url):
        start = time.time()
        sys.settrace(self.trace_function_factory(start))
        try:
            response = requests.get(url, timeout=self.search_time_limit)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            paragraphs = soup.find_all('p')
            page_text = ' '.join([para.get_text() for para in paragraphs])
            return url, page_text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        finally:
            sys.settrace(None)
        return url, None

    def trace_function_factory(self, start):
        def trace_function(frame, event, arg):
            if time.time() - start > self.total_timeout:
                raise TimeoutError('Website fetching timed out')
            return trace_function
        return trace_function

    def run(self, query, context=""):
        self.update_belief("query", query)
        self.form_intentions()
        return self.execute_intentions()

if __name__ == "__main__":
    agent = SearchAgent()
    query = "site:shu.edu.cn 项目"

    result = agent.run(query)
    print(f"Search results for '{query}':")
    for url, content in result.items():
        print(f"URL: {url}")
        decoded_content = content[:100].encode('latin1').decode('utf-8', errors='ignore')
        print(f"Content snippet: {decoded_content}...")



