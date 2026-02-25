import os
from django.core.files.base import ContentFile
from io import BytesIO
import logging
import random

logger = logging.getLogger(__name__)


def generate_video_thumbnail(video):
    """
    Generate a thumbnail from the first frame of a video.
    Tries OpenCV, then placeholder
    """
    if not video.video_file:
        logger.warning(f"Video {video.id} has no video file")
        return False
        
    video_path = video.video_file.path
    
    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return False
    
    # Try OpenCV first
    if _generate_thumbnail_opencv(video, video_path):
        return True
    
    # Create a placeholder thumbnail
    logger.warning(f"Could not extract frame for video {video.id}, creating placeholder")
    return _generate_placeholder_thumbnail(video)


def _generate_thumbnail_opencv(video, video_path):
    """Generate thumbnail using OpenCV from 2 seconds into the video"""
    try:
        import cv2
        
        cap = cv2.VideoCapture(video_path)
        # Seek to 2 seconds (2000 ms)
        cap.set(cv2.CAP_PROP_POS_MSEC, 2000)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            logger.warning(f"Could not read video frame at 2s for {video.id}")
            return False
        
        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        from PIL import Image
        img = Image.fromarray(frame)
        
        # Resize to 320x180
        img.thumbnail((320, 180), Image.Resampling.LANCZOS)
        
        # Save to video model
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        thumb_filename = f"thumbnail_{video.id}.jpg"
        video.thumbnail.save(
            thumb_filename,
            ContentFile(thumb_io.read()),
            save=True
        )
        
        logger.info(f"[SUCCESS] Thumbnail generated using OpenCV for video {video.id}")
        return True
        
    except ImportError:
        logger.debug(f"OpenCV not available")
        return False
    except Exception as e:
        logger.warning(f"OpenCV thumbnail generation failed: {str(e)}")
        return False


def _generate_thumbnail_moviepy(video, video_path):
    """Generate thumbnail using moviepy"""
    try:
        from moviepy.editor import VideoFileClip  # noqa: F401, optional dependency
        from PIL import Image
        
        clip = VideoFileClip(video_path)
        frame_time = min(1, clip.duration - 0.1) if clip.duration > 0 else 0
        frame = clip.get_frame(frame_time)
        clip.close()
        
        img = Image.fromarray(frame.astype('uint8'))
        img.thumbnail((320, 180), Image.Resampling.LANCZOS)
        
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        thumb_filename = f"thumbnail_{video.id}.jpg"
        video.thumbnail.save(
            thumb_filename,
            ContentFile(thumb_io.read()),
            save=True
        )
        
        logger.info(f"[SUCCESS] Thumbnail generated using moviepy for video {video.id}")
        return True
        
    except ImportError as e:
        logger.debug(f"moviepy not available: {e}")
        return False
    except Exception as e:
        logger.warning(f"moviepy thumbnail generation failed: {str(e)}")
        return False


def _generate_placeholder_thumbnail(video):
    """Generate a simple placeholder thumbnail with video title"""
    try:
        from PIL import Image, ImageDraw
        
        # Create a colorful background
        colors = [
            (255, 107, 107), (106, 168, 79), (74, 144, 226),
            (220, 105, 183), (255, 165, 0), (155, 89, 182)
        ]
        color = random.choice(colors)
        
        # Create image
        img = Image.new('RGB', (320, 180), color=color)
        draw = ImageDraw.Draw(img)
        
        # Add play button symbol (triangle)
        play_x, play_y = 150, 75
        triangle = [(play_x, play_y - 20), (play_x + 35, play_y + 10), (play_x, play_y + 40)]
        draw.polygon(triangle, fill=(255, 255, 255))
        
        # Add video title text (truncated)
        title = video.title[:25] + "..." if len(video.title) > 25 else video.title
        draw.text((10, 150), title, fill=(255, 255, 255))
        
        # Save to video model
        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)
        thumb_io.seek(0)
        
        thumb_filename = f"thumbnail_{video.id}.jpg"
        video.thumbnail.save(
            thumb_filename,
            ContentFile(thumb_io.read()),
            save=True
        )
        
        logger.info(f"[SUCCESS] Placeholder thumbnail created for video {video.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to generate placeholder thumbnail: {str(e)}")
        return False
