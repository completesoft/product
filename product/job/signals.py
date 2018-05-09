from .models import CvState, CvStatusName
from django.db.models.signals import post_save
from django.dispatch import receiver
from candidate.models import Person

@receiver(post_save, sender=Person)
def create_cv_state(sender, instance, created, **kwargs):
    if created:
        status = CvStatusName.objects.get(status=0)
        CvState.objects.create(cv=instance, status=status)