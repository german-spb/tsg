from django.db import models

class Documents(models.Model):
    title = models.CharField(max_length=300)
    document = models.FileField(upload_to='documents/')

    def __str__(self):
        return self.title

