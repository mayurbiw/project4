from django.contrib import admin
from . models import UsersList, Categories, savedNews


admin.site.site_header = 'News aggregator admin'

# Register your models here.
admin.site.register(Categories)
admin.site.register(UsersList)
admin.site.register(savedNews)
