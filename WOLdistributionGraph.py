import requests
from bs4 import BeautifulSoup
import seaborn as sns
import matplotlib.pyplot as plt
#Url to scrape
baseurl = 'https://wol.gg/top/world/'

#number of pages that we want to scrape
n_pages = 1

#set theme
sns.set_theme('talk')

#Iterate through each page and perform the scrape
data = []
for i in range(1, n_pages + 1):
    # Create URL for this page
    url = baseurl + str(i) + '/'
    print(f'Current Page: {url}')

    # Request to get the page
    response = requests.get(url)

    # Parse the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the data
    rows_color2 = soup.find_all(class_='row color2')
    rows_color3 = soup.find_all(class_='row color3')
    rows = rows_color2 + rows_color3

    for row in rows:
        region = row.find('span', class_='region').text.strip()
        rank = row.find('span', class_='rank').text.strip().replace('.', '')
        name = row.find('span', class_='name').text.strip()
        days = row.find('span', class_='days').text.strip().replace('.', '').rstrip('d')
        data.append([str(region), int(rank), str(days), int(days)])

# Create graph from data
x_values = [row[1] for row in data]
y_values = [row[3] for row in data]

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Create a bar plot
ax.bar(x_values, y_values, color='orange', edgecolor='black')

# Set the title and labels
ax.set_title('Rank vs Days', fontsize=16)
ax.set_xlabel('Rank', fontsize=14)
ax.set_ylabel('Days', fontsize=14)

# Rotate x-axis labels if they overlap
plt.xticks(rotation=90)

# Show the grid
ax.grid(True)

# Show the plot
plt.show()