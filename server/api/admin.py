from django.contrib import admin
from .models import Sample, WaterBrand, Customer


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WaterBrand)
class WaterBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'customer_type', 'brand', 'open_date', 'last_delivery_date', 'is_active', 'created_at']
    list_filter = ['customer_type', 'brand', 'is_active', 'open_date', 'created_at']
    search_fields = ['id', 'name', 'phone', 'address']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'open_date'
