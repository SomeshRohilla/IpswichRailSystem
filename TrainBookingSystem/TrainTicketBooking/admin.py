from django.contrib import admin
from .models import Train, Booking


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    list_display = ('name', 'source', 'destination', 'travel_date', 'price')
    search_fields = ('name', 'source', 'destination')
    list_filter = ('travel_date',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'train', 'booked_on')
    list_filter = ('booked_on',)
    search_fields = ('user__username', 'train__name')
