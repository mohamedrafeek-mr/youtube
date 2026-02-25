import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','youpro.settings')
import django
django.setup()
from videos.models import Video
print('total videos:', Video.objects.count())
print('statuses:', list(Video.objects.values_list('status', flat=True).distinct()))
print('examples', list(Video.objects.values('id','title','status')[:10]))
