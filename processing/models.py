from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    input_image_url = models.URLField()
    output_image_url = models.URLField(null=True, blank=True)

class ProcessingRequest(models.Model):
    csv_file = models.FileField(upload_to='processing/processed_csv/')
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
