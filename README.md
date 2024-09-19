# Recap Data Challenge SE

This document provides a brief explanation of the approach I used to solve the challenge, along with instructions to
reproduce the results.

## Approach

### Components

- **Processor** (entry point): Gathers and processes the data using multithreading. Outputs a list of tuples with the
  following structure:
    - Year/Month (as a tuple of integers)
    - Contract ID
    - Net Revenue
    - Churned Amount
- **Producer**: Collects data from the API and publishes it to a queue.
- **Consumer**: Consumes data from the queue and aggregates it.
- **PostProcessor**: Calculates the churned amount.
- **APIClient**: Retrieves data from the API.

### Process Flow

1. The **Processor** starts the **Producer** and **Consumer** in parallel using threads, waiting for them to complete.
2. The collected data is passed to the **PostProcessor** for further processing.
3. The final result is returned as a list of tuples.

> Note: I took the liberty of removing output items where both the net revenue and churned amount are zero.

## How to Run the Project

1. Clone the repository:

    ```bash
    git clone git@github.com:svaponi/recap-data-challenge-se.git
    cd recap-data-challenge-se
    ```

2. Install dependencies using [Poetry](https://python-poetry.org/docs/#installation):

    ```bash
    poetry install
    ```

3. Run the tests with [pytest](https://docs.pytest.org/en/stable/):

    ```bash
    poetry run pytest
    ```

4. Run the application against the production API:

    ```bash
    poetry run python main.py
    ```

## Observations

- The data source is a web API, which means most of the time will likely be spent waiting for I/O operations. While
  asynchronous operations could suffice, multithreading is preferred, assuming there are no significant CPU limitations
  on the machine running the code.
- The API supports pagination, suggesting that the total number of data items is not expected to exceed tens of
  thousands.
