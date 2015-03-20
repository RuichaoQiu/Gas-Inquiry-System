from django.contrib import admin
from gm.models import Car, GasStation

class CarAdmin(admin.ModelAdmin):
	list_display = ('company', 'modeltype', 'madeyear','mpg','location')

class GasStationAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'price','location')

admin.site.register(Car, CarAdmin)
admin.site.register(GasStation, GasStationAdmin)