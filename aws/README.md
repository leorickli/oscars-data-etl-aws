## Approach

<img width="695" alt="image" src="https://github.com/leorickli/oscars-data-etl-aws/assets/106999054/89c6e367-4b08-4482-bcd1-2b4154488b35">

This section of the project involves migrating the architecture implemented on-premises to the cloud. Given the small size of the date, there are much more cost-efficient approaches like ingesting data using Lambda, clean it completely and query it through Athena, but I wanted to use Glue because it's a much more mature way of dealing with data by using it's data catalog and better options for processing data by the use of Jupyter notebooks with Spark.

Of course, Redshift is kind of overkill in this situation too, Athena would be fine for analysis, but again, my intention here is to create a more "big data"-focused architecture.

Always assume the principle of least-privilege, you will see many times in this project a role like "AmazonS3FullAccess", this is not recommended in professional solutions. One should never have access to the full features of a service, unless this person is the admin.

### 1. [Extract with Lambda](https://github.com/leorickli/oscars-data-etl-aws/blob/main/aws/extract.py)
Lambda (and FaaS (Function-as-a-Service) tools like Cloud SQL and Azure Functions) is the go-to ingestion tool for periodically (daily or hourly) ingestion of data, perfect for ingesting data from APIs through HTTP requests. This is why it was used here, although not quite friendly with the "requests" library, "urllib3" ended up being a more mature and viable solution for Lambda.

On the cloud, it's nice to use the "medallion architecture", I tried to apply this principle by writing data into the bronze (raw) layer, where the data should be written "as-is". I actually transform every data type to string so I can further process it better in the next layers.

Parquet is our friend here, it stores data in a more compact form compared to CSV. It also stores data in columnar format, much appreciated by Redshift and other OLAP tools like BigQuery.

It's possible to create a trigger for that function using CloudWatch as a scheduler, so data is requested on a daily basis.

Increase the timeout of the function to at least 3 minutes so you don't get timeout errors.

*IAM Policies*: AmazonS3FullAccess, AWSLambdaBasicExecutionRole.

### 2. [Transform and Load with Glue](https://github.com/leorickli/oscars-data-etl-aws/blob/main/aws/transform_and_load.ipynb)

<img width="973" alt="SCR-20240709-brnq" src="https://github.com/leorickli/oscars-data-etl-aws/assets/106999054/729897ed-fae5-4c75-a195-9520cfda9b3d">

The hardest part of the project, not because of Glue, but because of the connections required for the other resources. This is the series of steps I took to successfully get data from the bronze layer in the S3 bucket to Redshift for analysis:

1. Create a crawler to get and catalog the data from the bronze layer, we will use the data from this catalog as a starting point for our Jupyter notebook.
2. Connect the Redshift database to Glue by inserting credentials and the JDBC connection on it, so we can call this database through the magic command `%connections`. This is an easier way of exporting data from Glue to Redshift.
3. Start the ETL job by creating a Jupyter notebook, use the policies down below for the chosen IAM role.
4. The main processing part is pretty similar to the on-premises version, but here we have to transition from DataFrames to get the desired results.
5. The [exchangerate-api](https://www.exchangerate-api.com) consistently failed me when I tried using it on our data, even though I tested it with a small sample of data (and it worked). I ended up hard-coding the conversion value inside the code, but there are other more elegant solutions like scheduling a Lambda function to give us the daily exchange rate so we query that to the notebook.
6. Always infer your schema explicitly when writing to a database tool like Redshift of BigQuery. If you don't do that, it will almost always get it wrong. For this case, it created ghost fields that had null values.
7. Once you get your database connected to the notebook through the use of `%connections`, it's easy to write data to Redshift. Just make sure you insert a valid and existing bucket for the temp files.

*IAM Policies*: AmazonS3FullAccess, AWSGlueServiceRole, AmazonRedshiftFullAccess, custom PassRolePolicy (allows an AWS service or user to pass an IAM role to another service).
```json
{
	"Version": "2012-10-17",
	"Statement": [
		{
			"Effect": "Allow",
			"Action": "iam:PassRole",
			"Resource": "arn:aws:iam::058264438444:role/service-role/AWSGlueServiceRole-s32rds"
		}
	]
}
```
### 3. Analysis

Once the data is inside Redshift, it's ready for some robust SQL analysis.

<img width="1374" alt="SCR-20240709-ciad" src="https://github.com/leorickli/oscars-data-etl-aws/assets/106999054/66e0e4c7-823c-4955-9a8f-7a8092cdb664">

