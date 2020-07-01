from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Customer

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # to associate the new user to customer group automatically
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        # to assign a new user a new profile once signed up
        Customer.objects.create(user=instance, name=instance.username)
        