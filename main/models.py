from django.db import models
import uuid

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


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='img/projects/')
    btn1_text = models.CharField(max_length=50)
    btn1_url = models.URLField(null=True, blank=True)

    btn2_text = models.CharField(max_length=50)
    btn2_url = models.URLField(null=True, blank=True)


    prj_value = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title