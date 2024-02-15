from django.db import models

class Car(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    mileage = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.make
