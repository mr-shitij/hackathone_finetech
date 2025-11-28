from duckduckgo_search import DDGS
from crewai.tools import tool

@tool("Search the internet")
def search_tool(query: str) -> str:
    """
    Useful for searching the internet to find financial data, product information, and market trends.
    
    Args:
        query: The search query string
    
    Returns:
        Search results as a string
    """
    try:
        results = list(DDGS().text(query, max_results=5))
        if not results:
            return "No search results found."
        
        output = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', 'No description')
            url = result.get('href', '')
            output.append(f"{i}. {title}\n   {body}\n   URL: {url}\n")
        
        return "\n".join(output)
    except Exception as e:
        return f"Search failed: {str(e)}"
