import logging
import json
import requests
from triplea.config.settings import SETTINGS

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

session = requests.Session()

def extract_topic(text: str, method: str, top: int = 10, threshold: float = 0) -> list:
    """Extracts topics from a given text using a specified method via an API.

    This function sends a POST request to a topic extraction API endpoint with the provided text,
    method, and optional parameters for the number of topics and a threshold. It handles proxy settings,
    authentication, and various error scenarios, returning a list of extracted topics or raising
    appropriate exceptions.

    Args:
        text: The input text to analyze for topic extraction.
        method: The topic extraction method to use (e.g., 'LDA', 'NMF').
        top: The number of top topics to return (default: 10).
        threshold: The minimum relevance score for topics (default: 0).

    Returns:
        A list of extracted topics from the API response.

    Raises:
        ValueError: If the input text is empty or method is invalid.
        requests.exceptions.Timeout: If the API request times out.
        requests.exceptions.HTTPError: If the API returns an HTTP error status.
        requests.exceptions.ConnectionError: If a connection error occurs.
        json.JSONDecodeError: If the API response cannot be parsed as JSON.
        KeyError: If the expected 'status' or 'r' keys are missing in the response.

    Examples:
        >>> text = "This is a sample text about machine learning and AI."
        >>> topics = extract_topic(text, method="LDA", top=5, threshold=0.1)
        >>> print(topics)
        ['machine learning', 'artificial intelligence', ...]
    """
    # Input validation
    if not text or not text.strip():
        logger.error("Input text is empty or contains only whitespace.")
        raise ValueError("Text cannot be empty or whitespace.")
    if not method or not isinstance(method, str):
        logger.error("Invalid or missing topic extraction method.")
        raise ValueError("Method must be a non-empty string.")

    # Construct API URL and payload
    url = f"{SETTINGS.AAA_TOPIC_EXTRACT_ENDPOINT}/"
    data = {
        "Text": text.replace("\n", " "),  # Replace newlines for API compatibility
        "Method": method,
        "Top": top,
        "Threshold": threshold,
    }

    headers = {
        "User-Agent": SETTINGS.AAA_CLIENT_AGENT,
        "Content-Type": "application/json",
    }

    # Configure proxy settings if available
    proxy_servers = {
        "http": SETTINGS.AAA_PROXY_HTTP,
        "https": SETTINGS.AAA_PROXY_HTTPS,
    } if SETTINGS.AAA_PROXY_HTTP else None

    # Send POST request to the API
    try:
        j_data = json.dumps(data)
        logger.debug(f"Sending POST request to {url} with data: {j_data}")
        response = session.post(
            url=url,
            data=j_data,
            headers=headers,
            proxies=proxy_servers,
            timeout=10  # Set a reasonable timeout
        )
        response.raise_for_status()  # Raises HTTPError for bad status codes

    except requests.exceptions.Timeout as e:
        logger.error(f"Request to {url} timed out after 10 seconds.")
        raise requests.exceptions.Timeout("API request timed out.") from e
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error while contacting {url}.")
        raise requests.exceptions.ConnectionError("Failed to connect to the API.") from e
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error {response.status_code} received from {url}.")
        if response.status_code == 404:
            logger.warning("Topic extraction endpoint not found.")
            return []  # Return empty list for non-critical 404 error
        raise requests.exceptions.HTTPError(
            f"HTTP error {response.status_code} occurred."
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error during API request to {url}: {str(e)}")
        raise

    # Parse API response
    try:
        data = response.json()
        logger.debug(f"Received response: {data}")
        if "status" in data and "r" in data:
            return data["r"]
        else:
            logger.error("Response missing 'status' or 'r' key.")
            raise KeyError("Invalid response format: 'status' or 'r' key missing.")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response from {url}: {str(e)}")
        raise json.JSONDecodeError(
            "Invalid JSON response from API.", e.doc, e.pos
        ) from e
    except Exception as e:
        logger.error(f"Unexpected error processing response from {url}: {str(e)}")
        raise