from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save

from admin_panel.models import AdminPanel
from user.models import User


@receiver(post_save, sender=User)
def sync_admin_panel(sender, instance, **kwargs):
    has_panel = AdminPanel.objects.filter(user_id=instance.id).exists()

    if instance.is_admin and not has_panel:
        AdminPanel.objects.create(user=instance)

    elif not instance.is_admin and has_panel:
        AdminPanel.objects.filter(user_id=instance.id).delete()


@receiver(pre_delete, sender=User)
def delete_admin_panel(sender, instance, **kwargs):
    if hasattr(instance, "adminpanel"):
        AdminPanel.objects.filter(user_id=instance.id).delete()
