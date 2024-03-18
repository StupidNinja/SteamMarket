A python project that is designed to calculate the lowest price to create desired CS2 skin via trade-up contract system



Version 1.0:
  - Added manually collection data filling feature


Version 1.1:
  - Replaced manual data filling with web parser ( Succesfully collected data about 78 collection with 1162 total skins)
  - Scraping price from "../market/priceoverview/.." url request for each wear property("Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred") for skin


Version 1.2:
  - The trade-up calculator with parameters : desired_skin, desired_wear, and output : total_cost, probability, skins_used, desired_skin_price, desired_collection
  - Posibility to calculate the profit or loss values of trade-up
