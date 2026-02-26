"""
Web search functionality using DuckDuckGo
"""

from duckduckgo_search import DDGS


def web_search(query, max_results=5):
    """
    Search the web using DuckDuckGo
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
        
    Returns:
        list: List of search results with title, snippet, and URL
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))
        
        search_results = []
        for result in results:
            search_results.append({
                'title': result.get('title', ''),
                'snippet': result.get('body', ''),
                'url': result.get('href', '')
            })
        
        return search_results
    except Exception as e:
        print(f"Search error: {e}")
        return []


def format_search_context(search_results):
    """
    Format search results into context string for AI
    
    Args:
        search_results (list): List of search result dictionaries
        
    Returns:
        str: Formatted search context
    """
    if not search_results:
        return ""
    
    search_context = "\n\nWEB SEARCH RESULTS:\n"
    for i, result in enumerate(search_results, 1):
        search_context += f"\n{i}. {result['title']}\n"
        search_context += f"   {result['snippet']}\n"
        search_context += f"   Source: {result['url']}\n"
    
    return search_context


def needs_web_search(query, search_keywords):
    """
    Determine if a query needs web search based on keywords
    
    Args:
        query (str): User query
        search_keywords (list): List of keywords that trigger search
        
    Returns:
        bool: True if search is needed
    """
    return any(keyword in query.lower() for keyword in search_keywords)