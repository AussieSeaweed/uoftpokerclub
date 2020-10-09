from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import Model, ForeignKey, CharField, CASCADE, DateTimeField, BooleanField, ImageField, \
    EmailField, TextField


class Category(Model):
    parent = ForeignKey("Category", related_name="categories", on_delete=CASCADE, blank=True, null=True)

    name = CharField(max_length=255)
    description = CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name}/" if self.parent is None else f"{self.parent}{self.name}/"

    class Meta:
        verbose_name_plural = "Categories"


class Post(Model):
    parent = ForeignKey(Category, related_name="posts", on_delete=CASCADE, blank=True, null=True)

    name = CharField(max_length=255)
    description = CharField(max_length=255, blank=True)
    draft = BooleanField(default=False)
    important = BooleanField(default=False)

    created_on = DateTimeField(auto_now_add=True)
    updated_on = DateTimeField(auto_now=True)

    thumbnail = ImageField(upload_to="thumbnails", blank=True, null=True)
    content = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.name if self.parent is None else f"{self.parent}{self.name}"


class Event(Model):
    post = ForeignKey(Post, related_name="events", on_delete=CASCADE, blank=True, null=True)

    name = CharField(max_length=255)
    description = CharField(max_length=255, blank=True)

    start_time = DateTimeField()
    end_time = DateTimeField()

    def __str__(self):
        return self.name


class Correspondence(Model):
    name = CharField(max_length=255)
    email = EmailField()
    subject = CharField(max_length=255)
    content = TextField()

    created_on = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
