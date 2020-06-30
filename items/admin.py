from django.contrib import admin
from .models import Item,Cart
from .forms import ItemForm
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ['name','image','newly_arrived','original_cost','revised_cost','stock','sold','booked','category','subcategory','material_type']

admin.site.register(Item, ItemAdmin)
admin.site.register(Cart)
