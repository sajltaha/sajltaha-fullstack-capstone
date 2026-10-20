from django.contrib.auth.models import User
from django.test import TestCase

from .models import CarMake, CarModel, Dealer, Review


class CapstoneApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="talgat", password="Capstone123!")
        self.dealer = Dealer.objects.create(
            source_id=8,
            city="Topeka",
            state="Kansas",
            st="KS",
            address="288 Larry Place",
            zip="66642",
            short_name="Bytecard",
            full_name="Bytecard Car Dealership",
        )
        Review.objects.create(dealership=self.dealer, name="Alex Driver", review="Fantastic service", sentiment="positive")
        make = CarMake.objects.create(name="Toyota", description="Reliable vehicles")
        CarModel.objects.create(make=make, name="Camry", type="Sedan", year=2024)

    def test_login_and_logout(self):
        response = self.client.post(
            "/djangoapp/login",
            data='{"userName":"talgat","password":"Capstone123!"}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "Authenticated")
        self.assertEqual(self.client.get("/djangoapp/logout").status_code, 200)

    def test_dealer_endpoints(self):
        self.assertEqual(len(self.client.get("/djangoapp/get_dealers").json()["dealers"]), 1)
        self.assertEqual(self.client.get("/djangoapp/get_dealers/Kansas").json()["dealers"][0]["st"], "KS")
        self.assertEqual(self.client.get("/djangoapp/dealer/8").json()["dealer"][0]["city"], "Topeka")
        self.assertEqual(len(self.client.get("/djangoapp/reviews/dealer/8").json()["reviews"]), 1)

    def test_cars_and_sentiment(self):
        cars = self.client.get("/djangoapp/get_cars").json()
        self.assertEqual(cars["CarMakes"][0]["name"], "Toyota")
        result = self.client.get("/djangoapp/analyze/Fantastic%20services").json()
        self.assertEqual(result["sentiment"], "positive")
