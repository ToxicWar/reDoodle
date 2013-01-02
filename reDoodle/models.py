# coding: utf-8
from django.db import models


class Room(models.Model):
    name = models.CharField('Name', max_length=255, default='')

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __unicode__(self):
        return self.name


class Chain(models.Model):
    name = models.CharField('Name', max_length=255, default='')
    likes = models.PositiveIntegerField('Likes', default=0)
    ban = []
    room = models.ForeignKey(Room)

    class Meta:
        verbose_name = 'Chain'
        verbose_name_plural = 'Chains'

    def __unicode__(self):
        return self.name
