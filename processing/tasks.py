from celery import shared_task
from PIL import Image as PilImage
import requests
import os
from django.conf import settings

from io import BytesIO
from .models import Image, ProcessingRequest, Product


@shared_task
def test_task():
    print("Test task executed successfully!")



@shared_task #(bind=True)
def compress_image(image_id):
    try:
        image_obj = Image.objects.get(id=image_id)
        response = requests.get(image_obj.input_image_url, timeout=10)  # Add timeout to avoid long waits
        response.raise_for_status()  # Raise an error for bad HTTP status codes

        img = PilImage.open(BytesIO(response.content))
        img = img.convert('RGB')
        
        # Resize image by 50% of its original quality
        img = img.resize((img.width // 2, img.height // 2))
        
        # Save the processed image to a local file
        # output_path = f"compressed_images/{os.path.basename(image_obj.input_image_url)}"
        # img.save(output_path, 'JPEG', quality=50)
        
        # Detect the current project directory
        project_directory = settings.BASE_DIR
        output_dir = os.path.join(project_directory, 'processing', 'compressed_images')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, os.path.basename(image_obj.input_image_url))
        img.save(output_path, 'JPEG', quality=50)

        
        # Save output URL (This should ideally be a cloud storage URL)
        image_obj.output_image_url = output_path
        image_obj.save()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")
        image_obj.output_image_url = None
        image_obj.save()
    except Exception as e:
        print(f"Error processing image: {e}")
        image_obj.output_image_url = None
        image_obj.save()





@shared_task()# bind=True
def process_csv(request_id):
    try:
        processing_request = ProcessingRequest.objects.get(id=request_id)
        processing_request.status = 'Processing'
        processing_request.save()
        print(f"Processing started for request_id: {request_id}")

        # Process the CSV file
        import csv
        with open(processing_request.csv_file.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Processing row: {row}")  # Add debug print
                product, created = Product.objects.get_or_create(name=row['Product Name'])
                input_image_urls = row['Input Image URLs'].split(',')
                for url in input_image_urls:
                    print(f"Processing image URL: {url}")  # Add debug print
                    image = Image.objects.create(product=product, input_image_url=url)
                    compress_image.delay(image.id)
                    # compress_image(image.id)


        processing_request.status = 'Completed'
        processing_request.save()
        print(f"Processing completed for request_id: {request_id}")
        notify_webhook.delay(request_id)
        # notify_webhook(request_id)

    except Exception as e:
        print(f"Error processing CSV: {e}")
        processing_request.status = 'Failed'
        processing_request.save()




@shared_task()
def notify_webhook(request_id):
    processing_request = ProcessingRequest.objects.get(id=request_id)
    webhook_url = "http://localhost:8000/api/webhook/"  # Replace with actual webhook URL
    payload = {
        "request_id": request_id,
        "status": processing_request.status,
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code == 200:
        print(f"Successfully notified webhook for request ID {request_id}")
    else:
        print(f"Failed to notify webhook for request ID {request_id}, status code: {response.status_code}")






# @shared_task
# def process_csv(request_id):
#     processing_request = ProcessingRequest.objects.get(id=request_id)
#     processing_request.status = 'Processing'
#     processing_request.save()

#     # Process the CSV file
#     import csv
#     with open(processing_request.csv_file.path, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             product, created = Product.objects.get_or_create(name=row['Product Name'])
#             input_image_urls = row['Input Image Urls'].split(',')
#             for url in input_image_urls:
#                 image = Image.objects.create(product=product, input_image_url=url)
#                 compress_image.delay(image.id)

#     processing_request.status = 'Completed'
#     processing_request.save()
#     notify_webhook.delay(request_id)



# @shared_task
# def compress_image(image_id):
#     image_obj = Image.objects.get(id=image_id)
#     response = requests.get(image_obj.input_image_url)
#     img = PilImage.open(BytesIO(response.content))
#     img = img.convert('RGB')
    
#     # Resize image by 50% of its original quality
#     img = img.resize((img.width // 2, img.height // 2))
    
#     # Save the processed image to a local file
#     output_path = f"compressed_images/{os.path.basename(image_obj.input_image_url)}"
#     img.save(output_path, 'JPEG', quality=50)
    
#     # Save output URL (This should ideally be a cloud storage URL)
#     image_obj.output_image_url = output_path
#     image_obj.save()
