import json
import requests
from time import sleep
from bs4 import BeautifulSoup
import urllib.parse


def scrape_and_save_prices():
    # Disable SSL warnings and certificate verification
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    http = requests.Session()

    # Load the data from skins_data.json
    with open('collections.json', 'r') as f:
        skins_data = json.load(f)

    # Define the base URL for the Steam market price overview API
    base_url = "http://steamcommunity.com/market/priceoverview/"

    # Define the parameters that are the same for all requests
    params = {
        'country': 'US',
        'currency': '1',
        'appid': '730',
    }

    # Define the wear options
    wear_options = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]

    # Define the request limit
    request_limit = 900

    # Initialize the request counter
    request_count = 0

    # Initialize the prices data
    prices_data = {}

    # Generate all combinations of collection, grade, skin, and wear
    combinations = ((collection_name, grade_name, skin_name, wear)
                    for collection_name, collection in skins_data.items()
                    for grade_name, skins in collection.items()
                    for skin_name in skins
                    for wear in wear_options)

    # Iterate over each combination
    for collection_name, grade_name, skin_name, wear in combinations:
        # Check if the request limit has been reached
        if request_count >= request_limit:
            break

        # Add the market_hash_name and wear to the parameters
        params['market_hash_name'] = f"{skin_name} ({wear})"

        # Construct the full URL
        url = base_url + '?' + urllib.parse.urlencode(params)

        # Send the GET request
        response = http.get(url)

        # Parse the response
        data = response.json()

        # Check if the request was successful
        if data['success']:
            # Add the lowest price to the skin's data
            prices_data.setdefault(collection_name, {}).setdefault(grade_name, {})[skin_name] = {
                f'lowest_price_{wear.replace(" ", "_").lower()}': data['lowest_price']
            }
        else:
            print(f"Request for {skin_name} ({wear}) failed.")

        # Increment the request counter
        request_count += 1

        # Sleep for a short time to avoid rate limiting
        sleep(0.1)

    # Write the prices data to skins_prices.json
    with open('skins_prices.json', 'w') as f:
        json.dump(prices_data, f, indent=4)


def scrape_cs_money():
    base_url = "https://wiki.cs.money"
    collections_url = base_url + "/collections"
    response = requests.get(collections_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    collections = {}

    # Find all collection blocks
    for collection_div in soup.find_all('div', class_='szvsuisjrrqalciyqqzoxoaubw'):
        collection_name = collection_div.text.strip()
        print(f"Found collection: {collection_name}")

        collection_link_element = collection_div.find_parent('a', class_='blzuifkxmlnzwzwpwjzrrtwcse')
        if collection_link_element is not None:
            collection_link = collection_link_element['href']
            collection_page_url = base_url + collection_link
            print(f"Going to collection page: {collection_page_url}")
        else:
            print(f"Could not find link for collection: {collection_name}")
            continue

        # Go to the collection's page and parse it
        collection_response = requests.get(collection_page_url)
        collection_soup = BeautifulSoup(collection_response.text, 'html.parser')

        collections[collection_name] = {}

        # Find all skin blocks within this collection
        for skin_div in collection_soup.find_all('div', class_='kxmatkcipwonxvwweiqqdoumxg'):
            weapon_name = skin_div.find('div', class_='szvsuisjrrqalciyqqzoxoaubw').text.strip()
            skin_name = skin_div.find('div', class_='zhqwubnajobxbgkzlnptmjmgwn').text.strip()

            divs = skin_div.find_all('div', class_='nwdmbwsohrhpxvdldicoixwfed')
            if len(divs) >= 2:
                skin_rarity = divs[1]['title'].strip()
                print(f"Found skin: {weapon_name} | {skin_name} ({skin_rarity})")
            else:
                print(f"Could not find rarity for skin: {weapon_name} | {skin_name}")
                continue

            # Add this skin to the collection
            collections.setdefault(collection_name, {}).setdefault(skin_rarity, []).append(f"{weapon_name} | {skin_name}")

    return collections


def count_collections_and_skins(json_file):
    # Load the collections data from the JSON file
    with open(json_file, 'r') as f:
        collections = json.load(f)

    # Count the number of collections and skins
    num_collections = len(collections)
    num_skins = sum(len(skins) for rarities in collections.values() for skins in rarities.values())

    return num_collections, num_skins


scrape_and_save_prices()
# Use the function
# num_collections, num_skins = count_collections_and_skins('collections.json')
# print(f"Number of collections: {num_collections}")
# print(f"Number of skins: {num_skins}")

# collections = scrape_cs_money()

# # Save the collections data into a JSON file with pretty-printing
# with open('collections.json', 'w') as f:
#     json.dump(collections, f, indent=4)

# print("Saved collections data into collections.json")
