from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# from .utils import validate_times 
# Create your models here.

COURT_TYPES = (
    ('clay', 'Clay'),
    ('grass', 'Grass'),
    ('hardcourt', 'Hardcourt'),
)
COURT_LOCATION = (
    ('indoors', 'Indoors'),
    ('outside', 'Out-side'),
)
BOOK_TYPE = (
    ('single', '1 Person'),
    ('child', 'Child Under 18'),
    ('double', 'Double (4 persons)'),
    ('couple', 'Couple'),
    ('family', 'Family'),
)

STATUS=(
    ('pendig', 'Pendig'),
    ('done', 'Done'),
    ('paid', 'Paid'),
)

class Court(models.Model):
    name = models.CharField(max_length=50, unique=True)
    court_type = models.CharField(max_length=20, choices=COURT_TYPES)
    court_location = models.CharField(max_length=20, choices=COURT_LOCATION)
    has_lighting = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    pre_image = models.ImageField(upload_to='static/img/upload', null=False)
    description = models.TextField(null=True);
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
class Image(models.Model):
    name = models.ImageField(upload_to='static/img/upload')
    court_id = models.ForeignKey(Court, on_delete=models.CASCADE)
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Sessions(models.Model):
    name = models.CharField(max_length=50, unique=True)
    startTime = models.TimeField()
    endTime = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
    def clean(self):
        if self.startTime >= self.endTime:
            raise ValidationError("Start time must be before end time.")
        super().clean()

PHONE_REGEX = r'^07\d{8}$' 

class Booking(models.Model):
    date = models.DateField()
    session_id = models.ForeignKey(Sessions, on_delete=models.CASCADE)
    court_id = models.ForeignKey(Court, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=BOOK_TYPE)
    name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=10, validators=[RegexValidator(PHONE_REGEX, 'Phone number must start with 07 and have 8 digits')])
    status = models.CharField(max_length=10, choices=STATUS, default='pendig')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name