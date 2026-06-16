from langchain.tools import tool
import wikipedia


@tool
def search_wiki(query: str):
    """
    Used to search for information on Wikipedia.
    Returns the information found on Wikipedia.
    """
    print(f"[TOOL_CALLED] search_wiki with query: {query}")

    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.summary(e.options[0], sentences=3)
    except wikipedia.exceptions.PageError as e:
        return f"No Wikipedia page found for '{query}'"
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"
