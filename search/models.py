from django.db import models


# Create your models here.

class Upload(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField()
    # def save(self, *args, **kwargs):
    #     print(self.file)
    #     print(dir(self.file))
    #     print(type(self.file))
    #     print(self.file.__dict__)
    #     super(Upload, self).save(*args, **kwargs)

