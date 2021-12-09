from django.db import models

# Create your models here.
class Visualisation(models.Model):
    item = models.CharField(max_length=500, null=True)
    price = models.FloatField(default=0)

    class Meta:
        verbose_name_plural = 'VisualisationData'

    def __str__(self):
        return self.item
