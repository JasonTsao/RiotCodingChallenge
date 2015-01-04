from django.db import models

# Create your models here.
class Mastery(models.Model):
	mastery_id = models.BigIntegerField(unique=True)
	name  = models.CharField(max_length=255, blank=True)
	mastery_type = models.CharField(max_length=255, blank=True)
	prereq = models.CharField(max_length=255, blank=True)

	def __unicode__(self):
		return self.mastery_type + ': ' + self.name


class Rune(models.Model):
	rune_id = models.BigIntegerField(unique=True)
	name  = models.CharField(max_length=255, blank=True)
	tier = models.IntegerField(null=True,blank=True)
	rune_type = models.CharField(max_length=255, blank=True)
	effect_type = models.CharField(max_length=255, blank=True)
	secondary_effect_type = models.CharField(max_length=255, blank=True)
	addition = models.FloatField(null=True,blank=True)
	secondary_addition = models.FloatField(null=True,blank=True)
	def __unicode__(self):
		return self.name + ' +' + str(self.addition) + ' ' + self.effect_type 