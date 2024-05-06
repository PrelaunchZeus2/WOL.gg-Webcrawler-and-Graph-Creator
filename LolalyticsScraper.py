#This script is going to comb the lolalytics site to find champion winrate and playrate data for the current patch. Then generate a graph of the data with x as the pickrate and y as the win delta

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import threading

#Site Url
url = 'https://lolalytics.com/lol/tierlist/'

#request the site
response = requests.get(url)

#parse the page
soup = BeautifulSoup(response.text, 'html.parser')

#get the data
rows = soup.find_all('div', class_ = 'flex h-[52px]  justify-between text-[13px] text-[#ccc] odd:bg-[#181818] even:bg-[#101010]')

data = []
for row in rows:
    Rank = row.find('[q = "0"]')
    Icon = row.find('[q = "1"]')
    Name = row.find('[q = "SO_0"]')
    Tier = row.find('[q = "3"]')
    Lane_pos = None  # There are two elements in lane, consider looking at alt text of image for lane and new data for lane percentage which is an int
    Lane_percent = None
    Win = row.find('[q = "Ts_0"]')
    Pick = row.find('[q = "6"]')
    Ban = row.find('[q = 7]')
    Pbi = row.find('[q = 8]')
    Games = row.find('[q = 9]')
    data.append([int(Rank), str(Icon), str(Name), int(Tier), Lane_pos, Lane_percent, float(Win), float(Pick), float(Ban), int(Pbi), int(Games)])

    print(data)







 