#This script is going to comb the lolalytics site to find champion winrate and playrate data for the current patch. Then generate a graph of the data with x as the pickrate and y as the win delta

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv

#Site Url
url = 'https://lolalytics.com/lol/tierlist/'

#request the site
response = requests.get(url)

#parse the page
soup = BeautifulSoup(response.text, 'html.parser')

#get the data
rows = soup.find_all('div', class_='flex h-[52px] justify-between text-[13px] text-[#ccc] odd:bg-[#181818] even:bg-[#101010]')

data = []
for row in rows:
    Rank = row.find(attrs={"q:key": "0"}).text
    Icon = row.find(attrs={"q:key": "0"}).text
    Name = row.find(attrs={"q:key": "SO_0"}).text
    Tier = row.find(attrs={"q:key": "3"}).text
    Lane_pos = row.find(attrs={"q:key": "kS_0"}).get('alt')
    Lane_percent = row.find(attrs={"q:key": "kS_0"}).text
    Win = row.find(attrs={"q:key": "Ts_0"}).text
    Pick = row.find(attrs={"q:key": "6"}).text
    Ban = row.find(attrs={"q:key": "7"}).text
    Pbi = row.find(attrs={"q:key": "8"}).text
    Games = row.find(attrs={"q:key": "9"}).text.strip().replace(',', '')
    data.append([int(Rank), str(Name), str(Tier), str(Lane_pos), str(Lane_percent), float(Win), float(Pick), float(Ban), int(Pbi), int(Games)])


with open('Lolalytics_Scraped_Data', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Name", "Tier", "Lane Position", "Lane Percentage", "Win", "Pick", "Ban", "Pbi", "Games"])
    writer.writerows(data)







 