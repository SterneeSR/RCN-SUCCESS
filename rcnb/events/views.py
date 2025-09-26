from django.http import JsonResponse
import cloudinary
import cloudinary.uploader

def cloudinary_test(request):
    try:
        # Print Cloudinary config to verify connection
        config = cloudinary.config()
        
        # Upload a dummy image from Cloudinary's sample image URL
        result = cloudinary.uploader.upload(
            "https://res.cloudinary.com/demo/image/upload/sample.jpg",
            folder="test_uploads"
        )
        
        return JsonResponse({
            "cloud_name": config.cloud_name,
            "upload_success": True,
            "url": result.get("secure_url")
        })
    except Exception as e:
        return JsonResponse({"error": str(e)})
