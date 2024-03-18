import json
import requests
import urllib3
from bs4 import BeautifulSoup

import urllib.parse


def scrape_and_save_prices(skin_name, wear):
    # Disable SSL warnings and certificate verification
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    http = urllib3.PoolManager(cert_reqs='CERT_NONE')

    # Define the base URL for the Steam market price overview API
    base_url = "http://steamcommunity.com/market/priceoverview/"

    # Define the parameters that are the same for all requests
    params = {
        'country': 'US',
        'currency': '1',
        'appid': '730',
    }

    # Add the market_hash_name and wear to the parameters
    params['market_hash_name'] = f"{skin_name} ({wear})"

    # Construct the full URL
    url = base_url + '?' + urllib.parse.urlencode(params)

    # Send the GET request
    response = http.request('GET', url)

    print(response.json())

    # Parse the response
    data = json.loads(response.data.decode('utf-8'))

    # Return the data
    return data


def get_skin_price(skin_name, wear):
    # Replace spaces with '+' for the URL
    skin_name = skin_name.replace(' ', '+')
    wear = wear.replace(' ', '+')

    # Make a request to the Steam Community Market priceoverview API
    response = requests.get(f"https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=730&market_hash_name={skin_name}+({wear})")

    # Parse the response JSON and return the lowest price
    return float(response.json()['lowest_price'].replace('$', ''))


def get_cheapest_item_id(item_name):
    # Get the listings for the item
    response = requests.get(f'https://steamcommunity.com/market/listings/730/{item_name}')
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the script tag that contains the listings
    script_tag = soup.find('script', text=lambda t: 'Market_LoadOrderSpread' in t)

    # Check if the script tag was found
    if script_tag is None:
        print(f"No listings found for {item_name}")
        return None

    # Extract the item_id of the cheapest listing from the script tag
    item_id = script_tag.text.split('Market_LoadOrderSpread(')[1].split(')')[0]

    return item_id


def trade_up_calculator(desired_skin, desired_wear):
    # Load the data from collections.json
    with open('collections.json', 'r') as f:
        collections_data = json.load(f)

    # Define a mapping from rarity names to integers
    rarity_mapping = {
        'Consumer Grade': 0,
        'Industrial Grade': 1,
        'Mil-Spec Grade': 2,
        'Restricted': 3,
        'Classified': 4,
        'Covert': 5,
        'Exceedingly Rare': 6
    }

    # Initialize the total cost
    total_cost = 0

    # Get the price of the desired skin
    desired_skin_data = scrape_and_save_prices(desired_skin, desired_wear)
    if desired_skin_data['success']:
        desired_skin_price = float(desired_skin_data['lowest_price'].strip('$'))
    else:
        desired_skin_price = 0

    # Find the collection and rarity of the desired skin
    desired_collection = None
    desired_rarity = None
    for collection_name, collection in collections_data.items():
        for rarity_name, skins in collection.items():
            if desired_skin in skins:
                desired_collection = collection_name
                desired_rarity = rarity_mapping[rarity_name]
                break
        if desired_collection is not None:
            break

    # Find the skins of one step lower rarity in the same collection
    lower_rarity_skins = collections_data[desired_collection][list(rarity_mapping.keys())[desired_rarity - 1]]

    # Get the prices of the lower rarity skins and keep track of the skins used
    lower_rarity_prices = []
    skins_used = {}
    for skin in lower_rarity_skins:
        data = scrape_and_save_prices(skin, desired_wear)
        if 'lowest_price' not in data:
            continue
        lower_rarity_prices.append((skin, float(data['lowest_price'].strip('$'))))

    # Sort the prices
    lower_rarity_prices.sort(key=lambda x: x[1])

    # Fill the contract with the cheapest skins
    skins_used = {}
    for skin, price in lower_rarity_prices:
        while total_cost + price <= desired_skin_price and len(skins_used) < 10:
            total_cost += price
            skins_used[skin] = skins_used.get(skin, 0) + 1

    # Define the skins of the same rarity as the desired skin
    same_rarity_skins = collections_data[desired_collection][list(rarity_mapping.keys())[desired_rarity]]

    # Calculate the probability of getting the desired skin
    probability = 1 / len(same_rarity_skins)

    # Return the total input cost, the probability, the skins used, and the price of the desired skin
    return total_cost, probability, skins_used, desired_skin_price, desired_collection


def test_trade_up_value():
    desired_skin = "M4A4 | Temukau"
    desired_wear = "Factory New"

    total_cost, probability, skins_used, desired_skin_price, desired_collection = trade_up_calculator(desired_skin, desired_wear)

    # Calculate the profit or loss
    profit_or_loss = desired_skin_price - total_cost

    # Determine whether it's a profit or loss
    result = 'Profit' if profit_or_loss > 0 else 'Loss'

    # Print the results to the terminal
    print(f'Total cost: ${total_cost:.2f}')
    print(f'Probability: {probability*100:.2f}%')
    print(f'Skins used in the contract:')
    for skin, count in skins_used.items():
        print(f'  {skin}: {count}')
    print(f'Collection of skins used: {desired_collection}')
    print(f'Price of desired skin: ${desired_skin_price:.2f}')
    print(f'{result}: ${abs(profit_or_loss):.2f}')


item_id = get_cheapest_item_id('AWP | Duality (Factory New)')
print(item_id)
