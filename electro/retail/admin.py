from django.contrib import admin
from .tasks import clear_debt_async
from .models import NetworkNode

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'email', 
        'city', 
        'country', 
        'street', 
        'house_number', 
        'producer_link', 
        'debt_to_producer', 
        'create_time'
    )
    list_editable = (
        'email', 
        'city', 
        'country', 
        'street', 
        'house_number'
    )
    list_filter = ('city', 'country')
    list_display_links = ('name',)
    actions = ('clear_debt',)
    
    def producer_link(self, obj):
        if obj.producer:
            return f'<a href="/admin/retail/networknode/{obj.producer.id}/change/">{obj.producer.name}</a>'
        else:
            return "-"
    
    producer_link.short_description = "Поставщик"
    producer_link.allow_tags = True
    
    @admin.action(description="Очистить задолженность")
    def clear_debt(self, request, queryset):
        if queryset.count() > 20:
            clear_debt_async.delay([obj.id for obj in queryset])
        else:
            queryset.update(debt_to_producer=0)