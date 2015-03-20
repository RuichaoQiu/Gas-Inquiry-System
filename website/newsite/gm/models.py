# Create your models here.
from django.db import models
import datetime
from django.utils import timezone


class Car(models.Model):
    company = models.CharField(max_length=200)
    modeltype = models.CharField(max_length=200)
    madeyear = models.CharField(max_length=200)
    mpg = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __unicode__(self):
        return self.modeltype


class GasStation(models.Model):
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=200)
	price = models.CharField(max_length=200)
	location = models.CharField(max_length=200)

	def __unicode__(self):
		return self.address
	