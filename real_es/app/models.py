from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Property(models.Model):
    PROPERTY_TYPES = [
        ('House', 'House'),
        ('Apartment', 'Apartment'),
        ('Land', 'Land'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('For Sale', 'For Sale'),
        ('For Rent', 'For Rent'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.FloatField()
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    image1 = models.FileField(null=True, blank=True)
    image2 = models.FileField(null=True, blank=True)
    image3 = models.FileField(null=True, blank=True)


class Amenities(models.Model):
    name = models.CharField(max_length=100)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)  

class ContactSeller(models.Model):
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the seller (User)
    date_submitted = models.DateTimeField(default=timezone.now)