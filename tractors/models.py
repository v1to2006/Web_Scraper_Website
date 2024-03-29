from django.db import models

class Tractor(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.name
