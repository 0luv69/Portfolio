from django.db import models
import uuid
from django.core.validators import MaxLengthValidator
from django.utils.text import slugify


# Create your models here.

class IPAddressInfo(models.Model):
    contact = models.OneToOneField('Contact', on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField()
    network = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=110, blank=True, null=True)
    region = models.CharField(max_length=110, blank=True, null=True)
    region_code = models.CharField(max_length=10, blank=True, null=True)
    country_name = models.CharField(max_length=110, blank=True, null=True)
    country_code = models.CharField(max_length=10, blank=True, null=True)
    continent_code = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    timezone = models.CharField(max_length=60, blank=True, null=True)
    utc_offset = models.CharField(max_length=10, blank=True, null=True)
    org = models.CharField(max_length=300, blank=True, null=True)
    asn = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=20, blank=True, null=True)
    languages = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip} - {self.city}, {self.country_name}"


class Contact(models.Model):
    auth_uuid =  models.UUIDField(default=uuid.uuid4, editable=True, unique=False, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name



class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_type = models.CharField(max_length=20, choices=[("image", "Image"), ("svg", "SVG")], default="image")
    logo_image = models.ImageField(upload_to="technology_logos/", blank=True, null=True)
    svg = models.TextField(help_text="Inline SVG markup or SVG path/URL", blank=True, null=True)
    short_description = models.CharField(max_length=30)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    short_summary = models.CharField(max_length=180)
    full_description = models.TextField()
    role = models.CharField(max_length=120, blank=True)
    duration = models.CharField(max_length=120, blank=True)
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    technologies = models.ManyToManyField(Technology, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    



class Achievement(models.Model):

    class AchievementType(models.TextChoices):
        AWARD       = "award",        "Award"
        CERTIFICATION = "certification", "Certification"
        RECOGNITION = "recognition",  "Recognition"
        COMPETITION = "competition",  "Competition"
        PUBLICATION = "publication",  "Publication"
        MILESTONE   = "milestone",    "Milestone"
        OTHER       = "other",        "Other"

    # --- Core Info ---
    title            = models.CharField(max_length=200)
    slug             = models.SlugField(max_length=220, unique=True, blank=True)
    achievement_type = models.CharField(max_length=20, choices=AchievementType.choices, default=AchievementType.OTHER)
    issuer           = models.CharField(max_length=200, blank=True, help_text="Org/person who gave the award e.g. 'Google', 'Harvard'")
    short_description = models.CharField(max_length=180)
    full_description  = models.TextField(blank=True)
    

    # --- Media ---
    image      = models.ImageField(upload_to="achievements/", blank=True, null=True, help_text="Badge, certificate screenshot, trophy photo")
    image_alt  = models.CharField(max_length=120, blank=True)

    # --- Flags & Ordering ---
    is_featured   = models.BooleanField(default=False, help_text="Show on hero/highlights section")
    is_published  = models.BooleanField(default=True)
    sort_order    = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.issuer})" if self.issuer else self.title


class ProjectLink(models.Model):
    class LinkType(models.TextChoices):
        WEBSITE = "website", "Website"
        GITHUB = "github", "GitHub"
        DOCUMENTATION = "documentation", "Documentation"
        DEMO = "demo", "Live Demo"
        DEMO_VIDEO = "demo_video", "Demo Video"
        OTHER = "other", "Other"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="links")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="achievements_links", blank=True, null=True)
    link_type = models.CharField(max_length=20, choices=LinkType.choices, default=LinkType.WEBSITE)
    label = models.CharField(max_length=80, blank=True)
    url = models.URLField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        owner = self.project or self.achievement
        return f"{owner} - {self.link_type}"


class ProjectMedia(models.Model):
    class MediaType(models.TextChoices):
        DESKTOP_IMAGE = "desktop_image", "Desktop Image"
        MOBILE_IMAGE = "mobile_image", "Mobile Image"
        GIF_VIDEO = "gif_video", "GIF/Video"
        OTHER = "other", "Other"

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="media_items")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="achievements_media", blank=True, null=True)
    media_type = models.CharField(max_length=20, choices=MediaType.choices, default=MediaType.OTHER)
    image = models.ImageField(upload_to="projects/images/", blank=True, null=True)
    file = models.FileField(upload_to="projects/media/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    alt_text = models.CharField(max_length=120, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        owner = self.project or self.achievement
        return f"{owner} - {self.media_type}"

