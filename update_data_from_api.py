from sodapy import Socrata
import datetime
import math
import json
import csv



def check_update():
    results = client.get(socrata_dataset_identifier, where="test_date > '"+last_updated+"'", select="test_date, county, new_positives, cumulative_number_of_positives", limit=1)
    print("Checking update.....")
    return results

def update_data():
    results = client.get(socrata_dataset_identifier, where="test_date > '"+last_updated+"'", select="test_date, county, new_positives, cumulative_number_of_positives", limit=1000)

    row_src = []
    source = "ny cases by county.csv"
    with open(source, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
    with open(source, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            for key in headers:
                if "ls" in key:
                    row.pop(key)
            row_src.append(row)

    for row in results:
        date_obj = datetime.datetime.strptime(row['test_date'], '%Y-%m-%dT00:00:00.000')
        date_header = str(date_obj.month) + "/" + str(date_obj.day) + "/" + str(date_obj.year)
        for entry in row_src: 
            if entry['county'].lower() == row['county'].lower():
                entry[date_header] = row['cumulative_number_of_positives']
    

    target = source
    with open(target, "w", newline="") as csvfile:
        headers = list(row_src[0].keys())
        writer = csv.DictWriter(csvfile, headers)
        writer.writeheader()
        for row in row_src:
            writer.writerow(row)

# API config (Do not change)
app_token = "1CKHfUB8qIpEQKUM1JNdiEK1N"
socrata_dataset_identifier = "xdss-u53e"

client = Socrata("health.data.ny.gov", app_token)
metadata = client.get_metadata(socrata_dataset_identifier)


today = datetime.date.today() -  datetime.timedelta(days=1)
today = datetime.datetime(today.year, today.month, today.day)
with open("Last updated.txt",'r') as fp:
    last_updated = fp.read()
    last_updated_obj = datetime.datetime.strptime(last_updated, '%Y-%m-%dT00:00:00.000')

if today > last_updated_obj:
    if len(check_update()) > 0:
        update_data()
        print("Data files updated")

        with open("Last updated.txt", 'w') as fp:
            fp.write(today.strftime('%Y-%m-%dT00:00:00.000'))

