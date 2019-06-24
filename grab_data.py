import requests
from bs4 import BeautifulSoup
import glob
import pathlib
import pandas as pd
import datetime

# grab_data.py Description
#----------------------------------
# Loop through all HTML files in HTML_FILES directory. Save each property's data from the HTML file to
# prop_data_dict (dictonary)  Append the dictonaries to prop_data_list (list of dictionaries).  Create a 
# pandas dataframe from the list of dictionaries.  Save the dataframe to a csv file titles for the day/time
# created.
#----------------------------------

# Initialize list and dictionary to hold property data results
prop_data_list = []
prop_data_dict = {}

# Create Path to HTML Files
html_dir = pathlib.Path.cwd()
html_dir = html_dir / 'HTML_FILES'

# Loop through all HTML files in HTML_FILES folder
for filename in html_dir.iterdir():
    # Open HTML File
    html_file = open(html_dir / filename.name, 'r')
    print('Scraping: ' + filename.name) # Print current scraped file to console
    
    # Create soup object from html file
    soup = BeautifulSoup(html_file, 'html.parser')

    # Grab Prop Items div from html file
    prop_item_list = soup.find_all(class_='prop_item')

    # From each property item div, grab all property data from nested divs.
    for prop_item in prop_item_list:
        mpi_img = prop_item.find(class_='mpi_img')
        mpi_info = prop_item.find(class_='mpi_info')
        prop_data_dict['img_url'] = mpi_img.a['style']
        prop_data_dict['list_price'] = mpi_img.find(class_='block_overlay').find(class_='block_price').find(class_='price').text
        prop_data_dict['list_status'] = mpi_img.find(class_='block_overlay').find(class_='block_price').find(class_='for_status').text
        prop_data_dict['list_url'] = mpi_img.a['href']
        prop_data_dict['address'] = mpi_info.a.text
        prop_data_dict['mls_num'] = mpi_info.find(class_='mpi_mls').text
        prop_data_dict['desc'] = mpi_info.p.text
        # Parse all mpf_item divs for specific strings to assign each datapoint to the appropriate column
        for info_type in mpi_info.find(class_='mp_features').find_all(class_='mpf_item'):
            if 'Bed' in info_type.text:
                prop_data_dict['bedrooms'] = info_type.text
            elif 'Stories' in info_type.text:
                prop_data_dict['stories'] = info_type.text
            elif 'Lot' in info_type.text:
                prop_data_dict['lot_sqft'] = info_type.text
            elif 'Pool' in info_type.text:
                prop_data_dict['pool'] = info_type.text
            elif 'Bath' in info_type.text:
                prop_data_dict['bathrooms'] = info_type.text
            elif 'Building' in info_type.text:
                prop_data_dict['building_sqft'] = info_type.text
            elif 'Built' in info_type.text:
                prop_data_dict['year_built'] = info_type.text
            elif 'Garage' in info_type.text:
                prop_data_dict['garages'] = info_type.text
            else:
                # Using an unkown_data column to visualize any missed data categories from a particular listing
                prop_data_dict['unknown_data'] = info_type.text
                print("--------UNKNOWN DATA-------")
                print(prop_data_dict['unknown_data'])
        real_data = mpi_info.find_all('a')
        prop_data_dict['real_name'] = real_data[1].text
        prop_data_dict['real_link'] = real_data[1]['href']
        prop_data_dict['real_comp_name'] = real_data[2].text
        prop_data_dict['real_comp_link'] = real_data[2]['href']

        # Append individual property dictionary to list of dictionaries
        prop_data_list.append(prop_data_dict)
        # Clear individual property dictionary for next property
        prop_data_dict = {} 
        # Close HTML file
        html_file.close()

# Grab current DT for filename
currentDT = datetime.datetime.now()
# Create pandas dataframe
df = pd.DataFrame(prop_data_list)
# Save dataframe to csv with date/time as filename
df.to_csv(str(currentDT) + '_csv.csv')