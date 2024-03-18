# CS:GO Trade-Up Contract Calculator

**This Python script calculates the potential profit or loss from a trade-up contract in the game Counter-Strike: Global Offensive (CS:GO). It uses the Steam Community Market API to fetch the current market prices of CS:GO skins.**


## Functions
### * 'scrape_and_save_prices(skin_name, wear)': Fetches the current market price of a specific CS:GO skin with a specific wear level.
### * 'get_skin_price(skin_name, wear)': Fetches the lowest market price of a specific CS:GO skin with a specific wear level.
### * 'get_cheapest_item_id(item_name)': Fetches the item ID of the cheapest listing for a specific item on the Steam Community Market.
### * 'trade_up_calculator(desired_skin, desired_wear)': Calculates the potential profit or loss from a trade-up contract for a specific CS:GO skin with a specific wear level.
### * 'test_trade_up_value()': Tests the trade_up_calculator() function with a specific skin and wear level.
### * 'main()': The main function of the script. It prompts the user to choose a skin and a wear level, calculates the trade-up value, and prints the results to the terminal.

## Usage

### The script is executed from the command line and interacts with the user through the terminal. It requires the 'json', 'requests', 'urllib3', and 'BeautifulSoup' libraries.

'python main.py'

## Dependencies

### * json
### * requests
### * urllib3
### * BeautifulSoup


Version 1.0:
  - Added manually collection data filling feature


Version 1.1:
  - Replaced manual data filling with web parser ( Succesfully collected data about 78 collection with 1162 total skins)
  - Scraping price from "../market/priceoverview/.." url request for each wear property("Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred") for skin


Version 1.2:
  - The trade-up calculator with parameters : desired_skin, desired_wear, and output : total_cost, probability, skins_used, desired_skin_price, desired_collection
  - Posibility to calculate the profit or loss values of trade-up
