from dataclasses import dataclass
from datetime import datetime
import numpy as np
import csv
import os
from datetime import datetime




class PricingEngine:

    @staticmethod
    def calculate_price(flight, seat_category):
        base_price = flight.base_prices[seat_category]

        hours_left = (flight.departure - datetime.now()).total_seconds() / 3600

        demand_factor = np.random.uniform(0.2, 0.4)
        demand_price = base_price * demand_factor

        peak_price = base_price * 0.15 if 18 <= datetime.now().hour <= 22 else 0
        early_discount = -base_price * 0.05 if hours_left > 48 else 0

        premium_price = base_price * 0.30
        last_minute_price = base_price * 0.50

        standard_price = base_price + demand_price + peak_price + early_discount
        
        if hours_left <= 24:
            final_price = base_price + last_minute_price
        elif hours_left <= 48:
            final_price = base_price + premium_price
        else:
            final_price = standard_price
        return round(final_price, 2)
    

    @staticmethod
    def show_price_breakdown(flight):
        print("\nREAL-TIME PRICE BREAKDOWN")

        for category, base in flight.base_prices.items():
            final_price = PricingEngine.calculate_price(flight, category)

            print(f"\nSeat Class: {category}")
            print(f"Base Price      : ₹{base}")
            print(f"Final Price Now : ₹{final_price}")

@staticmethod
def log_price(flight_no, seat_class, price):
    file_exists = os.path.exists("pricing_history.csv")

    with open("pricing_history.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Flight No", "Seat Class", "Price", "Timestamp"
            ])

        writer.writerow([
            flight_no,
            seat_class,
            price,
            datetime.now()
        ])
            

#The PricingEngine class dynamically calculates airline ticket prices using demand, peak hours, and time left before departure, similar to real-world airline pricing systems.”