from retail.models import Member, GRAND_LEVEL


def calc_level_member(instance: Member):
    if instance.member_type == GRAND_LEVEL:
        instance.member_level = 0
    else:
        instance.member_level = instance.supplier.member_level + 1


def recalc_level_buyer(instance: Member):
    buyers: Member = Member.objects.filter(supplier=instance)
    if buyers is not None:
        for buyer in buyers:
            # buyer.member_level = instance.member_level + 1
            buyer.save()
