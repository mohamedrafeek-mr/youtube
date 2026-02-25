import os
import shutil
import subprocess
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from videos.models import Video


class Command(BaseCommand):
    help = "Process uploaded videos: convert to mp4 and generate thumbnail using ffmpeg"

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Do not run ffmpeg; just report')
        parser.add_argument('--id', type=int, help='Process a single Video by id')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        vid = options.get('id')

        qs = Video.objects.filter(status='processing')
        if vid:
            qs = qs.filter(id=vid)

        if not qs.exists():
            self.stdout.write('No videos to process.')
            return

        for video in qs:
            try:
                self.process_video(video, dry_run=dry_run)
            except Exception as e:
                self.stderr.write(f'Error processing video {video.id}: {e}')

    def process_video(self, video: Video, dry_run=False):
        media_root = Path(settings.MEDIA_ROOT)
        input_path = Path(video.video_file.path)
        self.stdout.write(f'Processing Video id={video.id} file={input_path}')

        # Prepare output mp4 path
        out_dir = input_path.parent
        out_name = f'{input_path.stem}_converted.mp4'
        out_path = out_dir / out_name

        thumb_dir = media_root / 'thumbnails'
        thumb_dir.mkdir(parents=True, exist_ok=True)
        thumb_path = thumb_dir / f'{video.id}.jpg'

        if dry_run:
            self.stdout.write(f'[dry-run] would convert {input_path} -> {out_path}')
            self.stdout.write(f'[dry-run] would generate thumbnail {thumb_path}')
            # mark as published in dry-run? no
            return

        # Convert to mp4 using ffmpeg
        cmd_convert = [
            'ffmpeg', '-y', '-i', str(input_path),
            '-c:v', 'libx264', '-preset', 'fast', '-crf', '23',
            str(out_path)
        ]
        self.stdout.write('Running ffmpeg convert...')
        subprocess.check_call(cmd_convert)

        # Generate thumbnail at 1s
        cmd_thumb = ['ffmpeg', '-y', '-i', str(out_path), '-ss', '00:00:01.000', '-vframes', '1', str(thumb_path)]
        self.stdout.write('Generating thumbnail...')
        subprocess.check_call(cmd_thumb)

        # Replace original file with converted file (move)
        final_rel = video.video_file.name  # keep same field name path
        final_path = media_root / final_rel
        # Backup original
        backup_path = input_path.with_suffix(input_path.suffix + '.orig')
        if input_path.exists():
            shutil.move(str(input_path), str(backup_path))

        shutil.move(str(out_path), str(final_path))

        # Save thumbnail path to model
        # thumbnail field stores relative path from MEDIA_ROOT
        thumb_rel = os.path.relpath(str(thumb_path), str(media_root))
        video.thumbnail.name = thumb_rel.replace('\\', '/')
        video.status = 'published'
        video.save()

        self.stdout.write(f'Video {video.id} processed successfully.')
