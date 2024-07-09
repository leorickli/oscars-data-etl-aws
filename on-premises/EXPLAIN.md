# EXPLAIN.md

## Approach

This project involves extracting and processing data about Oscar-nominated films. The objective is to fetch data from a given URL, clean and process it, and finally convert it into a structured format suitable for further analysis. Below is a detailed explanation of the approach taken and the assumptions made.

### 1. Libraries

- pandas: Used for data manipulation and analysis.
- requests: Used for making HTTP requests to fetch data from the web.
- re: Used for regular expression operations to clean and extract specific patterns in strings.

### 2. Extract
Extraction was pretty straight forward. When the word "scraping" appeared in the challenge, my first thought was thinking about Scrapy, my favorite web-scraping tool. In the end it was just a simple request made via HTTP to a website. Anyway, I like to raise an exception on http requests, even a simple one like this might break someday.

I tried to extract and pre-transform every data that I could in this section, this is why I took the luxury of transforming the "year" field at this stage, along with the fact that it's in the same level of the "films" key; reserving the more robust transformations in the "Transform" stage for the "budget" field. The rest of the fields were pretty straight-forward.

I learned a lot about regex on CS50 Python (my favorite Python course), the regex part was a blessing in this project, specially when I discovered I can match groups inside the regex expression.

### 3. Transform
I really thought this would be an easy project, until I started working on the "budget" field. This was harder that I would expect, specially on the rows containing the "million"s.

I managed to create a pretty nice solution for the values inside a range, until I realized that ranged those ranged rows should just be zeroed out. Oh well... I commented out this snippet of code so it can be used some day in case it ever finds some use some day. It took some uncomfortable time to realize the differences between hyphens and dashes.

I believe I found a pretty elegant solution for converting the non USD budgets into USD by using the [exchangerate-api](https://www.exchangerate-api.com), but you will later find that this approach did not work so well on my cloud solution.

I came to realize that '£', '₤' were considered different currencies, the latter is named "lira" which is not used nowadays, so I considered as a pound too.
### 4. Load

This was also a straight-forward step, just saving it into CSV without the index (it wasn't asked for). For the cloud solution, I used parquet instead of CSV, it's a more mature and storage-efficient way of storing data in transit or at the end of the process.

## Assumptions

1. **URL Availability**: The URL provided will always be available and return valid JSON data.
2. **Budget Field**: The budget information may not always be available; hence, a default value of 0 is used.
3. **Year Extraction**: Assumes the presence of at least one four-digit year in the year field.
4. **Currency Conversion**: Assumes the availability of a valid API key and a functioning exchange rate API for currency conversion.
5. **Data Consistency**: Assumes the data structure in the JSON file remains consistent over time.

This approach ensures that data is fetched, cleaned, and processed efficiently, making it ready for further analysis or use in other applications.
