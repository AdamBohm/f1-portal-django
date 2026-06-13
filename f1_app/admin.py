from django.contrib import admin
from .models import Country, Track, Team, Driver, Race

# Registrace nových modelů do administrace
admin.site.register(Country)
admin.site.register(Track)
admin.site.register(Team)
admin.site.register(Driver)
admin.site.register(Race)