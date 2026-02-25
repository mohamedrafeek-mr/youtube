from django.core.management.base import BaseCommand
from users.models import Profile

class Command(BaseCommand):
    help = 'Set default avatar for profiles with no avatar'

    def handle(self, *args, **options):
        updated = 0
        for profile in Profile.objects.filter(avatar__isnull=True):
            profile.avatar = 'avatars/human_avatar.png'
            profile.save()
            updated += 1
        for profile in Profile.objects.filter(avatar=''):
            profile.avatar = 'avatars/human_avatar.png'
            profile.save()
            updated += 1
        self.stdout.write(self.style.SUCCESS(f'Set default avatar for {updated} profiles.'))
