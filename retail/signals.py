from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from retail.models import Member
from retail.src.utils import calc_level_member, recalc_level_buyer


@receiver(pre_save, sender=Member, weak=False, dispatch_uid="member_pre_save_handler")
def member_pre_save_handler(sender, instance: Member, *args, **kwargs):
    # return None
    calc_level_member(instance)
    if instance.pk:
        existing_instance: Member = Member.objects.filter(pk=instance.pk).first()
        if existing_instance is not None:
            if (
                instance.member_type != existing_instance.member_type
                or instance.supplier != existing_instance.supplier
                or instance.member_level != existing_instance.member_level
            ):
                instance.need_recalc = True


@receiver(post_save, sender=Member, weak=False, dispatch_uid="member_post_save_handler")
def member_post_save_handler(sender, instance: Member, *args, **kwargs):
    if instance is not None:
        if instance.need_recalc:
            recalc_level_buyer(instance)
