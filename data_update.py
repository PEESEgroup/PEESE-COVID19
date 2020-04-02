import requests
from bs4 import BeautifulSoup
import time
import csv
import datetime
import math
import os
import pip

# pip install C:\Users\shreyaaa\Downloads\lxml-4.5.0-cp38-cp38-win32 (3).whl
# Scrape date
def get_page():
    url = "https://coronavirus.health.ny.gov/county-county-breakdown-positive-cases"
    page = requests.get(url).text
    return page

count = 0
page = get_page()
time.sleep(5)

# send requests until success (20 requests max)
# while(page.status_code!=200 and count<=20):
#     page = get_page()
#     time.sleep(10)
#     count += 0

soup = BeautifulSoup(page, 'lxml')

rd = soup.findAll('div', attrs={'class':'wysiwyg--field-webny-wysiwyg-title'})
tb = soup.find('table')


recent_date = rd[0].get_text()
date_obj = datetime.datetime.strptime(recent_date, 'Last update: %B %d, %Y | %I:%M%p')
date_header = str(date_obj.month) + "/" + str(date_obj.day) + "/" + str(date_obj.year)

fp = open("Last updated.txt", "r")
recent_updated_date = fp.readlines()[0]
fp.close()

def update_data():

    data = []
    td = tb.find_all('td')
    for i in range(len(td)//2):
        #print(td[2*i].get_text())
        data.append([td[2*i].get_text(), int(td[2*i+1].get_text().replace(",",""))])

    data.pop(-1)

    row_src = [["county", date_header]]
    row_src.extend(data)


    # Write data
    target = "ny cases by county - ls.csv"
    target2 = "ny cases by county.csv"

    row_tgt = []
    with open(target, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            row_tgt.append(row)


    row_tgt2 = []
    with open(target2, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            row_tgt2.append(row)


    headt = row_tgt.pop(0)
    heads = row_src.pop(0)
    for e in heads[1:]:
        headt.extend([e, e+"/ls"])

    headt2 = row_tgt2.pop(0)
    for e in heads[1:]:
        headt2.extend([e])


    # adjust 0 values
    err = 1E-2

    for rt in row_tgt:
        is_present = False
        for rs in row_src:
            if rt[1].lower() == rs[0].lower():
                for e in rs[1:]:
                    try:
                        rt.extend([e, math.log10(int(e)+err)])
                    except ValueError:
                        rt.extend([0, math.log10(0+err)])
                is_present = True
                break
        if not is_present:
            rt.extend([0, math.log10(0+err)] * len(rs[1:]))

    for rt in row_tgt2:
        is_present = False
        for rs in row_src:
            if rt[0].lower() == rs[0].lower() or rt[0].lower() + " city" == rs[0].lower():
                for e in rs[1:]:
                    rt.extend([e])
                is_present = True
                break
        if not is_present:
            rt.extend([0] * len(rs[1:]))

    data = [headt]
    data.extend(row_tgt)

    data2 = [headt2]
    data2.extend(row_tgt2)

    with open("test.csv", 'w', newline="") as wfile:
        writer = csv.writer(wfile)
        for r in data:
            writer.writerow(r)

    with open("test2.csv", 'w', newline="") as wfile:
        writer = csv.writer(wfile)
        for r in data2:
            writer.writerow(r)

    os.remove("ny cases by county - ls.csv")
    os.rename("test.csv", "ny cases by county - ls.csv")

    os.remove("ny cases by county.csv")
    os.rename("test2.csv", "ny cases by county.csv")

# update only if not previously updated
if recent_updated_date != recent_date:
    update_data()
    fp = open("Last updated.txt", "w+")
    fp.write(recent_date)
    fp.close()


