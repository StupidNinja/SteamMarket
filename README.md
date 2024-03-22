# CS:GO Trade-Up Contract Calculator

This Python script calculates the potential profit or loss from a trade-up contract in the game Counter-Strike: Global Offensive (CS:GO). It uses the Steam Community Market API to fetch the current market prices of CS:GO skins.

## Functions

- `scrape_and_save_prices(skin_name, wear)`: Fetches the current market price of a specific CS:GO skin with a specific wear level.
- `get_skin_price(skin_name, wear)`: Fetches the lowest market price of a specific CS:GO skin with a specific wear level.
- `trade_up_calculator(desired_skin, desired_wear)`: Calculates the potential profit or loss from a trade-up contract for a specific CS:GO skin with a specific wear level.

## Usage

This script is designed to be run from the command line. Here's a step-by-step guide on how to use it:

1. **Install Dependencies**: Before running the script, make sure you have the required libraries installed. You can install them using pip:

    ```bash
    pip install json requests urllib3 beautifulsoup4
    ```

2. **Run the Script**: Navigate to the directory containing the script and run it using Python:

    ```bash
    python main.py
    ```

3. **Choose a Skin and Wear Level**: The script will prompt you to choose a CS:GO skin and a wear level. Enter your choices when prompted.

4. **View the Results**: The script will calculate the trade-up value and print the results to the terminal. The results include the total cost, probability, skins used, desired skin price, and desired collection.

5. **Test the Trade-Up Value**: You can test the `trade_up_calculator()` function with a specific skin and wear level by calling the `test_trade_up_value()` function.

6. **Use the CLI**: From version 1.3 onwards, you can use the command line interface (CLI) to interact with the script. This allows you to pass parameters directly from the command line, making the script more flexible and easier to use in different contexts.

Remember to replace `main.py` with the actual name of your script if it's different.
## Dependencies

 - `json`
 - `requests`
 - `urllib3`
 - `BeautifulSoup`

## Versions
Version 1.0:
  - Added manually collection data filling feature


Version 1.1:
  - Replaced manual data filling with web parser ( Succesfully collected data about 78 collection with 1162 total skins)
  - Scraping price from "../market/priceoverview/.." url request for each wear property("Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred") for skin


Version 1.2:
  - The trade-up calculator with parameters : desired_skin, desired_wear, and output : total_cost, probability, skins_used, desired_skin_price, desired_collection
  - Posibility to calculate the profit or loss values of trade-up

Version 1.3:
 - Added CLI


 
