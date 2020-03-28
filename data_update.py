import requests
from bs4 import BeautifulSoup
import time

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
tb = soup.find('table')

row_src = []
td = tb.find_all('td')
for i in range(len(td)//2):
    #print(td[2*i].get_text())
    row_src.append([td[2*i].get_text(), int(td[2*i+1].get_text().replace(",",""))])

