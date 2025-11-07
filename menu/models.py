from django.db import models
from cloudinary.models import CloudinaryField

class DailySpecial(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image', folder='daily-specials/')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Daily Special'
        verbose_name_plural = 'Daily Specials'

    def __str__(self):
        return f"{self.name} - {'Active' if self.is_active else 'Inactive'}"