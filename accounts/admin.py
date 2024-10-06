# booking/admin.py

from django.contrib import admin
from .models import PrintingPress, Booking

@admin.register(PrintingPress)
class PrintingPressAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'location']
    search_fields = ['name', 'location']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'printing_press', 'date', 'status']
    list_filter = ['status', 'date']
    search_fields = ['customer__username', 'printing_press__name']
