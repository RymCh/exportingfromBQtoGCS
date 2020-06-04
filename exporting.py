from google.cloud import bigquery
import argparse
#Every package uses a Client as a base for interacting with an API.
client = bigquery.Client()
#you should download a service account JSON keyfile and point to it using an environment variable:
client = client.from_service_account_json(
    '/path/to/keyfile.json')  # Use service account credentials
bucket_name = "my_bucket_name"
project = "my_project"
dataset_id = "my_dataset_id"   # The bigquery dataset (input)

parser = argparse.ArgumentParser()
parser.add_argument("-t",
                    "--table_id",
                    help=" -t <table_id> "
                    )
parser.add_argument("-f",
                    "--file_id",
                    help="-f <file_id> "
                    )
args = parser.parse_args()
table_id = args.table_id
file_id = args.file_id

# path of the file in GCS
destination_uri = "gs://{}/{}".format(bucket_name,file_id)
dataset_ref = client.dataset(dataset_id, project=project)
table_ref = dataset_ref.table(table_id)

# Asynchronous job of extracting data to Cloud storage
extract_job = client.extract_table(
    table_ref,
    destination_uri
)
extract_job.result()  # result() starts the job and wait for it to complete

print(
    "Exported {}:{}.{} to {}".format(
        project, dataset_id, table_id, destination_uri)
)
