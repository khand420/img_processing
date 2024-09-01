from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import ProcessingRequest
from .tasks import process_csv, test_task
from rest_framework import status

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


class UploadCSV(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES['csv_file']
        processing_request = ProcessingRequest.objects.create(csv_file=file, status='Pending')
        process_csv.delay(processing_request.id)
        # test_task() sync task
        test_task.delay() #async task

        # process_csv(processing_request.id)  # Run synchronously
        return Response({"request_id": processing_request.id}, status=201)

class StatusAPI(APIView):
    def get(self, request, request_id):
        processing_request = ProcessingRequest.objects.get(id=request_id)
        return Response({"status": processing_request.status})


class WebhookAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            print(f"Received webhook data: {data}")
            # Add additional processing logic here if needed
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Error processing webhook: {e}")
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        





# class WebhookAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data
#         # Process the webhook data as needed
#         # print(f"Received webhook: {data}").
#         print(f"Raw body: {request.body}")
#         print(f"Received data: {request.data}")

#         return Response({'status': 'success'}, status=status.HTTP_200_OK)

# @csrf_exempt
# def webhook_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         # Process the webhook data as needed
#         print(f"Received webhook: {data}")
#         return JsonResponse({'status': 'success'}, status=200)
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=400)