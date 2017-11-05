from django.db import models
from django.contrib.auth.models import User


class Beer(models.Model):
    name = models.CharField(max_length=100)
    name_lower = models.CharField(max_length=100, default='')
    description = models.TextField(default='')

    def __str__(self):
        return '%s %s' % (self.id, self.name)

    class Meta:
        verbose_name = 'Beer'
        verbose_name_plural = 'Beer'


class Graph(models.Model):
    beer1_id = models.ForeignKey(Beer, null=False, related_name='+')
    beer2_id = models.ForeignKey(Beer, null=False, related_name='+')


class Like(models.Model):
    user_id = models.ForeignKey(User, null=False, related_name='+')
    beer_id = models.ForeignKey(Beer, null=False, related_name='+')


class Recommendation(models.Model):
    user = models.ForeignKey(User, related_name='+')
    beer = models.ForeignKey(Beer, related_name='+')
    mark = models.IntegerField(default=5)

    def __str__(self):
        return '%s %s' % (self.id, self.beer_id)
