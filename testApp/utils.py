import boto3
import uuid
from django.conf import settings
from botocore.exceptions import ClientError
from PIL import Image
import io

class S3ImageUploader:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        self.bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    
    def upload_image(self, image_file, folder='images/'):
        """
        Upload image to S3 bucket
        Args:
            image_file: Django UploadedFile object
            folder: S3 folder path (default: 'images/')
        Returns:
            dict: {'success': bool, 'url': str, 'error': str}
        """
        try:
            # Validate image
            if not self._is_valid_image(image_file):
                return {'success': False, 'error': 'Invalid image format'}
            
            # Generate unique filename
            file_extension = image_file.name.split('.')[-1].lower()
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            s3_key = f"{folder}{unique_filename}"
            
            # Optimize image if needed
            optimized_image = self._optimize_image(image_file)
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                optimized_image,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': f'image/{file_extension}',
                    'ACL': 'public-read'
                }
            )
            
            # Generate URL
            image_url = f"https://{self.bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{s3_key}"
            
            return {
                'success': True,
                'url': image_url,
                'key': s3_key,
                'filename': unique_filename
            }
            
        except ClientError as e:
            return {'success': False, 'error': f'AWS Error: {str(e)}'}
        except Exception as e:
            return {'success': False, 'error': f'Upload failed: {str(e)}'}
    
    def delete_image(self, s3_key):
        """Delete image from S3 bucket"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return {'success': True}
        except ClientError as e:
            return {'success': False, 'error': str(e)}
    
    def _is_valid_image(self, image_file):
        """Validate image file"""
        allowed_formats = ['jpg', 'jpeg', 'png', 'gif', 'webp']
        file_extension = image_file.name.split('.')[-1].lower()
        
        if file_extension not in allowed_formats:
            return False
        
        # Check file size (max 10MB)
        if image_file.size > 10 * 1024 * 1024:
            return False
        
        return True
    
    def _optimize_image(self, image_file):
        """Optimize image for web"""
        try:
            # Open image with PIL
            image = Image.open(image_file)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large
            max_size = (1920, 1080)
            if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Save optimized image to bytes
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            return output
            
        except Exception:
            # If optimization fails, return original
            image_file.seek(0)
            return image_file