# Image Manipulation App

## Overview

This web application allows users to perform various image manipulation tasks, such as removing backgrounds and converting images to black and white. Users can upload images and trigger different processing services directly from the homepage.

### Technologies Used

- **Backend**: Django, HTMX, Celery, AWS Lambda
- **Frontend**: Materialize CSS framework
- **Database**: PostgreSQL
- **Task Queue**: Celery
- **Deployment**: Docker, AWS (for Lambda and S3)

## Features

- **Image Upload**: Users can easily upload images.
- **Image Processing Options**: 
  - Remove Background
  - Convert to Black and White
  - Resize Image
  - Apply Filters
- **Asynchronous Processing**: Tasks are handled in the background using Celery.
- **AWS Integration**: Offloads specific image processing tasks to AWS Lambda and stores images in AWS S3.
- **Responsive UI**: Built using the Materialize CSS framework.

## Getting Started

### Prerequisites

To run this application, you only need to have **Docker** and **Docker Compose** installed on your machine.

### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/your-username/image-manipulation-app.git
    cd image-manipulation-app
    ```

2. **Create a `.env` file in /imageassistant/**:

    Copy the `.env.example` file to `.env` and fill in your environment-specific configurations. This includes AWS credentials and database settings.

    Example `.env` file:
    ```env
    SECRET_KEY=yoursecretkey
    ALLOWED_HOSTS=127.0.0.1,localhost
    DB_NAME=something
    DB_USER=someuser
    DB_PASSWORD=somepassword
    DB_HOST=172.17.0.1   the docker container user the host postgres, this mean you will need to figure out the gateway but its normally this
    DJANGO_SETTINGS_MODULE=app.settings
    ```

3. **Build and start the application**:

    ```bash
    docker-compose up --build
    ```

    This command will build the Docker images and start the application, including the web server, PostgreSQL database, Redis server, and Celery workers.

### AWS Setup

1. **AWS S3**: 
   - Create an S3 bucket to store the uploaded images.
   - Update the S3 bucket name in your `.env` file.
   - Set the appropriate IAM policies to allow your application to upload and retrieve images.

2. **AWS Lambda**:
   - Set up AWS Lambda functions for specific image processing tasks, ensuring they can be triggered from the Django backend.

## Usage

1. Navigate to `http://localhost:8084` in your web browser.
2. On the homepage, you'll find an **Upload Image** button.
3. Upload an image and select from the available processing options like:
   - **Remove Background**: Triggers the background removal function.
   - **Convert to Black and White**: Converts the uploaded image to grayscale.
   - **Resize Image**: Resizes the image based on user input.

## Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

