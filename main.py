if __name__ == "__main__":
    from app.api_client import APIClient
    from app.processor import process

    client = APIClient(
        "https://nookdtmzylu7w75p7atatnzom40zmdpz.lambda-url.eu-central-1.on.aws/invoices"
    )
    results = process(client, max_workers=4)

    for item in results:
        print(item)
