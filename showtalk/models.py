from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)
    bio = models.TextField(max_length=512)

    def __str__(self) -> str:
        return self.user.username


class TVShow(models.Model):
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=512)
    image = models.ImageField(upload_to="show_covers", blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class FavouriteTVShow(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    tv_show = models.OneToOneField(TVShow, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


def get_extension(file_name: str) -> str | None:
    idx = file_name.rfind(".")  # Get the last extension
    return file_name[idx + 1 :] if idx > 0 else None


class Clip(models.Model):
    VIDEO_FORMATS = [
        "mov",
        "avi",
        "flv",
        "mp4",
        "mkv",
        "webm",
    ]

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    tv_show = models.OneToOneField(TVShow, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512)
    extension = models.CharField(max_length=8)
    video_file = models.FileField(upload_to="clips")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        extension = get_extension(self.video_file.name)
        if extension is None:
            raise ValueError(
                "Unable to parse file extension of " + self.video_file.name
            )
        self.extension = extension
        super().save(*args, **kwargs)

    # Ensures that `video_file` is a video, as Django does not have
    # native support for videos. See https://stackoverflow.com/a/68017377
    validators = [
        FileExtensionValidator(
            allowed_extensions=VIDEO_FORMATS,
            message="Unknown file format: not a video",
        )
    ]
