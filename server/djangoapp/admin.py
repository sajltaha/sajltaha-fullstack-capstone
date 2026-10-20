from django.contrib import admin

from .models import CarMake, CarModel, Dealer, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = (CarModelInline,)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "make", "type", "year")
    list_filter = ("make", "type", "year")


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("source_id", "full_name", "city", "state")
    list_filter = ("state",)
    search_fields = ("full_name", "city", "state")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "dealership", "sentiment", "purchase", "created_at")
    list_filter = ("sentiment", "purchase")
