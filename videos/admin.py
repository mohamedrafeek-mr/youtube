from django.contrib import admin
from .models import Video, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "thumbnail_preview", "uploader", "category", "status", "views", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description")
    readonly_fields = ("thumbnail_preview", "views", "created_at")

    def thumbnail_preview(self, obj):
        """Display thumbnail as an image in admin"""
        if obj.thumbnail and obj.thumbnail.name:
            return f'<img src="{obj.thumbnail.url}" width="100" height="60" style="object-fit:cover;" />'
        return "<em>No thumbnail</em>"
    thumbnail_preview.short_description = "Thumbnail"
    thumbnail_preview.allow_tags = True
