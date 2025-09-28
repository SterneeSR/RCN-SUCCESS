# core/views.py
import csv
import openpyxl
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import BulkUploadForm
from products.models import Product
from startups.models import Startup

@staff_member_required
def bulk_upload_view(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['file']
            
            try:
                if upload_file.name.endswith('.csv'):
                    # Handle CSV file
                    decoded_file = upload_file.read().decode('utf-8').splitlines()
                    reader = csv.DictReader(decoded_file)
                    process_rows(reader)
                elif upload_file.name.endswith(('.xls', '.xlsx')):
                    # Handle Excel file
                    workbook = openpyxl.load_workbook(upload_file)
                    sheet = workbook.active
                    
                    # Get headers from the first row
                    headers = [cell.value for cell in sheet[1]]
                    
                    # Create a list of dictionaries for each row
                    rows = []
                    for row in sheet.iter_rows(min_row=2, values_only=True):
                        rows.append(dict(zip(headers, row)))
                        
                    process_rows(rows)
                else:
                    messages.error(request, "Unsupported file format. Please upload a CSV or Excel file.")
                    return redirect('admin:bulk_upload')
                    
                messages.success(request, "Bulk upload successful!")
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
            
            return redirect('admin:bulk_upload')
    else:
        form = BulkUploadForm()
    
    context = {
        'form': form,
        'title': 'Bulk Upload Products and Startups',
    }
    return render(request, 'admin/bulk_upload.html', context)


def process_rows(reader):
    for row in reader:
        startup, created = Startup.objects.get_or_create(
            name=row['startup_name'],
            defaults={
                'category': row.get('category', 'undefined'),
                'description': row.get('startup_description', ''),
            }
        )

        if created and row.get('startup_logo_url'):
            # Download and save the startup logo
            save_image_from_url(startup, 'logo', row['startup_logo_url'])

        if row.get('product_name'):
            product = Product.objects.create(
                startup=startup,
                name=row['product_name'],
                description=row.get('product_description', ''),
                price=row.get('price'),
            )
            
            if row.get('product_image_url'):
                # Download and save the product image
                save_image_from_url(product, 'image', row['product_image_url'])


def save_image_from_url(model_instance, field_name, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Get the filename from the URL
            filename = url.split('/')[-1]
            
            # Save the image to the specified field
            getattr(model_instance, field_name).save(
                filename,
                ContentFile(response.content),
                save=True
            )
    except Exception as e:
        # Handle cases where the image can't be downloaded
        print(f"Could not download image from {url}: {e}")