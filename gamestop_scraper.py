import requests
from main import Game

# Create a session to reuse the underlying TCP connection
session = requests.Session()


def gamestop_scrape_backend(url, sku):
    # Construct the URL for the first request
    unique_url = url + str(sku)
    # 1st request for obtaining everything except UPC
    response = session.get(unique_url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})

    if response.status_code == 200:
        try:
            # Extract product data from the JSON response
            product_data = response.json().get("product")

            if product_data:
                # Extract product information
                product_sku = product_data.get("id")
                product_title = product_data.get("name")
                all_product_prices = product_data.get("price", {})
                product_base_price = all_product_prices.get("base")
                is_digital_product = product_data.get("availability", {}).get("isDigitalProduct")
                image_url = product_data.get("image", {}).get("base")
                product_url = product_data.get('url')

                # Extract product category from the URL
                product_category = product_url.split('/')[1]

                # Check if the product is a video game with a base price
                if product_base_price is None and product_category != 'video-games':
                    return None

                # Parse the product ID from the image URL
                start_url = image_url.find("https://media.gamestop.com/i/gamestop/") + len(
                    "https://media.gamestop.com/i/gamestop/")
                end_url = image_url.find("/", start_url)
                # Extract the number from the string
                product_id = image_url[start_url:end_url]

                # 2nd request for obtaining UPC, using the parsed product ID
                upc_response = session.get(
                    f"https://api.bazaarvoice.com/data/products.json?passkey=ca0SPanXcxTi6Os49LTaXK2PuXoCok57Y7dzJY0FfuxDs&locale=en_US&allowMissing=true&apiVersion=5.4&filter=id:{product_id}")

                if upc_response.status_code == 200:
                    try:
                        # Extract UPC from the second response
                        product_upc = upc_response.json()['Results'][0].get('UPCs', [None])[0]
                        if product_upc is None:
                            raise IndexError("UPC does not exist")

                        # Determine product condition based on digital status and pricing
                        if is_digital_product:
                            product_condition = "Digital"
                        else:
                            product_condition = "Pre-Owned" if all_product_prices.get("pro") else "New"

                        # Create a Game object and store product data
                        new_game = Game(product_upc, int(product_sku), product_id, product_title, product_base_price,
                                        product_condition, product_category)
                        return new_game

                    except IndexError as e:
                        # Handle UPC extraction errors
                        print(e)
                        return None
                else:
                    return None
            else:
                print("Invalid API response format.")
        except requests.exceptions.JSONDecodeError as e:
            # Handle JSON parsing errors
            print(f"Failed to parse JSON response. Error: {e}")
            return None

    else:
        # Handle non-200 response status
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None



def loop_gamestop_scrape(url, connection, min_sku, max_sku):
    from setup_db import insert_data
    # Loop through SKUs and scrape data
    for i in range(min_sku, max_sku + 1):
        scrapped_data = gamestop_scrape_backend(url, i)
        print(scrapped_data)

        if scrapped_data:
            try:
                # Insert scraped data into the database
                insert_data(connection, scrapped_data)
                print(f"Sku:{scrapped_data.sku} added")
            except IndexError as e:
                # Handle database insertion errors
                print(e)
        else:
            # Print a message for SKUs with no data
            print("SKU: ",i , "No Data")
            continue




