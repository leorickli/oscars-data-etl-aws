import json
import urllib3
import pandas as pd
import boto3
import re
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO

# Initialize urllib3 and boto3 clients
http = urllib3.PoolManager()
s3 = boto3.client('s3')

# Function to get the JSON data from the URL
def fetch_json_data(url):
    response = http.request('GET', url)
    if response.status == 200:
        return json.loads(response.data.decode('utf-8'))
    else:
        raise Exception(f"Failed to fetch data from {url}, status code: {response.status}")

# Function to clean the year field and extract the latest year mentioned
def extract_latest_year(year_text):
    match = re.search(r'(\d{2})(\d{2}) / (\d{2})', year_text)
    if match:
        return int(f"{match.group(1)}{match.group(3)}")
    else:
        # If the pattern does not match, fall back to finding the latest year
        matches = re.findall(r'\d{4}', year_text)
        if matches:
            return max(map(int, matches))
    return None

# Function to get the budget from the film's detail URL
def fetch_budget(url):
    try:
        response = http.request('GET', url)
        if response.status == 200:
            film_data = json.loads(response.data.decode('utf-8'))
            return str(film_data.get('Budget', '0'))  # Convert budget to string
        else:
            return '0'
    except:
        return '0'

def lambda_handler(event, context):
    # URL of the JSON file
    url = "http://oscars.yipitdata.com/"

    # Fetch data
    data = fetch_json_data(url)

    # Extract the required information
    films_data = []
    for year_data in data['results']:
        year = extract_latest_year(year_data.get('year', ''))
        for film in year_data['films']:
            detail_url = film.get('Detail URL')
            budget = fetch_budget(detail_url)
            film_info = {
                'film': str(film.get('Film', '')),
                'year': str(year),
                'wiki_url': str(film.get('Wiki URL', '')),
                'oscar_winner': str(film.get('Winner', '')),
                'budget': budget
            }
            films_data.append(film_info)

    # Convert to DataFrame
    films_df = pd.DataFrame(films_data)

    # Ensure all columns are strings
    for col in films_df.columns:
        films_df[col] = films_df[col].astype(str)

    # Convert DataFrame to Parquet
    table = pa.Table.from_pandas(films_df)
    buffer = BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)
    
    # Upload the Parquet file to S3
    s3.put_object(Bucket='yipitdata-bucket', Key='bronze/bronze_oscars_data.parquet', Body=buffer.getvalue())

    return {
        'statusCode': 200,
        'body': json.dumps('Data extracted and stored in S3 as Parquet')
    }