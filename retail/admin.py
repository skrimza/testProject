from django.contrib import admin
from django.utils.html import format_html
from .tasks import clear_debt_async
from .models import NetworkNode

@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'city', 'supplier_link', 'debt', 'created_at')
    list_editable = ('name', 'email', 'country', 'street', 'house_number')
    list_filter = ('city',)
    actions = ('clear_debt',)
    
    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="/admin/network/networknode/{}/change/">{}</a>', 
                obj.supplier.id, 
                obj.supplier.name
            )
        else:
            return "-"
    
    supplier_link.short_description = "Поставщик"
    
    @admin.action(description="Очистить задолженность")
    def clear_debt(self, request, queryset):
        if queryset.count() > 20:
            clear_debt_async.delay([obj.id for obj in queryset])
        else:
            queryset.update(debt=0)