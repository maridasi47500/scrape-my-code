import requests
import json
from bs4 import BeautifulSoup
import sys

def scrape_bing(query, programming_language, spoken_language="en", num_results=10):
    """
    Scrapes Bing search results for a given query, programming language, and spoken language.

    Parameters:
        query (str): The search query.
        programming_language (str): The programming language (e.g., Python, Java).
        spoken_language (str): The spoken language code (default is "en" for English).
        num_results (int): Number of results to return (default is 10).

    Returns:
        list: A list of dictionaries containing titles, links, snippets, and extracted code.
    """
    # Construct the Bing search URL with language parameter
    search_query = f"{query} {programming_language}"
    #print(search_query)
    url = f"https://www.bing.com/search?q={search_query.replace(' ', '+')}&count={num_results}&setlang={spoken_language}"
    
    # Set headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Send the request
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        #print(f"Failed to fetch Bing search results, status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract search results
    results = []
    for item in soup.find_all("li", class_="b_algo")[:num_results]:
        title = item.find("h2").text if item.find("h2") else "No Title"
        #print(title)
        link = item.find("a")["href"] if item.find("a") else "No Link"
        snippet = item.find("p").text if item.find("p") else "No Snippet"
        code_snippets = extract_code_from_page(link, programming_language)
        results.append({
            "title": title,
            "link": link,
            "snippet": snippet,
            "code_snippets": code_snippets
        })
    
    return results

def extract_code_from_page(url, programming_language):
    """
    Extracts code snippets and programming language-specific content from a webpage.

    Parameters:
        url (str): The URL of the webpage.
        programming_language (str): The programming language to filter by.

    Returns:
        list: A list of extracted code snippets and relevant content.
    """
    # Set headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Define keywords for filtering based on the programming language
    keywords = {
        "python": ["#print", "x=", "str(", "def ", "import ", "class "],
        "java": ["System.out.#print", "int ", "String ", "class ", "public ", "void "]
    }
    
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            #print(f"Failed to fetch the page: {response.status_code} for URL: {url}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract code snippets inside <code>, <pre>, or <div> tags with keywords
        code_snippets = []
        for tag in soup.find_all(["code", "pre", "div"]):
            text = tag.get_text()
            for keyword in keywords.get(programming_language.lower(), []):
                if keyword in text:  # Check if any keyword matches
                    code_snippets.append(text.strip())
                    break  # Avoid appending the same block multiple times
        
        return code_snippets
    except requests.exceptions.RequestException as e:
        #print(f"Error fetching the page {url}: {e}")
        return []

if __name__ == "__main__":
    # Ensure proper usage
    if len(sys.argv) < 3:
        #print("Usage: python scrape_bing.py <query> <programming_language> [spoken_language]")
        sys.exit(1)

    # Get query, programming language, and optional spoken language from command line arguments
    query = sys.argv[1]
    programming_language = sys.argv[2]
    spoken_language = sys.argv[3] if len(sys.argv) > 3 else "en"  # Default to English

    # Get search results
    search_results = scrape_bing(query, programming_language, spoken_language)
    
    # Print the results with extracted code
    if search_results:
        #print("Search Results with Extracted Code:")
        json_str = json.dumps(search_results, indent=4)
        print(json_str)
        for i, result in enumerate(search_results, start=1):
            #print(f"{i}. {result['title']}")
            #print(f"   {result['link']}")
            #print(f"   {result['snippet']}")
            if result["code_snippets"]:
                #print("   Extracted Code:")
                for code_snippet in result["code_snippets"]:
                    #print(f"   ```\n{code_snippet}\n   ```")
                    print(f"")
            else:
                print("")
    else:
        #print("No results found.")
