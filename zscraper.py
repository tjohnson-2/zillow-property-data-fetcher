import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import csv

def get_zillow_data(zillow_link):
    # simulating browser
    user_agent = UserAgent()
    headers = {'User-Agent': user_agent.random}

    # making a request to the website
    response = requests.get(zillow_link, headers=headers)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # extracting address
        summary_container = soup.find('div', {'class': 'summary-container'})
        h1_element = summary_container.find('h1')
        address = h1_element.text.strip() if h1_element else "N/A"

        # extracting price
        price_element = soup.find('span', {'data-testid': 'price'})
        if price_element:
            # Extract only numeric values and remove commas
            price = re.sub(r'[^0-9]', '', price_element.text)
        else:
            price = "N/A"

        # extracting beds, baths, and square footage
        bed_bath_beyond_element = soup.find('span', {'data-testid': 'bed-bath-beyond'})
        if bed_bath_beyond_element:
            # Flattening square footage and returning as a list, allowing for decimal points
            bed_bath_beyond_values = [re.sub(r'[^0-9\.]', '', strong.text.strip()) for strong in bed_bath_beyond_element.find_all('strong')]
        else:
            bed_bath_beyond_values = []

        # combining data for CSV
        data_for_csv = [address, price] + bed_bath_beyond_values
        combined_output = ('Address: ' + address + '\nPrice: ' + price + '\nBeds: ' + (bed_bath_beyond_values[0]) +
                           '\nBaths: ' + (bed_bath_beyond_values[1]) + '\nSize: ' + (bed_bath_beyond_values[2]))
        print(combined_output)

        # write data to CSV
        csv_file_name = f'property_data_{address}.csv'
        with open(csv_file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Address', 'Price', 'Beds', 'Baths', 'Size'])
            csv_writer.writerow(data_for_csv)

    else:
        print("Failed to fetch the page. Status code:", response.status_code)

userSuppliedLink = input()
get_zillow_data(userSuppliedLink)
