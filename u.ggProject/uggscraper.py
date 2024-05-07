#This script is going to comb the lolalytics site to find champion winrate and playrate data for the current patch. Then generate a graph of the data with x as the pickrate and y as the win delta
#The data will be saved in a csv file called Lolalytics_Scraped_Data.csv

#imports
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import csv
import requests

#Site Url
url = 'https://u.gg/lol/tier-list'


#Get the page
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


#get the data
rows = soup.find_all('div', class_='rt-tr-group')

data = []
for row in rows:
    Rank = row.find('div', class_='rt-td rank is-in-odd-row').text
    Role = row.find('div', class_='rt-td rank is-in-odd-row').text
    Champion = row.find('div', class_='rt-td rank is-in-odd-row').text
    Tier = row.find('div', class_='rt-td rank is-in-odd-row').text

        


with open('Lolalytics_Scraped_Data.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Rank", "Name", "Tier", "Lane Position", "Lane Percentage", "Win", "Pick", "Ban", "Pbi", "Games"])
    writer.writerows(data)










 