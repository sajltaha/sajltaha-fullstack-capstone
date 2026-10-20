from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    CAR_TYPES = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("Wagon", "Wagon"),
        ("Coupe", "Coupe"),
        ("Truck", "Truck"),
    ]
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CAR_TYPES, default="Sedan")
    year = models.IntegerField(validators=[MinValueValidator(2015), MaxValueValidator(2026)])

    class Meta:
        unique_together = ("make", "name", "year")

    def __str__(self):
        return f"{self.make.name} {self.name} ({self.year})"


class Dealer(models.Model):
    source_id = models.PositiveIntegerField(unique=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    st = models.CharField(max_length=2)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=12)
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)

    class Meta:
        ordering = ("source_id",)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    source_id = models.PositiveIntegerField(null=True, blank=True)
    dealership = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=160)
    review = models.TextField()
    purchase = models.BooleanField(default=False)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=100, blank=True)
    car_model = models.CharField(max_length=100, blank=True)
    car_year = models.PositiveIntegerField(null=True, blank=True)
    sentiment = models.CharField(max_length=16, default="neutral")
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="dealer_reviews")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at", "-id")

    def __str__(self):
        return f"{self.name}: {self.dealership.full_name}"
