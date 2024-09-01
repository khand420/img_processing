from django.contrib import admin
from .models import Image,ProcessingRequest, Product 

# Register your models here.

admin.site.register(Image)
admin.site.register(ProcessingRequest)
admin.site.register(Product)

