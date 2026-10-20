import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel, Dealer, Review


class Command(BaseCommand):
    help = "Load the capstone dealers, reviews, car makes, models, and demo users."

    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR) / "database" / "data"
        dealer_rows = json.loads((data_dir / "dealerships.json").read_text())["dealerships"]
        review_rows = json.loads((data_dir / "reviews.json").read_text())["reviews"]

        User.objects.update_or_create(
            username="root",
            defaults={"email": "root@bestcars.example", "first_name": "Root", "last_name": "Administrator", "is_staff": True, "is_superuser": True},
        )[0].set_password("RootPass123!")
        root = User.objects.get(username="root")
        root.set_password("RootPass123!")
        root.save()

        demo, _ = User.objects.update_or_create(
            username="talgat",
            defaults={"email": "talgat@bestcars.example", "first_name": "Talgat", "last_name": "Yerkhanuly"},
        )
        demo.set_password("Capstone123!")
        demo.save()

        Dealer.objects.all().delete()
        for row in dealer_rows:
            Dealer.objects.create(
                source_id=row["id"],
                city=row["city"],
                state=row["state"],
                st=row["st"],
                address=row["address"],
                zip=row["zip"],
                short_name=row["short_name"],
                full_name=row["full_name"],
            )

        for row in review_rows:
            dealer = Dealer.objects.filter(source_id=row["dealership"]).first()
            if not dealer:
                continue
            try:
                purchase_date = datetime.strptime(row.get("purchase_date", ""), "%m/%d/%Y").date()
            except ValueError:
                purchase_date = None
            Review.objects.create(
                source_id=row.get("id"),
                dealership=dealer,
                name=row.get("name", "Customer"),
                review=row.get("review", ""),
                purchase=row.get("purchase", False),
                purchase_date=purchase_date,
                car_make=row.get("car_make", ""),
                car_model=row.get("car_model", ""),
                car_year=row.get("car_year"),
                sentiment=self._sentiment(row.get("review", "")),
            )

        CarModel.objects.all().delete()
        CarMake.objects.all().delete()
        catalog = {
            "Audi": [("A6", "Sedan", 2022), ("Q5", "SUV", 2023)],
            "BMW": [("330i", "Sedan", 2024), ("X5", "SUV", 2023)],
            "Ford": [("Mustang", "Coupe", 2024), ("F-150", "Truck", 2023)],
            "Toyota": [("Camry", "Sedan", 2024), ("RAV4", "SUV", 2023)],
        }
        for make_name, models in catalog.items():
            make = CarMake.objects.create(name=make_name, description=f"{make_name} vehicles available through Best Cars dealerships.")
            for model_name, car_type, year in models:
                CarModel.objects.create(make=make, name=model_name, type=car_type, year=year)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Dealer.objects.count()} dealers, {Review.objects.count()} reviews, "
            f"{CarMake.objects.count()} makes, and {CarModel.objects.count()} models."
        ))

    @staticmethod
    def _sentiment(text):
        lowered = text.lower()
        if any(word in lowered for word in ("great", "excellent", "fantastic", "best", "friendly")):
            return "positive"
        if any(word in lowered for word in ("bad", "terrible", "poor", "worst", "rude")):
            return "negative"
        return "neutral"
