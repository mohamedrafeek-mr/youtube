from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management import call_command
from .models import Video
from .utils import generate_video_thumbnail
import logging
import threading
import traceback

logger = logging.getLogger(__name__)

# Configure logging to file for debugging
try:
    handler = logging.FileHandler('thumbnail_generation.log')
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
except:
    pass


@receiver(post_save, sender=Video)
def generate_thumbnail_for_video(sender, instance, created, **kwargs):
    """
    Signal handler to automatically generate thumbnail when video is created.
    """
    logger.info(f"Signal triggered for video {instance.id}: created={created}, has_video_file={bool(instance.video_file)}")
    
    if created and instance.video_file:
        logger.info(f"Starting thumbnail generation for video {instance.id}")
        _generate_thumbnail_async(instance.id)
    elif created and not instance.video_file:
        logger.warning(f"Video {instance.id} created but no video file attached")
    else:
        logger.debug(f"Signal not triggered: created={created}")


def _generate_thumbnail_async(video_id):
    """Generate thumbnail in background thread"""
    try:
        logger.info(f"Background thread started for video {video_id}")
        video = Video.objects.get(id=video_id)
        logger.info(f"Retrieved video {video_id} from database")
        
        result = generate_video_thumbnail(video)
        if result:
            logger.info(f"Thumbnail generation completed successfully for video {video_id}")
            # mark published if still processing
            if video.status != 'published':
                video.status = 'published'
                video.save(update_fields=['status'])
                logger.info(f"Video {video_id} status set to published")
    except Video.DoesNotExist:
        logger.error(f"Video {video_id} not found in database")
    except Exception as e:
        logger.error(f"Error generating thumbnail for video {video_id}: {str(e)}")
        logger.error(traceback.format_exc())
