from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    reviews_count = models.IntegerField()
    positive_reviews_percent = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.name
