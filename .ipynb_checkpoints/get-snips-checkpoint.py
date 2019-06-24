from bs4 import BeautifulSoup

# get-snip.py Description
#-------------------------------
# Intermediate script to decipher correct html parsing
# structure for desired property data.  Pulls property data
# from a single HTML file saved on a disk.
#-------------------------------

from bs4 import BeautifulSoup

# Open saved html file
html_file = open('example_html.html', 'r')

# Create soup object from html file
soup = BeautifulSoup(html_file, 'html.parser')

# Grab Prop Items
prop_item_list = soup.find_all(class_='prop_item')

# From each property item div, grab all property data from nested divs.
for prop_item in prop_item_list:
    mpi_img = prop_item.find(class_='mpi_img')
    mpi_info = prop_item.find(class_='mpi_info')
    img_url = mpi_img.a['style']
    
    # Grab list price
    list_price = (mpi_img.find(class_='block_overlay')
    .find(class_='block_price')
    .find(class_='price').text)
    
    # Grab listing status
    list_status = (mpi_img.find(class_='block_overlay')
    .find(class_='block_price')
    .find(class_='for_status').text)
    
    # Grab list url
    list_url = mpi_img.a['href']
    # Grab address
    address = mpi_info.a.text
    # Grab mls number
    mls_num = mpi_info.find(class_='mpi_mls').text
    # Grab property description
    desc = mpi_info.p.text
    for info_type in mpi_info.find(class_='mp_features').find_all(class_='mpf_item'):
        if 'Bed' in info_type.text:
            bedrooms = info_type.text
        elif 'Stories' in info_type.text:
            stories = info_type.text
        elif 'Lot' in info_type.text:
            lot_sqft = info_type.text
        elif 'Pool' in info_type.text:
            pool = info_type.text
        elif 'Bath' in info_type.text:
            bathrooms = info_type.text
        elif 'Building' in info_type.text:
            building_sqft = info_type.text
        elif 'Built' in info_type.text:
            year_built = info_type.text
        elif 'Garage' in info_type.text:
            garages = info_type.text
        else:
            # Grab 'unknown_data" to ensure we didn't miss a category
            unknown_data = info_type.text
            print(unknown_data)
    real_data = mpi_info.find_all('a')
    # Grab realtor name
    real_name = real_data[1].text
    # Grab realtor page link
    real_link = real_data[1]['href']
    # Grab realtor company link
    real_comp_name = real_data[2].text
    # Grab realtor company link
    real_comp_link = real_data[2]['href']
    print("-----------NEW LISTING----------------")
    print(img_url)
    print(list_price)
    print(list_status)
    print(list_url)
    print(address)
    print(mls_num)
    print(desc)
    print(bedrooms)
    print(stories)
    print(lot_sqft)
    print(pool)
    print(bathrooms)
    print(building_sqft)
    print(year_built)
    print(garages)
    print(real_name)
    print(real_link)
    print(real_comp_name)
    print(real_comp_link)