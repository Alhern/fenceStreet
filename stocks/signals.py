from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

#Fonction pour créer le profile et l'associer à l'utilisateur lors de la création du compte
@receiver(post_save, sender=User)
def crea_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

#Fonction qui sauvegarde le profile à chaque fois que l'utilisateur est sauvegardé
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
    
