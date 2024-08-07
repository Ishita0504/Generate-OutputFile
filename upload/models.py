from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

class OutputData(models.Model):
    year = models.IntegerField()
    month = models.CharField(max_length=3)
    clubbed_name = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.year} {self.month} {self.clubbed_name} {self.product} {self.value}'

