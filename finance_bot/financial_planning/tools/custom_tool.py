from duckduckgo_search import DDGS
from crewai.tools import BaseTool

class SearchTool(BaseTool):
    name: str = "Search"
    description: str = "Useful for searching the internet to find financial data, product information, and market trends."

    def _run(self, query: str) -> str:
        results = DDGS().text(query, max_results=5)
        return str(results)
