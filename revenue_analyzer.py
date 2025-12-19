import pandas as pd

class RevenueAnalyzer:

    @staticmethod
    def generate_report(bookings):
        try:
            if not bookings:
                print("No bookings available!")
                return

            df = pd.DataFrame({
                "Passenger": [b.passenger for b in bookings],
                "Flight": [b.flight_no for b in bookings],
                "Seat": [b.seat_id for b in bookings],
                "Price": [b.price for b in bookings]
            })

            print("\n💰 REVENUE REPORT")
            print(df)
            print(f"\nTOTAL REVENUE: ₹{df['Price'].sum()}")

            df.to_csv("revenue_report.csv", index=False)

        except Exception as e:
            print("Error generating revenue report:", e)


#“The RevenueAnalyzer class uses Pandas to generate a tabular revenue report, calculate total earnings, and export the data as a CSV file.