from urllib.parse import urlencode, quote
import json
import requests
import urllib3

def create_skin_data_json():
  """
  Creates or updates a JSON file for CS:GO skin data with user input.
  """

  # Try to load existing data from JSON file (or create empty dict if not found)
  try:
    with open("skins_data.json", "r") as f:
      skin_data = json.load(f)
  except FileNotFoundError:
    skin_data = {}

  while True:
    collection_name = input("Enter collection name (or 'q' to quit): ")
    if collection_name.lower() == 'q':
      break

    # Check if collection already exists
    if collection_name not in skin_data:
      skin_data[collection_name] = {}  # Create new collection if not found

    collection_data = skin_data[collection_name]  # Access or create collection data

    while True:
      rarity = input("Enter rarity (or 'q' to quit collection): ")
      if rarity.lower() == 'q':
        break

      # Check if rarity already exists for this collection
      if rarity not in collection_data:
        collection_data[rarity] = []  # Create new rarity list if not found

      skins = collection_data[rarity]  # Access or create list of skins

      while True:
        skin_name = input("Enter skin name (or 'q' to quit rarity): ")
        if skin_name.lower() == 'q':
          break
        skins.append(skin_name)

  # Write updated skin data to JSON file
  with open("skins_data.json", "w") as f:
    json.dump(skin_data, f, indent=4)  # Use indent for readability

  print("Skin data saved to skins_data.json")
def get_currency(currencies):
    key_value_pairs = [f"{key}: {value}" for key,value in currencies.items()]
    output_text = ", ".join(key_value_pairs)
    currency_id = int(input("Enter currency id:\n"+output_text+"\n"))
    return currency_id
def req_get(url):
    urllib3.disable_warnings()
    http = urllib3.PoolManager()
    req = http.request('GET', url)
    return req.data.decode("utf-8")
# def test():
#     # Define the base URL and query parameters
#     base_url = "https://steamcommunity.com/market/priceoverview/"
#     params = {
#         "country": "US",  # Replace with your desired country code
#         "currency": 1,  # Replace with your desired currency code (e.g., 1 for USD)
#         "appid": 570,  # Replace with the app ID of the game
#         "market_hash_name": "AK-47%20%7C%20Redline%20%28Field-Tested%29",
#         # Replace with the market hash name of the item
#     }
#
#     # Create a urllib3 PoolManager object
#     http = urllib3.PoolManager()
#
#     # Encode the query parameters
#     # encoded_params =
#
#     # Build the complete URL
#     url = f"{base_url}?{encoded_params}"
#
#     # Send the GET request and get the response
#     response = http.request('GET', url)
#
#     # Check for successful response
#     if response.status == 200:
#         # Process the response data (usually JSON)
#         data = response.json()
#         print(data)
#     else:
#         print(f"Error: {response.status} - {response.reason}")
def get_and_combine_skin_data(skin_data_file, api_url, output_file, country="US", currency="1", appid=730):
  """
  Gets prices for skins in a JSON file, combines with existing data, and saves to a new file after each successful response.

  Args:
      skin_data_file (str): Path to the JSON file containing skin data.
      api_url (str): URL of the Steam market price overview API.
      output_file (str): Path to the output JSON file.
      country (str, optional): Country code for price information (defaults to "US").
      currency (str, optional): Currency ID for price information (defaults to "1").
      appid (int, optional): App ID of the game (defaults to 730 for CS:GO).
  """

  # Load existing skin data from JSON file (consider loading only necessary data for efficiency)
  with open(skin_data_file, "r") as f:
    skins_data = json.load(f)

  # Data to store combined information (consider using a dictionary for better structure)
  combined_data = {}

  # Define skin wear options with the desired format
  wear_options = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]

  http = urllib3.PoolManager()  # Create a connection pool manager

  for collection_name, collection_data in skins_data.items():
    for rarity, skins in collection_data.items():
      for skin_name in skins:
        # Combine skin name with wear options (use the modified list)
        for wear in wear_options:
          encoded_name = quote(f"{skin_name} ({wear})")  # Encode the entire string

          # Create a dictionary of parameters with the correct order
          params = {
              "country": country,
              "currency": currency,
              "appid": appid,
              "market_hash_name": encoded_name  # Already URL-encoded using quote
          }

          # Encode only the remaining parameters (if any)
          other_params = {k: v for k, v in params.items() if k != "market_hash_name"}
          encoded_params = urlencode(other_params)

          # Construct the URL using the encoded market_hash_name and potentially other parameters
          url = f"{api_url}?{encoded_params}&market_hash_name={encoded_name}" if encoded_params else f"error"

          print(f"Sending request to URL: {url}")  # Print the constructed URL

          # Send the GET request using urllib3
          response = http.request('GET', url)

          # Check for successful response status code
          if response.status == 200:
            data = response.json()
          else:
            print(f"Error: API request failed with status code {response.status}")
            data = {}  # Empty data to avoid errors in following steps

          print(f"API Response for skin '{skin_name} ({wear})':")
          print(json.dumps(data, indent=4))

          # Extract and store price data for the current skin
          if data["success"] and "prices" in data:
            price_info = data["prices"][0]
            median_price = price_info.get("median_price", None)
            lowest_price = price_info.get("lowest_price", None)  # Ensure lowest price is captured

            # Prepare price data for saving
            price_data = {
                "name": skin_name,
                "wear": wear,  # Add wear information
                "prices": {
                    "lowest_price": lowest_price,
                    "volume": price_info.get("volume", None),
                    "median_price": median_price
                }
            }

            # Append price data to combined data (consider a more structured approach)
            combined_data[f"{skin_name} ({wear})"] = price_data

            # Save the combined data to the JSON file after each successful response
            with open(output_file, "w") as f:
              json.dump(combined_data, f, indent=4)  # Use indent for readability

  print(f"Finished processing all skins. Combined data saved to {output_file}")

def main():
    # game_id = 730
    # currencies = {"usd": 1, "gbp": 2, "eur": 3, "chf": 4, "rub": 5, "pln": 6, "brl": 7, "jpy": 8, "nok": 9, "idr": 10}
    # get_currency(currencies)
    create_skin_data_json()
    # Replace with the paths to your files and API URL
    # skin_data_file = "skins_data.json"
    # api_url = "https://steamcommunity.com/market/priceoverview/"
    # output_file = "skins_data_with_prices.json"
    #
    # # Call the function to retrieve prices and create the combined data file
    # get_and_combine_skin_data(skin_data_file, api_url, output_file)


if __name__ == "__main__":
    main()