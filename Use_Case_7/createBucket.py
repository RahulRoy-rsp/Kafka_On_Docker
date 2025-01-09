import boto3 # pip install boto3

# Create a session using the environment variables you've set
session = boto3.Session(
    aws_access_key_id='', # aws_access_key_id of your localstack
    aws_secret_access_key='', # aws_secret_access_key of your localstack
    region_name='us-east-1' 
)

# Create an S3 client
s3 = session.client('s3', endpoint_url='http://<endpoint>:<port>') # replace <endpoint> with localhost/IP address or how you set up in your docker file, also replace <port> as per localstack's configuration

# Create a new bucket
bucket_name = '' # bucket-name
s3.create_bucket(Bucket=bucket_name)

print(f'Bucket {bucket_name} created successfully!')
