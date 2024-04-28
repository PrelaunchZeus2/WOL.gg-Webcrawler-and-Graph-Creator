import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import concurrent.futures
import seaborn as sns

sns.set_theme(context = 'talk', style='whitegrid')

#Url to scrape
baseurl = 'https://wol.gg/top/world/'

#Number of pages that we want to scrape
n_pages = 200

#Function to scrape a single page
def scrape_page(i):
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
        rank = row.find('span', class_='rank').text.strip().replace('.', '')
        days = row.find('span', class_='days').text.strip().replace('.', '').rstrip('d')
        page_data.append([int(rank), int(days)])

    return page_data

#MULTI THREADING!!!!! BRRRRR
with concurrent.futures.ThreadPoolExecutor() as executor:
    #Use list comprehension to create a list of futures
    futures = [executor.submit(scrape_page, i) for i in range(1, n_pages + 1)]

    #Use as_completed to get the results as they become available
    data = []
    for future in concurrent.futures.as_completed(futures):
        data.extend(future.result())


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