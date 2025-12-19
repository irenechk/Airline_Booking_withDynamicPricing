import numpy as np
from datetime import datetime

class Seat:
    def __init__(self, seat_id, category):
        self.seat_id = seat_id
        self.category = category
        self.booked = False


class Flight:
    def __init__(self, flight_no, origin, destination, departure, arrival, aircraft):
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrival = arrival
        self.aircraft = aircraft

        self.eco_seats = 25
        self.bus_seats = 15
        self.first_seats = 10

        self.base_prices = {
            "Economy Class": 1000,
            "Business Class": 2500,
            "First Class": 4000
        }

        self.seats = {}
        self.create_seats()

    def create_seats(self):
        for i in range(1, self.first_seats + 1):
            self.seats[f"F{i}"] = Seat(f"F{i}", "First Class")
        for i in range(1, self.bus_seats + 1):
            self.seats[f"B{i}"] = Seat(f"B{i}", "Business Class")
        for i in range(1, self.eco_seats + 1):
            self.seats[f"E{i}"] = Seat(f"E{i}", "Economy Class")

    def show_seat_configuration(self):
        print("\nSEAT CONFIGURATION")
        print(f"Economy Class  : {self.eco_seats}")
        print(f"Business Class : {self.bus_seats}")
        print(f"First Class    : {self.first_seats}")

    def status(self):
        now = datetime.now()
        if now < self.departure:
            return "On-Time"
        elif now > self.arrival:
            return "Departed"
        else:
            return "Delayed"


def show_numpy_seat_layout(flight):
    print(f"\nNUMPY SEAT LAYOUT — Flight {flight.flight_no}")

    layout_config = {
        "First Class": (2, 5),
        "Business Class": (3, 5),
        "Economy Class": (5, 5)
    }

    for category, (rows, cols) in layout_config.items():
        print(f"\n🔸 {category}")
        layout = np.full((rows, cols), "🟩")

        seats = [s for s in flight.seats.values() if s.category == category]

        for idx, seat in enumerate(seats):
            r, c = divmod(idx, cols)
            if r < rows and seat.booked:
                layout[r][c] = "🟥"

        for row in layout:
            print(" ".join(row))


#This module manages flights and seats using object-oriented programming and displays real-time seat layouts visually using NumPy.”