from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from admin_panel.models import AdminPanel
from user.models import User

@receiver(post_save, sender=AdminPanel)
def save_admin_panel(sender, instance, created, **kwargs):
    if created:
        instance.user.is_admin = True
        instance.user.save()


@receiver(pre_delete, sender=AdminPanel)
def delete_admin_panel(sender, instance, **kwargs):
    User.objects.filter(pk=instance.user.pk).update(is_admin=False)
