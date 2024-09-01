```markdown
# Image Processing System

## Overview

This Django application processes image data from CSV files, compresses the images asynchronously, and stores the results in a database. The system includes APIs for uploading CSV files, checking the processing status, and supports webhook notifications after processing is completed.

## Features

- **Upload CSV:** Accepts a CSV file containing product names and associated image URLs.
- **Asynchronous Processing:** Compresses images by 50% of their original quality using Celery.
- **Status API:** Allows users to check the processing status using a unique request ID.
- **Webhook Support:** Notifies a specified endpoint upon completion of image processing.

## Tech Stack

- **Backend:** Django, Django Rest Framework, Celery
- **Database:** SQLite (default, can be replaced with PostgreSQL/MySQL)
- **Task Queue:** Celery with Redis as a broker
- **Image Processing:** Pillow library

## Setup Instructions

### Prerequisites

- Python 3.x
- Redis (for Celery)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/khand420/image-processing-system.git
   cd image-processing-system
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations:**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Redis Server:**

   Ensure Redis is running on your system. You can start Redis using:

   ```bash
   redis-server
   ```

6. **Start Celery Worker:**

   ```bash
   celery -A image_processor worker --pool=solo --loglevel=info
   or
   celery -A image_processor worker --loglevel=info
   ```

7. **Start the Django Server:**

   ```bash
   python manage.py runserver
   ```

### API Documentation

#### Upload CSV

- **URL:** `/api/upload/`
- **Method:** `POST`
- **Description:** Upload a CSV file for processing.
- **Request:**
  - `csv_file`: CSV file containing product names and image URLs.
- **Response:**
  ```json
  {
      "request_id": "<unique_request_id>"
  }
  ```

#### Status API

- **URL:** `/api/status/<request_id>/`
- **Method:** `GET`
- **Description:** Check the processing status of the uploaded CSV.
- **Response:**
  ```json
  {
      "status": "Pending/Processing/Completed"
  }
  ```

### Deployment

1. **Server Setup:**
   - Deploy the application on a cloud server.
   - Use Nginx as a reverse proxy and Gunicorn as the WSGI server.

2. **Environment Variables:**
   - Set up environment variables for Django settings, including `DEBUG`, `SECRET_KEY`, and database credentials.

3. **Celery and Redis:**
   - Ensure Redis is running on the server.
   - Start Celery workers using Supervisor or systemd for process management.

4. **Nginx Configuration:**
   - Configure Nginx to serve the Django application and handle static files.

5. **Testing:**
   - Test the application in the production environment to ensure everything is working as expected.

## Architecture Diagram

Include a visual diagram of the system architecture (using a tool like Draw.io) to illustrate the flow from CSV upload to image processing and status checking.

## Postman Collection

A Postman collection is provided for testing the APIs. You can import it into Postman using the following link:

[Postman Collection Link](https://github.com/khand420/img_processing/Image_processing.postman_collection)


