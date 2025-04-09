import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def lambda_handler(event, context):
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    
    try:
        response = http.get("https://jsonplaceholder.typicode.com/todos/1", timeout=15)
        response.raise_for_status()
        # Process the response data here
        return {
            'statusCode': 200,
            'body': response.json()
        }
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }
