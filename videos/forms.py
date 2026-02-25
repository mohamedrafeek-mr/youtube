from django import forms
from django.conf import settings
from .models import Video
import os


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'category', 'video_file']

    def clean_video_file(self):
        f = self.cleaned_data.get('video_file')
        if not f:
            raise forms.ValidationError('No file uploaded')

        # Validate extension
        name, ext = os.path.splitext(f.name.lower())
        if ext not in getattr(settings, 'ALLOWED_VIDEO_EXTENSIONS', ['.mp4']):
            raise forms.ValidationError('Unsupported file extension.')

        # Validate size
        max_size = getattr(settings, 'MAX_VIDEO_UPLOAD_SIZE', 500 * 1024 * 1024)
        if f.size > max_size:
            raise forms.ValidationError(f'File too large (max {max_size//(1024*1024)} MB).')

        return f
