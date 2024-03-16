from django.db import models

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

class Court(models.Model):
    name = models.CharField(max_length=50, unique=True)
    court_type = models.CharField(max_length=20, choices=COURT_TYPES)
    court_location = models.CharField(max_length=20, choices=COURT_LOCATION)
    has_lighting = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
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

    def __str__(self):
        return self.name

    