from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import UserProfile
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

@receiver(post_save, sender=UserProfile, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    """
    Signal receiver function to handle post-save operations for UserProfile model.
    Tokens for each user is generated each time a a userprofile is created.

    Args:
        sender: The model class that sent the signal (UserProfile).
        instance: The actual instance being saved.
        created: A boolean indicating whether the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None.
    """
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=get_user_model())
def set_superuser_role(sender, instance, created, **kwargs):
    """
    Signal receiver function to set the 'role' field of superuser instances.
    Each time a superuser is created, 'role' is set to 'admin' for that user.

    Args:
        sender: The model class that sent the signal (the user model).
        instance: The actual instance being saved.
        created: A boolean indicating whether the instance was created or updated.
        **kwargs: Additional keyword arguments.

    Returns:
        None.
    """
    if created and instance.is_superuser:
        instance.role = 'admin'
        instance.save()