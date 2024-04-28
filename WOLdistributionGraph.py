import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import concurrent.futures
import seaborn as sns
import threading
import csv

sns.set_theme(context = 'notebook', style='white', font_scale=1.5)
sns.color_palette("tab10")

#thread lock
print_lock = threading.Lock() #lock to print which page is being processed

#Url to scrape
baseurl = 'https://wol.gg/top/world/'

#Number of pages that we want to scrape
n_pages = 50

#Function to scrape a single page
def scrape_page(i):
    with print_lock:
        print(f'Processing page {i}')
    # Create URL for this page
    url = baseurl + str(i) + '/'

    #Request to get the page
    response = requests.get(url)

    #Parse the page
    soup = BeautifulSoup(response.text, 'html.parser')

    #Get the data
    rows_color2 = soup.find_all(class_='row color2')
    rows_color3 = soup.find_all(class_='row color3')
    rows = rows_color2 + rows_color3

    page_data = []
    for row in rows:
        region = row.find('span', class_='region')
        rank = row.find('span', class_='rank').text.strip().replace('.', '')
        name = row.find('span', class_='name').text.strip()
        days = row.find('span', class_='days').text.strip().replace('.', '').rstrip('d')
        page_data.append([str(region), int(rank), str(name), int(days)])

    #write data to csv file
    with open('WOL_Top_Player_Data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(page_data)

    return page_data

#MULTI-THREADING!!!!! BRRRRR
with concurrent.futures.ThreadPoolExecutor() as executor:
    #Use list comprehension to create a list of futures
    futures = [executor.submit(scrape_page, i) for i in range(1, n_pages + 1)]

    #Use as_completed to get the results as they become available
    data = []
    for future in concurrent.futures.as_completed(futures):
        data.extend(future.result())
#I dont really know how to use multi threading but according to stack overflow and other *cough cough ai assisted* research this should work, I should probably learn about it more

#Create graph from data
x_values = [row[1] for row in data]
y_values = [row[3] for row in data]

# Create a figure and a set of subplots
fig, ax = plt.subplots()

#Create a bar plot
ax.bar(x_values, y_values, color='orange', edgecolor='black')

#Set the title and labels
ax.set_title('Rank vs Days', fontsize=16)
ax.set_xlabel('Rank', fontsize=14)
ax.set_ylabel('Days', fontsize=14)
plt.xticks(rotation=90)
ax.grid(True)


plt.show()