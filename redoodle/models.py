# coding: utf-8
from django.db import models
from django.contrib.auth.models import User


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

    def like(self, user):
        Like.objects.create(chain=self, user=user)
        self.likes += 1

    def dislike(self, user):
        user_like = Like.objects.get(chain=self, user=user)
        user_like.delete()
        self.likes -= 1


class Like(models.Model):
    user = models.ForeignKey(User)
    chain = models.ForeignKey(Chain)

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __unicode__(self):
        return '%s_%s' % (self.user.username, self.chain.name)
