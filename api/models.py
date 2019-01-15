from django.db import models

# Create your models here.
class MyTest(models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
    	return self.name


class MyStore(models.Model):
    #mytest = models.ForeignKey(MyTest)
    storeName = models.CharField(max_length=255,unique=True)
    storeId = models.CharField(max_length=255,unique=True)
    
    def __str__(self):
    	return self.name