from retail.models import Member, GRAND_LEVEL


def calc_level_member(instance: Member):
    if instance.member_type == GRAND_LEVEL:
        instance.member_level = 0
    elif instance.supplier is not None:
        instance.member_level = instance.supplier.member_level + 1


def recalc_level_buyer(instance: Member):
    buyers = Member.objects.filter(supplier=instance)
    if len(buyers) > 0:
        for buyer in buyers:
            # buyer.member_level = instance.member_level + 1
            buyer.save()

def get_buyers_list(pk):
    instance = Member.objects.filter(pk=pk).first()
    buyers = list(instance.buyers.all())
    for buyer in instance.buyers.all():
        buyers.extend(get_buyers_list(buyer.pk))
    return buyers