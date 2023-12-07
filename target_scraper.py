import requests
import json

ZIPCODE = 50323
TARGET_STOREID = 1791

def target_scrape_backend(upc):
    # Define the base URL for Target scraping
    unique_url = 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2'
    # Make a GET request to the Target API
    response = requests.get(unique_url, params={"key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
                                                  "channel": "WEB",
                                                  "keyword": int(upc),
                                                  "page": f"%2Fs%2F{upc}",
                                                  "pricing_store_id": TARGET_STOREID,
                                                  "visitor_id": "018C280EC5700201BBCC4FFEFCFEF5ED",
                                                  "zip": 50323},
                            headers={
                                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Try to extract price information from the JSON response
        try:
            # Decode JSON data from the response content
            json_data = json.loads(response.content.decode())
            # Extract the regular retail price from the JSON data
            price = json_data["data"]["search"]["products"][0]["price"]['reg_retail']
            return price
        except IndexError:
            # Handle the case where the UPC doesn't exist
            print("UPC Doesn't Exist")
    else:
        # Print the status code for unsuccessful requests
        print(response.status_code)
        return None







