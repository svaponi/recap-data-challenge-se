import os

if __name__ == "__main__":
    from app.api_client import APIClient
    from app.processor import process

    endpoint = os.getenv(
        "ENDPOINT_URL",
        "http://localhost:8007/invoices",
    )

    client = APIClient(endpoint)
    results = process(client, max_workers=4)

    for item in results:
        print(item)
