from django.db import models

# Create your models here.
from members.models import PersonalProfile


class CommitteeMember(models.Model):
    POSITION = [
        ('PR', 'President'),
        ('VP', 'Vice President'),
        ('SC', 'Secretary'),
        ('TR', 'Treasurer'),
        ('MB', 'Member'),
    ]
    member = models.ForeignKey(PersonalProfile, on_delete=models.CASCADE)
    position = models.CharField(choices=POSITION, max_length=2)

    class Meta:
        verbose_name = 'Committee member'
        verbose_name_plural = 'Committee members'
        ordering = ['member']

    def __str__(self):
        return f'{self.member} : {self.position}'
