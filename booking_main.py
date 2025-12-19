from datetime import datetime
from flight_class import Flight, show_numpy_seat_layout
from pricing_engine import PricingEngine
from revenue_analyzer import RevenueAnalyzer
import csv
import os

def log_action(func):
    def wrapper(*args, **kwargs):
        print("\nProcessing Request...")
        result = func(*args, **kwargs)
        print("\nDone\n")
        return result
    return wrapper


class Booking:
    def __init__(self, passenger, flight_no, seat_id, price):
        self.passenger = passenger
        self.flight_no = flight_no
        self.seat_id = seat_id
        self.price = price


flights = {
    "AI101": Flight("AI101", "Delhi", "Mumbai",
                    datetime(2025, 12, 25, 10, 30),
                    datetime(2025, 12, 25, 12, 45),
                    "Airbus A320"),

    "AI202": Flight("AI202", "Mumbai", "Bangalore",
                    datetime(2025, 12, 26, 8, 0),
                    datetime(2025, 12, 26, 10, 10),
                    "Boeing 737"),

    "AI303": Flight("AI303", "Chennai", "Hyderabad",
                    datetime(2025, 12, 27, 14, 15),
                    datetime(2025, 12, 27, 15, 45),
                    "ATR 72")
}


bookings = []

def save_flights_to_csv():
    file_exists = os.path.exists("flights.csv")

    with open("flights.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Flight No", "Origin", "Destination",
            "Departure", "Arrival", "Aircraft"
        ])

        for f in flights.values():
            writer.writerow([
                f.flight_no,
                f.origin,
                f.destination,
                f.departure,
                f.arrival,
                f.aircraft
            ])
save_flights_to_csv()            

def choose_seat_by_category(flight):
    try:
        print("\nChoose Seat Class")
        print("1. Economy")
        print("2.  Business")
        print("3. First")

        choice = input("Enter option: ")

        mapping = {"1": "Economy Class", "2": "Business Class", "3": "First Class"}
        if choice not in mapping:
            print("Invalid seat class")
            return None

        category = mapping[choice]
        available = [s.seat_id for s in flight.seats.values()
                     if s.category == category and not s.booked]

        if not available:
            print("No seats available")
            return None

        print("Available seats:", ", ".join(available))
        return input("Choose seat: ").upper()

    except Exception:
        print("Seat selection error")
        return None


def save_booking_to_csv(booking):
    file_exists = os.path.exists("bookings.csv")

    with open("bookings.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Passenger", "Flight No", "Seat", "Price", "Booking Time"
            ])

        writer.writerow([
            booking.passenger,
            booking.flight_no,
            booking.seat_id,
            booking.price,
            datetime.now()
        ])


@log_action
def book_ticket():
    try:
        print("\nAVAILABLE FLIGHTS")
        for fn, f in flights.items():
            print(f"{fn} → {f.origin} to {f.destination}")

        flight_no = input("Enter flight number: ").upper()
        if flight_no not in flights:
            print("Flight not found")
            return

        flight = flights[flight_no]
        show_numpy_seat_layout(flight)

        seat_id = choose_seat_by_category(flight)
        if not seat_id or seat_id not in flight.seats or flight.seats[seat_id].booked:
            print("Seat unavailable")
            return

        name = input("Passenger Name: ").strip()
        if not name:
            print("Name cannot be empty")
            return

        price = PricingEngine.calculate_price(flight, flight.seats[seat_id].category)

        flight.seats[seat_id].booked = True
        booking = Booking(name, flight_no, seat_id, price)
        bookings.append(booking)
        save_booking_to_csv(booking)

        print(f"\nBOOKING CONFIRMED")
        print(f"Passenger: {name}")
        print(f"Seat: {seat_id}")
        print(f"Fare: ₹{price}")

    except Exception as e:
        print("Booking failed:", e)


def cancel_booking():
    name = input("Enter passenger name: ").lower()
    for b in bookings:
        if b.passenger.lower() == name:
            flights[b.flight_no].seats[b.seat_id].booked = False
            bookings.remove(b)
            print("Booking cancelled")
            return
    print("Booking not found")


while True:
    print("\n================ AIRLINE BOOKING SYSTEM ================")
    print("1. Flight Details")
    print("2. Seat Configuration")
    print("3. Seat Layout (NumPy)")
    print("4. View Real-Time Price Breakdown")
    print("5. Book Ticket")
    print("6. Revenue Report")
    print("7. Cancel Booking")
    print("8. Exit")

   

    choice = input("Choose option: ")

    if choice == "1":
        for f in flights.values():
            print(f"\n{f.flight_no} | {f.origin} → {f.destination}")
            print(f"Departure: {f.departure}")
            print(f"Arrival: {f.arrival}")
            print(f"Aircraft: {f.aircraft}")
            print(f"Status: {f.status()}")

    elif choice == "2":
        for f in flights.values():
            f.show_seat_configuration()

    elif choice == "3":
        fn = input("Enter flight number: ").upper()
        if fn in flights:
            show_numpy_seat_layout(flights[fn])
        else:
            print("Invalid flight")
    elif choice == "4":
        fn = input("Enter flight number: ").upper()
        if fn in flights:
            PricingEngine.show_price_breakdown(flights[fn])
        else:
            print("Invalid flight")  

    elif choice == "5":
        book_ticket()

    elif choice == "6":
        RevenueAnalyzer.generate_report(bookings)

    elif choice == "7":
        cancel_booking()    
        
    elif choice == "8":
        print("Thank you for using the system!")
        break

    
    

    
