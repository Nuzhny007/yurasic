from django.contrib import admin

from .models import Author, Song, Realization

# Register your models here.

admin.site.register([Author, Song, Realization])