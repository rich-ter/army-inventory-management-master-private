# Use Python 3.10.12-slim as the base image
FROM python:3.10.12-slim

# Set environment variables to prevent Python from writing .pyc files and to buffer output
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the deb files and install system dependencies and Python
COPY ./template_django/offline-packages/debs /debs/
RUN dpkg -i /debs/*.deb || apt-get -f install -y && rm -rf /var/lib/apt/lists/* /debs

# Copy the requirements file and the offline packages into the container
COPY ./template_django/requirements.txt /app/
COPY ./template_django/offline-packages /app/offline-packages

# Install Python dependencies from the offline packages
RUN pip install --no-index --find-links=/app/offline-packages -r requirements.txt

# Copy the application code into the container
COPY ./template_django/ /app/

# Set the DJANGO_SETTINGS_MODULE environment variable
ENV DJANGO_SETTINGS_MODULE=DjangoHUD.settings

# Collect static files
RUN mkdir -p /app/staticfiles && chown -R www-data:www-data /app/staticfiles
RUN python manage.py collectstatic --noinput

# Ensure the media directory exists
RUN mkdir -p /app/product_images && chown -R www-data:www-data /app/product_images

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "DjangoHUD.wsgi:application", "--bind", "0.0.0.0:8000"]
