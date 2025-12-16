from django.core.management.base import BaseCommand
from TrainTicketBooking.models import Train
from datetime import date, timedelta, time
import random


class Command(BaseCommand):
    help = "Generate trains for December & January with dynamic pricing"

    def handle(self, *args, **kwargs):

        today = date.today()

        # 🗑 DELETE OLD DATA
        Train.objects.all().delete()
        self.stdout.write("🗑 Old train data deleted")

        cities = [
            "London",
            "Manchester",
            "Birmingham",
            "Leeds",
            "Liverpool",
            "Edinburgh",
            "Glasgow",
            "ipswich",
            "Cambridge",
            "Oxford",
            "nottingham",
            "Norwich",
            "York",
            "Sheffield"
        ]

        # 📆 DATE RANGE (DECEMBER + JANUARY)
        start_date = date(today.year, 12, 1)
        end_date = date(today.year + 1, 1, 31)

        current_date = start_date

        while current_date <= end_date:

            days_before = (current_date - today).days

            # 💰 PRICE LOGIC
            if days_before >= 30:
                price_range = (20, 40)
            elif days_before >= 15:
                price_range = (40, 70)
            elif days_before >= 7:
                price_range = (70, 100)
            else:
                price_range = (100, 150)

            for source in cities:
                for destination in cities:
                    if source == destination:
                        continue

                    # 🚆 MORNING TRAIN
                    m_depart = random.randint(6, 9)
                    m_duration = random.randint(1, 4)
                    m_arrival = min(m_depart + m_duration, 23)

                    Train.objects.create(
                        name=f"{source[:3]}-{destination[:3]}-M{random.randint(100,999)}",
                        source=source,
                        destination=destination,
                        travel_date=current_date,
                        departure_time=time(m_depart, 0),
                        arrival_time=time(m_arrival, 0),
                        price=random.randint(*price_range)
                    )

                    # 🌆 EVENING TRAIN
                    e_depart = random.randint(16, 19)
                    e_duration = random.randint(1, 4)
                    e_arrival = min(e_depart + e_duration, 23)

                    Train.objects.create(
                        name=f"{source[:3]}-{destination[:3]}-E{random.randint(100,999)}",
                        source=source,
                        destination=destination,
                        travel_date=current_date,
                        departure_time=time(e_depart, 30),
                        arrival_time=time(e_arrival, 30),
                        price=random.randint(*price_range)
                    )

            current_date += timedelta(days=1)

        self.stdout.write(self.style.SUCCESS(
            "✅ Trains generated for December & January with smart pricing!"
        ))
