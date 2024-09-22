import asyncio
import os

if __name__ == "__main__":
    from app.api_client_async import APIClientAsync
    from app.processor_async import process

    endpoint = os.getenv(
        "ENDPOINT_URL",
        "http://localhost:8007/invoices",
    )

    client = APIClientAsync(endpoint)
    results = asyncio.run(process(client, max_workers=4))

    for item in results:
        print(item)
