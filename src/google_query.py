from googlesearch import search

def generate_google_res(query, num_results=5):
    """
    Perform a Google search for the given query and return a formatted string.

    The string contains links retrieved from the search results, with headings as references.

    Args:
        query (str): The search query to perform on Google.
        num_results (int): The number of search results to retrieve. Default is 5.

    Returns:
        str: A formatted string containing links as references.
    """
    try:
        # Perform the search and retrieve the top results
        search_results = search(query, num_results=num_results)

        # Format the string with headings and links
        result_string = f"Search results for: {query}\n\n"

        for index, url in enumerate(search_results, start=1):
            result_string += f"Link {index}: {url}\n"

        return result_string

    except Exception as e:
        return f"Error during search: {e}"

if __name__ == "__main__":
    # Example usage
    query = "Python web scraping tutorials"
    result_docstring = generate_google_res(query)
    print(result_docstring)
