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
    isBlocked = models.BooleanField('IsBlocked', default=True)
    ban = []
    room = models.ForeignKey(Room)

    class Meta:
        verbose_name = 'Chain'
        verbose_name_plural = 'Chains'

    def __unicode__(self):
        return self.name

    def like(self):
        self.likes += 1

    def dislike(self):
        self.likes -= 1
