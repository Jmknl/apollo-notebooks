from django.db import models
from django.conf import settings
from django_ckeditor_5.fields import CKEditor5Field
from django.core.exceptions import ValidationError
from django.utils import timezone


class Book(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to="apollo/")
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Paper(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    paragraphs = CKEditor5Field("Parágrafos", config_name="default")  


class Profile(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )  
    profile_image = models.ImageField(
    upload_to="apollo/profiles/", blank=True, null=True )
    banner_image = models.ImageField(upload_to="apollo/banners/", blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"


class Event(models.Model):
    user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE )  
    title = models.CharField(max_length=200)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()

    def clean(self):
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError(
                    "A data de fim não pode ser anterior à data de início."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TranslationCache(models.Model):
    original_text = models.CharField(max_length=255)
    target_language = models.CharField(max_length=10)
    translated_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("original_text", "target_language")
        indexes = [ models.Index(fields=["original_text", "target_language"]), ]

    def __str__(self):
        return f"{self.original_text[:30]}... -> {self.target_language}"


class DictionaryCache(models.Model):
    word = models.CharField(max_length=255, unique=True)
    definition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["word"]),
        ]

    def __str__(self):
        return self.word
