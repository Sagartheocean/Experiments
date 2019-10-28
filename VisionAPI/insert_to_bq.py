from google.cloud import bigquery
from oauth2client.client import GoogleCredentials
from apiclient import discovery
import httplib2
import datetime
import csv

SCOPES = ['https://www.googleapis.com/auth/cloud-platform',
          'https://www.googleapis.com/auth/bigquery']

project_id ="cp-gaa-visualization-dev"
dataset = "cic_recommendation"
table = "image_full_detail_en"

def get_credentials():
    """Get the Google credentials needed to access our services."""
    credentials = GoogleCredentials.get_application_default()
    if credentials.create_scoped_required():
            credentials = credentials.create_scoped(SCOPES)
    return credentials


def create_bigquery_client(credentials):
    """Build the bigquery client."""
    http = httplib2.Http()
    credentials.authorize(http)
    return discovery.build('bigquery', 'v2', http=http, cache_discovery=False)

############################

def insert_to_bq_tuples(dataset, table, data):
    """using for inserting the data to bq tables"""
    client = bigquery.Client()
    dataset_id = dataset
    table_id = table
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)
    errors = client.insert_rows(table, data)
    print (errors)


def update_bq(dataset, table, dict_price,dict_size,dict_variant):
    """Not using it, kept it for reference. This method would update the value in the bigquery table finding the image as an index"""
    client = bigquery.Client()
    dataset_id = dataset
    table_id = table
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    for key in dict_price.keys():
         variants = "','".join(dict_variant[key])
         prices = "','".join(dict_price[key])
         sizes = "','".join(dict_size[key])
         QUERY = ("UPDATE `cp-gaa-visualization-dev.cic_recommendation.image_details` SET variant =['"+variants+"'] ,price=['"+prices+"'], size=['"+sizes+"'] where image_name = '"+key+"' and category='HC'" )
         query_job = client.query(QUERY)  # API request
         rows = query_job.result()  # Waits for query to finish
         print rows



def insert_bq_json(bigquery_client, project_id, dataset, table, data):
    """Not using it kept it for reference.
    Inserting the data in the bigquery in JSON format"""
    response = bigquery_client.tabledata().insertAll(
        projectId=project_id, datasetId=dataset,
        tableId=table, body=data).execute(num_retries=3)
    print "streaming response: %s %s" % (datetime.datetime.now(), response)
    print(response)



if __name__ == '__main__':
    credentials = get_credentials()

    # mode value would be : insert/update based on the operation type that we want to choose.
    operation_mode = "insert"

    # file to insert the data
    filename = 'C:\Users\Sagar Raythatha\Desktop\CIC\Extracted data\product_tab_uap.csv'
    with open(filename) as f:
        data = [tuple(line) for line in csv.reader(f)]

        if operation_mode == "insert":
            # for inserting the data to table
            insert_to_bq_tuples(dataset, table, data)

        elif operation_mode == "update":
            rows = []
            price_file = "C:\Users\Sagar Raythatha\Desktop\CIC\Extracted data\product_prices_oc.csv"
            with open(price_file, 'r') as csvfile:
                # creating a csv reader object
                csvreader = csv.reader(csvfile)

                # extracting field names through first row
                fields = csvreader.next()

                dict_price = {}
                dict_size = {}
                dict_variant = {}
                # extracting each data row one by one and keeping them in dictionary where key would  be
                # image name and value would be list of elements present.
                for row in csvreader:
                    if row[0] not in dict_price.keys():
                        dict_price[row[0]] = [row[2]]
                        dict_size[row[0]] = [row[3]]
                        dict_variant[row[0]] = [row[4]]
                    else:
                        dict_price[row[0]].append(row[2])
                        dict_size[row[0]].append(row[3])
                        dict_variant[row[0]].append(row[4])

            # for updating price, variant and size
            update_bq(dataset, table, dict_price, dict_size, dict_variant)


