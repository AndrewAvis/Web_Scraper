
import tkinter as tk
from tkinter import ttk
from setup_db import get_record_upc, get_record_sku
from target_scraper import target_scrape_backend

class UserInterface:
    def __init__(self, master):
        # Initialize the UserInterface object with the main window
        self.master = master
        self.master.title("Main Menu")
        self.main_menu()

    def main_menu(self):
        # Create the main menu with a "Start" button
        start_button = tk.Button(self.master, text="Start", command=self.open_game_window)
        start_button.grid(row=4, column=0, columnspan=2, pady=20)


    def open_game_window(self):
        # Open a new window for displaying game information
        game_window = tk.Toplevel(self.master)
        game_window.title("Game Information")

        # Labels for displaying GameStop and Target prices, SKU, and UPC
        self.gamestop_price_label = ttk.Label(game_window, text="GameStop Price:", font=("Arial", 12, 'bold'))
        self.gamestop_price_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.target_price_label = ttk.Label(game_window, text="Target Price:", font=("Arial", 12, 'bold'))
        self.target_price_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Define SKU and UPC labels
        sku_label = ttk.Label(game_window, text="SKU:")
        sku_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        upc_label = ttk.Label(game_window, text="UPC:")
        upc_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Entry widgets for user input of SKU and UPC
        sku_entry = ttk.Entry(game_window)
        sku_entry.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        upc_entry = ttk.Entry(game_window)
        upc_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Button to retrieve data based on SKU and UPC
        retrieve_button = tk.Button(game_window, text="Retrieve",
                                    command=lambda: self.retrieve_data(sku_entry.get(), upc_entry.get()))
        retrieve_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Create a frame to display retrieved data
        data_frame = ttk.Frame(game_window)
        data_frame.grid(row=5, column=0, columnspan=2, pady=20)

        # Labels to display retrieved data
        ttk.Label(data_frame, text="Retrieved Data:").pack()

        # Label to display retrieved data and comparison result
        self.data_label = ttk.Label(data_frame, text="")
        self.data_label.pack()

    def retrieve_data(self, sku, upc):
        # Retrieve data based on SKU or UPC and update labels with comparison results
        retrieved_data = None
        target_price = None  # Initialize target_price before the conditional statements
        try:
            if sku and upc == '':
                retrieved_data = get_record_sku(sku)
                target_price = target_scrape_backend(int(retrieved_data[1]))
            elif upc and sku == '':
                retrieved_data = get_record_upc(upc)
                target_price = target_scrape_backend(int(retrieved_data[1]))
        except TypeError:
            print("Error: ", TypeError)

        self.data_label.config(text="No data found")

        # Set default text if no data is found
        display_text = f"Title: {retrieved_data[4]}, SKU: {retrieved_data[1]}, UPC: {retrieved_data[0]}"

        # Compare GameStop and Target prices
        compare_result = compare_prices(retrieved_data[5], target_price)
        if compare_result is None:
            return

        self.gamestop_price_label.config(text=f"GameStop Price: {retrieved_data[5]}")
        self.target_price_label.config(text=f"Target Price: {target_price}")

        # Update label colors based on comparison result
        self.update_label_color(self.gamestop_price_label, retrieved_data[5], target_price)
        self.update_label_color(self.target_price_label, target_price, retrieved_data[5])

        self.data_label.config(text=f"{display_text}\nComparison Result: {compare_result}")

        print(display_text)

    def update_label_color(self, label, price, comparison_price):
        # Update label color based on the comparison result
        if price is not None and comparison_price is not None:
            if price > comparison_price:
                label.config(foreground="red")
            elif price < comparison_price:
                label.config(foreground="green")
            else:
                label.config(foreground="yellow")





def compare_prices(gamestop_price, target_price):
    if target_price is None or gamestop_price is None:
        return
    else:
        price_difference = abs(gamestop_price - target_price)
        if gamestop_price > target_price:
            return f"Target's price is ${price_difference} less than GameStop's."
        elif gamestop_price < target_price:
            return f"GameStop's price is ${price_difference} less than Target's."
        else:
            return "GameStop and Target prices are equal."



def init_user_interface():
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()

if __name__ == "__main__":

    init_user_interface()