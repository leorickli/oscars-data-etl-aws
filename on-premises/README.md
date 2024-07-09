# README.md

This project contains code to fetch and process film data, including budget conversion to USD. The code fetches data from a specified URL, extracts and cleans necessary information, and converts budget values to USD. The final data is saved in a CSV file.

## Requirements

To run this code, you need the following libraries:

- `pandas`
- `requests`
- `re`

You can install these libraries using `pip`:

```sh
pip install pandas requests
```

## Assumptions

- The budget values are given in different currencies (USD, GBP, EUR) and need to be converted to USD.
- The exchange rates are fetched from an API.
- If the budget is zero or a range, it will be set to 0.
- The input data is in JSON format, accessible via a specified URL.

## Instructions

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Install the required libraries:**
    ```sh
    pip install pandas requests
    ```

3. **Run the code:**

    - Ensure the URL for fetching JSON data is set correctly in the code.
    - Make sure to replace `'your_api_key_here'` with your actual API key for the [exchange rate API](https://www.exchangerate-api.com/).
    - Run the script to fetch, process, and convert the budget data:

## Example Usage

The script fetches film data from a specified URL, processes the data to clean and convert budget values, and saves the result in `films.csv`.

## Notes

- Ensure the URL provided for fetching the JSON data is accessible and returning the expected format.
